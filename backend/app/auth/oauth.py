from collections.abc import Awaitable, Callable
from typing import Annotated, Any, Literal, TypeGuard

import httpx
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import Depends, Request

from app.auth.signup import OAuthIdentity
from app.config import Settings, get_settings
from app.errors import AppError

IdentityResolver = Callable[[str, Request], Awaitable[OAuthIdentity]]

Provider = Literal["google", "github"]


def build_oauth(settings: Settings) -> OAuth:
    oauth = OAuth()
    oauth.register(
        name="google",
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret.get_secret_value(),
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )
    oauth.register(
        name="github",
        client_id=settings.github_client_id,
        client_secret=settings.github_client_secret.get_secret_value(),
        authorize_url="https://github.com/login/oauth/authorize",
        access_token_url="https://github.com/login/oauth/access_token",  # noqa: S106 - public URL, not a secret
        api_base_url="https://api.github.com/",
        client_kwargs={"scope": "read:user user:email"},
    )
    return oauth


def get_oauth(
    settings: Annotated[Settings, Depends(get_settings)],
) -> OAuth:
    return build_oauth(settings)


def _google_identity(token: dict[str, Any]) -> OAuthIdentity:
    userinfo = token.get("userinfo")
    if userinfo is None:
        raise _login_failed()
    if (
        userinfo.get("email_verified") is not True
        or userinfo.get("sub") is None
        or userinfo.get("email") is None
    ):
        raise _login_failed()
    return OAuthIdentity("google", userinfo["sub"], userinfo["email"])


async def _github_identity(client: Any, token: dict[str, Any]) -> OAuthIdentity:
    try:
        user_resp = await client.get("user", token=token)
        user_resp.raise_for_status()
        emails_resp = await client.get("user/emails", token=token)
        emails_resp.raise_for_status()
        email = next(
            (
                item["email"]
                for item in emails_resp.json()
                if item.get("primary") and item.get("verified")
            ),
            None,
        )
        if email is None:
            raise _login_failed()
    except httpx.HTTPError:
        raise _login_failed() from None

    return OAuthIdentity("github", str(user_resp.json()["id"]), email)


async def resolve_identity(provider: Provider, request: Request, oauth: OAuth) -> OAuthIdentity:
    client = oauth.create_client(provider)
    if client is None:
        raise _login_failed()
    try:
        token = await client.authorize_access_token(request)
    except OAuthError:
        raise _login_failed() from None
    if provider == "google":
        return _google_identity(token)
    return await _github_identity(client, token)


def _login_failed() -> AppError:
    return AppError("LOGIN_FAILED", "Could not sign in. Please try again.", 401)


def _is_provider(value: str) -> TypeGuard[Provider]:
    return value in ("google", "github")


def get_identity_resolver(
    oauth: Annotated[OAuth, Depends(get_oauth)],
) -> IdentityResolver:
    async def resolver(provider: str, request: Request) -> OAuthIdentity:
        if not _is_provider(provider):
            raise _login_failed()
        return await resolve_identity(provider, request, oauth)

    return resolver
