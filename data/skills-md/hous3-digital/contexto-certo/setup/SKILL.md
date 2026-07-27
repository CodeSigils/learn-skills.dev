---
name: setup
description: Use when Track MCP is missing, returns 401/403, token expired or revoked, first-time agent connection, or the user asks how to configure Track MCP credentials in Cursor/Claude
---

# Setup (MCP Track)

## Visão geral

Guia **uma vez** (e de novo quando o token expirar) para o humano autenticar o MCP Track no agente.

**Anuncie:** "Usando setup para configurar o MCP Track."

**Fora de escopo:** instalar o pacote Contexto Certo (`npx skills add …` fica no README). Este skill assume que as skills já estão instaladas.

## Lei de ferro

```
NUNCA PEÇA, ACEITE, COLE OU ECOE O TOKEN NO CHAT
CREDENCIAIS SÓ NAS SETTINGS DO MCP DO AGENTE
401 / TOKEN EXPIRADO → VOLTAR AQUI (NÃO IMPROVISAR ESCOPO)
```

## Quando usar

- MCP Track não responde / não listado
- `hous3_health` ou qualquer tool Track retorna **401** / **403**
- Token expirado ou revogado
- Primeira conexão do agente ao Track
- Humano pergunta “como gero o token?” / “como configuro o MCP?”

**Quando NÃO usar:** MCP já autentica (smoke ok) — siga `usando-contexto-certo` / entrega normal.

## Passo a passo (mínimo)

Oriente o humano **um passo por vez**. Não peça o valor do token.

### 1. Conta Track

- Ter login no Track (produto / Community conforme o ambiente do time).
- Sem conta → apontar signup/login do produto; não inventar credenciais.

### 2. Abrir tokens MCP

- No app: **Configurações** → `/settings` (tokens / MCP).
- Portal client usa superfície própria de tokens — se for o caso, avise a diferença; este fluxo padrão é interno/delivery em `/settings`.

### 3. Gerar token (dados mínimos)

Só o necessário no formulário do produto:

| Campo | O que orientar |
|-------|----------------|
| Nome | Ex.: `cursor-contexto-certo` (rótulo legível) |
| Expiração | Usar o default sugerido pela UI (ou o máximo permitido se o humano quiser menos rotação) |

- Clicar **Gerar token**
- **Copiar na hora** — o valor costuma aparecer **uma vez**
- **Não** colar o token neste chat

### 4. URL do MCP

- Copiar a **URL do MCP** da própria tela de settings (botão de copiar).
- Não digitar URL de memória se a UI já oferece o valor certo do ambiente.

### 5. Colar no agente (Cursor / Claude)

No Cursor (ou equivalente), settings de MCP / `mcp.json`:

- Servidor remoto com a URL copiada
- Header `Authorization: Bearer <colar-o-token-só-aqui-nas-settings>`

Exemplo de **forma** (placeholder — nunca preencher com token real no chat):

```json
{
  "mcpServers": {
    "hous3-track": {
      "url": "<URL_COPIADA_DAS_SETTINGS>",
      "headers": {
        "Authorization": "Bearer <TOKEN_SÓ_NAS_SETTINGS_DO_AGENTE>"
      }
    }
  }
}
```

Perfil tipicamente usado com Contexto Certo: **delivery** / Community (o que o Track oferecer na criação do token).

### 6. Smoke

Depois que o humano confirmar que salvou o MCP:

1. Chamar `hous3_health` **ou** `list_my_tasks`
2. Sucesso → setup ok; anunciar retorno a `usando-contexto-certo`
3. Ainda 401/403 → repetir passos 3–5 (novo token; revogar o antigo se estiver exposto ou expirado). **Não** pedir o token no chat para “conferir”

## 401 no meio do trabalho

Qualquer skill do pacote que receber **401** (ou “token expirado”) deve:

1. **Parar** a entrega / edição
2. Invocar **`setup`** (este skill)
3. Só retomar `esclarecer-antes-de-planejar` / `planejar-no-track` / `implementar-task` / `fechar-task` após smoke ok

Não inventar escopo a partir do chat enquanto o MCP estiver sem auth.

## Sinais vermelhos

| Pensamento | Realidade |
|------------|-----------|
| "Manda o token aqui que eu configuro" | Proibido |
| "401, sigo com o que está no chat" | Pare → setup |
| "Instalo o pacote por esta skill" | Install é README / `npx skills add` |
| "Peço print do token pra debugar" | Nunca |

## Depois do verde

```
setup (ok) → usando-contexto-certo → planejar / implementar / …
```
