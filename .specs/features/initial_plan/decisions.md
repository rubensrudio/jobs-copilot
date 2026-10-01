# Decisões — initial_plan (Copiloto de busca de vagas)

Etapa: gate de clarificação do spec (`/generate-plan`, Passo 2).

## Decisões do humano

### LAC-01 — De onde o app lê o perfil e o CV Master?
- **Data**: 2026-10-01
- **Opções apresentadas**: A) lê os arquivos do /master-cv, só leitura, por caminho configurado B) importa uma cópia para o app C) perfil próprio editável na interface
- **Recomendação do spec-writer**: A
- **Escolha**: Outra (resposta livre, próxima de C)
- **Observações do humano**: O usuário faz upload do CV em PDF. A aplicação lê o PDF e preenche o perfil do usuário, salvo no banco de dados. O perfil pode ser modificado ou preenchido manualmente na interface. Não há leitura dos arquivos do /master-cv.

### LAC-02 — Em que formato sai o CV adaptado?
- **Data**: 2026-10-01
- **Opções apresentadas**: A) Markdown no formato CV Enviado B) Markdown + PDF C) só um briefing, e o humano roda /generate-cv
- **Recomendação do spec-writer**: B
- **Escolha**: Outra — o CV adaptado é gerado e exportado em PDF (sem Markdown como artefato entregue)
- **Observações do humano**: Primeira resposta: "Não vai gerar PDF nem Markdown; o CV será lido a partir de upload de arquivo PDF e preencherá o perfil do usuário, salvo no banco". Pergunta de esclarecimento (LAC-02b): "Sua resposta tira a geração de CV adaptado do app?" — opções: gera CV adaptado como texto na UI (recomendado) | sem CV adaptado | gera e exporta PDF. Resposta: **gera e exporta PDF**. Interpretação consolidada: entrada = CV em PDF (upload) que alimenta o perfil (LAC-01); saída = CV adaptado por vaga, gerado pelo agente e disponibilizado para download em PDF. Markdown não é formato de entrega.

### LAC-03 — Qual a fórmula do score de aderência (0–100)?
- **Data**: 2026-10-01
- **Opções apresentadas**: A) cobertura ponderada de requisitos B) similaridade de embeddings C) composição fixa de A e B, com as duas parcelas visíveis
- **Recomendação do spec-writer**: C
- **Escolha**: A
- **Observações do humano**: — (score = cobertura ponderada de requisitos; embeddings seguem usados para busca/similaridade, não compõem o score)

### LAC-04 — Que URLs o MVP aceita e o que fazer quando a captura falha?
- **Data**: 2026-10-01
- **Opções apresentadas**: A) qualquer página pública sem login, com a opção de colar o texto B) lista fechada de ATS C) só texto colado
- **Recomendação do spec-writer**: A
- **Escolha**: A
- **Observações do humano**: —

### LAC-05 — Qual a interface do MVP?
- **Data**: 2026-10-01
- **Opções apresentadas**: A) Angular desde o MVP B) API + CLI, com Angular no P2 C) só API
- **Recomendação do spec-writer**: A
- **Escolha**: A
- **Observações do humano**: —

### LAC-06 — Como o app é acessado e protegido?
- **Data**: 2026-10-01
- **Opções apresentadas**: A) local, sem login B) na nuvem, um único usuário com login C) multiusuário
- **Recomendação do spec-writer**: B
- **Escolha**: C — multiusuário
- **Observações do humano**: — (implica cadastro/login, isolamento de dados por usuário em todas as entidades e em todos os stores: MongoDB, Pinecone, MLflow/modelo de ranqueamento por usuário ou com segregação explícita)

### LAC-07 — Que dados do perfil podem ir para provedores externos?
- **Data**: 2026-10-01
- **Opções apresentadas**: A) só o conteúdo profissional, sem contato, salário e autorização de trabalho B) o perfil completo C) só modelos locais
- **Recomendação do spec-writer**: A
- **Escolha**: A
- **Observações do humano**: — (o PDF do CV enviado contém dados de contato; a extração deve separar dados pessoais antes de qualquer envio a LLM/Pinecone além da etapa de parsing)

### LAC-08 — Quais são as etapas do pipeline de candidaturas?
- **Data**: 2026-10-01
- **Opções apresentadas**: A) Aplicada → Entrevista → Oferta, mais Rejeitada e Desistência B) Aplicada e Encerrada C) etapas configuráveis
- **Recomendação do spec-writer**: A
- **Escolha**: A
- **Observações do humano**: —

### LAC-09 — Quais as fontes, os critérios e a frequência da coleta?
- **Data**: 2026-10-01
- **Opções apresentadas**: A) APIs e feeds públicos (agregadores e boards de ATS), com filtros, uma vez por dia B) scraping de LinkedIn ou Indeed C) e-mails de alerta das plataformas
- **Recomendação do spec-writer**: A
- **Escolha**: A
- **Observações do humano**: —

### LAC-10 — Qual o mínimo de rótulos e a regra de promoção do modelo?
- **Data**: 2026-10-01
- **Opções apresentadas**: A) 30 decisões, com pelo menos 5 por classe; promove só se superar o baseline B) 100 decisões C) treina e promove sempre
- **Recomendação do spec-writer**: A
- **Escolha**: A
- **Observações do humano**: — (multiusuário: mínimo vale por usuário)

### LAC-11 — Qual o canal e o gatilho dos alertas?
- **Data**: 2026-10-01
- **Opções apresentadas**: A) e-mail com limiar configurável B) Telegram C) só destaque na interface
- **Recomendação do spec-writer**: A
- **Escolha**: C — só destaque na interface
- **Observações do humano**: —

### LAC-12 — Em que idioma sai o CV adaptado?
- **Data**: 2026-10-01
- **Opções apresentadas**: A) inglês, e pt/es só se a vaga pedir B) o idioma da vaga C) o usuário escolhe a cada geração, com inglês como padrão
- **Recomendação do spec-writer**: C
- **Escolha**: C
- **Observações do humano**: —

### LAC-13 — O que fazer quando a mesma URL é enviada de novo?
- **Data**: 2026-10-01
- **Opções apresentadas**: A) devolver a análise existente, com ação de reanalisar B) reanalisar sempre C) recusar
- **Recomendação do spec-writer**: A
- **Escolha**: A
- **Observações do humano**: — (escopo: mesma URL pelo mesmo usuário)

### LAC-14 — Como controlar o custo dos serviços pagos?
- **Data**: 2026-10-01
- **Opções apresentadas**: A) teto mensal que bloqueia novas análises B) só registrar e exibir o custo C) sem controle
- **Recomendação do spec-writer**: A
- **Escolha**: A
- **Observações do humano**: — (multiusuário: teto por usuário e teto global, conforme descrito na pergunta)

### LAC-15 — Qual o tempo máximo de análise no MVP?
- **Data**: 2026-10-01
- **Opções apresentadas**: A) até 60 s, com progresso por etapa B) até 15 s C) sem limite
- **Recomendação do spec-writer**: A
- **Escolha**: A
- **Observações do humano**: —

### LAC-17 — Quais as regras de retenção e exclusão?
- **Data**: 2026-10-01
- **Opções apresentadas**: A) guarda indefinidamente, com exclusão em cascata por vaga B) guarda sem exclusão C) expurgo automático após N dias, mais a exclusão de A
- **Recomendação do spec-writer**: A
- **Escolha**: A
- **Observações do humano**: — (multiusuário: inclui exclusão em cascata por conta — vagas, análises, CVs gerados, PDF de CV enviado, perfil, decisões, vetores no Pinecone — atendendo LGPD)

### LAC-19 — Quem pode criar conta, e existe papel de administrador?
- **Data**: 2026-10-01 (etapa: spec, 2ª passada)
- **Opções apresentadas**: A) cadastro aberto, sem admin; teto global na configuração da implantação B) só por convite ou lista de e-mails, com admin que gere convites, contas e teto global C) cadastro aberto com admin para tetos e bloqueio de contas
- **Recomendação do spec-writer**: B
- **Escolha**: B
- **Observações do humano**: —

### LAC-20 — Qual o método de autenticação?
- **Data**: 2026-10-01 (etapa: spec, 2ª passada)
- **Opções apresentadas**: A) e-mail e senha, com confirmação e redefinição B) só login social (Google e GitHub) C) os dois
- **Recomendação do spec-writer**: B
- **Escolha**: B
- **Observações do humano**: —

### LAC-21 — Novo upload de PDF quando o perfil já existe
- **Data**: 2026-10-01 (etapa: spec, 2ª passada)
- **Opções apresentadas**: A) proposta com diff, confirmação item a item B) substitui tudo após uma confirmação C) upload só com perfil vazio
- **Recomendação do spec-writer**: A
- **Escolha**: B — substitui tudo após confirmação
- **Observações do humano**: —

### LAC-22 — PDF escaneado e tamanho máximo do upload
- **Data**: 2026-10-01 (etapa: spec, 2ª passada)
- **Opções apresentadas**: A) recusa sem OCR, orienta preenchimento manual, 5 MB B) OCR, 10 MB C) recusa sem OCR, 10 MB
- **Recomendação do spec-writer**: A
- **Escolha**: A
- **Observações do humano**: —

### LAC-23 — Gatilho do destaque "nova relevante"
- **Data**: 2026-10-01 (etapa: spec, 2ª passada)
- **Opções apresentadas**: A) score (ou pontuação do modelo promovido) acima de limiar configurável pelo usuário, padrão 70 B) N melhores de cada coleta C) toda vaga nova
- **Recomendação do spec-writer**: A
- **Escolha**: A
- **Observações do humano**: —

### LAC-24 — LGPD: consentimento e direitos do titular
- **Data**: 2026-10-01 (etapa: spec, 2ª passada)
- **Opções apresentadas**: A) aceite de termos e política (versão e data) + exportação + exclusão da conta B) aceite + exclusão C) só exclusão
- **Recomendação do spec-writer**: A
- **Escolha**: A
- **Observações do humano**: —

### LAC-25 — Pesos must_have : nice_to_have no score
- **Data**: 2026-10-01 (etapa: spec, 2ª passada)
- **Opções apresentadas**: A) 2:1 B) 3:1 C) só must_have
- **Recomendação do spec-writer**: A
- **Escolha**: B — 3:1
- **Observações do humano**: —

## Premissas assumidas (lacunas não bloqueantes)

### LAC-16 — Texto exato das mensagens ao usuário
- **Premissa**: textos propostos na seção 9 do spec.md
- **Reversibilidade**: alta
- **Onde impacta**: spec.md seção 9; componentes Angular

### LAC-18 — Idioma da interface
- **Premissa**: inglês (vitrine global)
- **Reversibilidade**: alta
- **Onde impacta**: textos da interface Angular
