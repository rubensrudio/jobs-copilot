import logging
from datetime import UTC, datetime, timedelta
from typing import Annotated, Any

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse
from pymongo.database import Database

from app.auth.oauth import IdentityResolver, get_identity_resolver, get_oauth
from app.auth.sessions import create_session, set_session_cookie
from app.auth.signup import find_user_by_identity, is_email_allowed, record_signup_attempt
from app.config import Settings, get_settings
from app.db import get_db
from app.errors import AppError

router = APIRouter(prefix="/api/auth")
logger = logging.getLogger(__name__)

PROVIDERS = ["google", "github"]
PENDING_SIGNUP_TTL = timedelta(minutes=10)


def _redirect(settings: Settings, path: str) -> RedirectResponse:
    return RedirectResponse(f"{settings.frontend_url}{path}", status_code=302)


@router.get("/login/{provider}")
async def login(
    provider: str,
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
    oauth: Annotated[OAuth, Depends(get_oauth)],
) -> Response:
    if provider not in PROVIDERS:
        raise AppError("NOT_FOUND", "Not found.", 404)

    client = oauth.create_client(provider)

    redirect_uri = f"{settings.frontend_url}/api/auth/callback/{provider}"

    response: Response = await client.authorize_redirect(request, redirect_uri)
    return response


@router.get("/callback/{provider}")
async def callback(
    provider: str,
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
    db: Annotated[Database[dict[str, Any]], Depends(get_db)],
    resolver: Annotated[IdentityResolver, Depends(get_identity_resolver)],
) -> RedirectResponse:
    try:
        identity = await resolver(provider, request)
    except AppError:
        logger.info("auth.login provider=%s outcome=failed", provider)
        return _redirect(settings, "/login?error=login_failed")

    user = find_user_by_identity(db, identity)
    if user is not None:
        user_id = str(user["_id"])

        if not user.get("active") or user.get("deletion_pending"):
            logger.info("auth.login provider=%s outcome=inactive user_id=%s", provider, user_id)
            return _redirect(settings, "/login?error=login_failed")

        token = create_session(
            db, user_id, ttl_days=settings.session_ttl_days, now=datetime.now(UTC)
        )
        response = _redirect(settings, "/jobs")
        set_session_cookie(response, token, settings)
        logger.info("auth.login provider=%s outcome=success user_id=%s", provider, user_id)
        return response

    now = datetime.now(UTC)
    if not is_email_allowed(db, identity.email, settings):
        record_signup_attempt(db, identity.email, provider, "rejected_not_invited", now)
        logger.info("auth.signup provider=%s outcome=rejected_not_invited", provider)
        return _redirect(settings, "/login?error=not_invited")

    record_signup_attempt(db, identity.email, provider, "pending_terms", now)
    request.session["pending_signup"] = {
        "provider": identity.provider,
        "subject": identity.subject,
        "email": identity.email,
        "exp": (now + PENDING_SIGNUP_TTL).timestamp(),
    }
    logger.info("auth.signup provider=%s outcome=pending_terms", provider)
    return _redirect(settings, "/signup/terms")
