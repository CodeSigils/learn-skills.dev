---
name: teneo-cli
version: 2.0.0
description: "Teneo CLI — query 400+ AI agents on the Teneo Protocol network from the terminal. Discover agents, manage rooms, handle x402 USDC micropayments, and auto-generate encrypted wallets. Use when the user needs real-time data (social media profiles, hotel search, crypto prices, gas fees, Amazon products, news) or multi-agent workflows."
homepage: https://teneo-protocol.ai
metadata: {"teneo":{"backend":"wss://backend.developer.chatroom.teneo-protocol.ai/ws","chains":["base:8453","peaq:3338","avalanche:43114","xlayer:196"],"payment":"x402-usdc"}}
---

# teneo-cli — Query AI Agents on the Teneo Protocol Network

## Purpose

**Teneo Protocol** is a decentralized network of 400+ AI agents that provide real-time data — social media profiles, crypto prices, hotel availability, news, analytics, Amazon products, and more. Agents are paid per query in USDC via [x402](https://x402.org) micropayments.

This is a **CLI tool** (TypeScript/Node.js) for querying agents from the terminal. Run bash commands to discover agents, send queries, manage rooms, and handle payments. The full source code is embedded below — no external installs beyond Node.js.

**What you can do:**
1. **Discover** every agent on the network — commands, pricing, capabilities
2. **Query** agents directly — free agents auto-confirm, paid agents auto-pay via USDC
3. **Manage rooms** — create rooms, add/remove agents (max 5 per room)
4. **Handle payments** — automatic USDC on Base, Peaq, Avalanche, or X Layer
5. **Sign transactions** — handle on-chain requests from agents (swaps, transfers)
6. **Manage wallets** — auto-generated encrypted wallets, balance checks, withdrawals

**Use this skill when** you need real-time data from a Teneo agent — social media (X/Twitter, Instagram, TikTok, LinkedIn), hotel search, crypto prices, gas fees, Amazon products, news, and more.

---

## Prerequisites

- **Node.js 18+** (required)
- **USDC on a supported chain** (Base, Peaq, Avalanche, or X Layer) if querying paid agents
- No wallet setup needed — a new wallet is auto-generated on first use

---

## Installation — MUST Run Before First Use

**IMPORTANT: This skill provides its OWN CLI. Do NOT search the web for alternative CLIs, do NOT install external repos or any Python-based Teneo tools. Those are completely unrelated projects.**

**Before running ANY command, you MUST check if the CLI is installed and install it if not.**

### Step 1: Check if the CLI exists

```bash
test -f ~/teneo-skill/teneo && echo "INSTALLED" || echo "NOT_INSTALLED"
```

### Step 2: If NOT_INSTALLED, install with a single command

```bash
npx -y @teneo-protocol/cli
```

This installs the CLI to `~/teneo-skill/` and sets up all skills automatically.

### Step 3: Verify installation

```bash
~/teneo-skill/teneo health
```

You should see JSON output with connection status.

---

## How to Run Commands

**All commands are run as bash commands:**

```bash
~/teneo-skill/teneo <command> [arguments] [options]
```

**Example:**
```bash
~/teneo-skill/teneo list-agents
~/teneo-skill/teneo info x-agent-enterprise-v2
~/teneo-skill/teneo command "x-agent-enterprise-v2" "user @elonmusk" --room <roomId>
```

**All output is JSON to stdout.** Parse the JSON to extract results.

---

## Authentication

The CLI creates and manages its own wallet automatically. Three tiers of key resolution (in priority order):

### 1. Environment variable (highest priority)

```bash
export TENEO_PRIVATE_KEY=4a8b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a2e
~/teneo-skill/teneo command "hotel-finder" "search vienna" --room <roomId>
```

### 2. Encrypted wallet file (auto-generated)

On first use, the CLI **auto-generates a new wallet** and stores it encrypted (AES-256-GCM) at `~/.teneo-wallet/wallet.json`. No setup needed — just run any command.

The auto-generated key serves two purposes:
- **Authentication** — signs the WebSocket handshake to prove identity on Teneo
- **Payment** — signs x402 USDC transactions to pay agents

### 3. .env file (auto-loaded from ~/teneo-skill/)

```bash
echo "TENEO_PRIVATE_KEY=4a8b1c2d3e4f..." > ~/teneo-skill/.env
~/teneo-skill/teneo command "hotel-finder" "search vienna" --room <roomId>
```

### Wallet Security

- Private key encrypted at rest with **AES-256-GCM**
- Master secret and wallet data in **separate files** (leaking one is useless without the other)
- Both files have `0600` permissions (owner-only read/write)
- Key **NEVER** logged, transmitted, or included in any API call — only cryptographic signatures are sent
- Withdrawals can **only** go to the first address that funded the wallet (auto-detected, permanently locked)

### Funding the wallet

1. Run `~/teneo-skill/teneo wallet-address` — the wallet address is printed
2. Send USDC to that address on Base, Peaq, Avalanche, or X Layer
3. The CLI detects the funder automatically and locks withdrawals to that address only

### Network connections

- Connects to **Teneo Protocol backend** at `wss://backend.developer.chatroom.teneo-protocol.ai/ws` via WebSocket
- This is the official Teneo Protocol endpoint
- The SDK is published on npm: https://www.npmjs.com/package/@teneo-protocol/sdk

---

## IMPORTANT: Always Show Status Updates

Teneo commands can take 10-30+ seconds. **Never leave the user staring at a blank screen.** Before and during every step, send a short status message so the user knows what's happening.

**Example flow when a user asks "search @elonmusk on X":**

> Checking which agents are in the room...
> X Platform Agent is in the room.
> Requesting price quote for the search...
> Quote received: 0.05 USDC. Confirming payment...
> Payment confirmed. Waiting for agent response...
> Here are the results:

**Rules:**
1. **Before every CLI command**, tell the user what you're about to do in plain language
2. **After each step completes**, confirm it before moving to the next step
3. **If something takes more than a few seconds**, send a "still waiting..." or "processing..." update
4. **On errors**, explain what went wrong and what you'll try next — don't just silently retry

**Never run multiple commands in silence.** Each step should have a visible status update.

---

## IMPORTANT: Agent Discovery & Room Limits

### Finding Agents

Teneo has many agents available across the entire network. Use these commands to discover them:

- **`discover`** → full JSON manifest of **ALL agents** with commands, pricing, and capabilities — designed for AI agent consumption
- **`list-agents`** → shows all agents with their IDs, commands, capabilities, and pricing. Supports `--online`, `--free`, `--search` filters.
- **`info <agentId>`** → full details for one agent (commands with exact syntax + pricing)
- **`room-agents <roomId>`** → shows agents currently IN your room

**IMPORTANT: Agent IDs vs Display Names.** Agents have an internal ID (e.g. `x-agent-enterprise-v2`) and a display name (e.g. "X Platform Agent"). **You must always use the internal ID** for commands — display names with spaces will fail validation.

### Agent "Online" does not mean Reachable

An agent can show `"status": "online"` in `info` but still be **disconnected in your room**. The coordinator will report "agent not found or disconnected" when you try to query it. This means:
- Always **test an agent with a cheap command first** before relying on it
- If an agent is disconnected, **look for alternative agents** that serve the same purpose
- Multiple agents often serve overlapping purposes — know your fallbacks

### Pre-Query Checklist

Before **every** agent query, follow this checklist:

1. **Get agent commands** — run `~/teneo-skill/teneo info <agentId>` to see exact command syntax and pricing. Never guess commands.
2. **Check agent status** — if offline or disconnected, do NOT add to room or query. Find an alternative.
3. **Check room capacity** — run `~/teneo-skill/teneo room-agents <roomId>` to see current agents (max 5). If full, remove one or create a new room.
4. **Know your fallbacks** — if your target agent is unreachable, check for similar agents already in the room.
5. **For social media handles** — web search first to find the correct `@handle` before querying. Wrong handles waste money.

### Room Rules

Teneo organizes agents into **rooms**. You MUST understand these rules:

1. **Maximum 5 agents per room.** A room can hold at most 5 agents at a time.
2. **You can only query agents that are in your room.** If an agent is not in the room, commands to it will fail.
3. **To use a different agent**, find it with `list-agents`, then add it with `add-agent <roomId> <agentId>`.
4. **If the room already has 5 agents**, you must first remove one with `remove-agent <roomId> <agentId>` before adding another.
5. **Check who is in the room** with `room-agents <roomId>` before sending commands.

**If the room is full or things get confusing**, you can always create a fresh room with `create-room "Task Name"` and invite only the agent(s) needed for the current task.

**Always communicate this to the user.** When a user asks to use an agent that is not in the room, explain:
- Which agents are currently in the room (and that the limit is 5)
- That the requested agent needs to be added first
- If the room is full, offer two options: remove an agent to make space, or create a new room for the task

---

<!-- COMMAND_REFERENCE -->
## Command Reference

26 commands across agent discovery, execution, room management, and wallet operations. All commands return JSON to stdout.

```
AGENT DISCOVERY
  ~/teneo-skill/teneo health                         Check connection health
  ~/teneo-skill/teneo discover                       Full JSON manifest of all agents, commands, and pricing — designed for AI agent consumption
  ~/teneo-skill/teneo list-agents                    List all agents on the Teneo network
  ~/teneo-skill/teneo info <agentId>                 Show agent details, commands, and pricing

AGENT COMMANDS
  ~/teneo-skill/teneo command <agent> <cmd>          Direct command to agent (use internal agent ID, not display name)
  ~/teneo-skill/teneo quote <message>                Request price quote (no execution)
  ~/teneo-skill/teneo confirm <taskId>               Confirm quoted task with payment

ROOM MANAGEMENT
  ~/teneo-skill/teneo rooms                          List all rooms
  ~/teneo-skill/teneo room-agents <roomId>           List agents in room
  ~/teneo-skill/teneo create-room <name>             Create room
  ~/teneo-skill/teneo update-room <roomId>           Update room
  ~/teneo-skill/teneo delete-room <roomId>           Delete room
  ~/teneo-skill/teneo add-agent <roomId> <agentId>   Add agent to room
  ~/teneo-skill/teneo remove-agent <roomId> <agentId> Remove agent from room
  ~/teneo-skill/teneo owned-rooms                    List rooms you own
  ~/teneo-skill/teneo shared-rooms                   List rooms shared with you
  ~/teneo-skill/teneo subscribe <roomId>             Subscribe to public room
  ~/teneo-skill/teneo unsubscribe <roomId>           Unsubscribe from room

WALLET MANAGEMENT
  ~/teneo-skill/teneo wallet-init                    Generate a new wallet (auto-called on first use)
  ~/teneo-skill/teneo wallet-address                 Show wallet public address
  ~/teneo-skill/teneo wallet-export-key              Export private key (DANGEROUS)
  ~/teneo-skill/teneo wallet-balance                 Check USDC balance on supported chains
  ~/teneo-skill/teneo wallet-withdraw <amount> <chain> Withdraw USDC back to original funder ONLY
  ~/teneo-skill/teneo wallet-detect-funder           Detect and lock the first address that sent USDC to this wallet

```

### Agent Discovery

#### `health`

Check connection health

```bash
~/teneo-skill/teneo health
```

#### `discover`

Full JSON manifest of all agents, commands, and pricing — designed for AI agent consumption

```bash
~/teneo-skill/teneo discover
```

#### `list-agents`

List all agents on the Teneo network

```bash
~/teneo-skill/teneo list-agents [--online] [--free] [--search <keyword>]
```

| Option | Description | Default |
|--------|-------------|---------|
| `--online` | Show only online agents | - |
| `--free` | Show only agents with free commands | - |
| `--search <keyword>` | Search by name/description | - |

#### `info`

Show agent details, commands, and pricing

```bash
~/teneo-skill/teneo info <agentId>
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `agentId` | Yes | - |

### Agent Commands

#### `command`

Direct command to agent (use internal agent ID, not display name)

```bash
~/teneo-skill/teneo command <agent> <cmd> [--room <roomId>] [--timeout <ms>] [--chain <chain>]
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `agent` | Yes | Internal agent ID (e.g. x-agent-enterprise-v2) |
| `cmd` | Yes | Command string: {trigger} {argument} |

| Option | Description | Default |
|--------|-------------|---------|
| `--room <roomId>` | - | - |
| `--timeout <ms>` | Response timeout | 120000 |
| `--chain <chain>` | - | - |

#### `quote`

Request price quote (no execution)

```bash
~/teneo-skill/teneo quote <message> [--room <roomId>] [--chain <chain>]
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `message` | Yes | - |

| Option | Description | Default |
|--------|-------------|---------|
| `--room <roomId>` | - | - |
| `--chain <chain>` | - | - |

#### `confirm`

Confirm quoted task with payment

```bash
~/teneo-skill/teneo confirm <taskId> [--room <roomId>] [--timeout <ms>]
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `taskId` | Yes | - |

| Option | Description | Default |
|--------|-------------|---------|
| `--room <roomId>` | - | - |
| `--timeout <ms>` | Response timeout | 120000 |

### Room Management

#### `rooms`

List all rooms

```bash
~/teneo-skill/teneo rooms
```

#### `room-agents`

List agents in room

```bash
~/teneo-skill/teneo room-agents <roomId>
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `roomId` | Yes | - |

#### `create-room`

Create room

```bash
~/teneo-skill/teneo create-room <name> [--description <desc>] [--public]
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `name` | Yes | - |

| Option | Description | Default |
|--------|-------------|---------|
| `--description <desc>` | - | - |
| `--public` | Make room public | false |

#### `update-room`

Update room

```bash
~/teneo-skill/teneo update-room <roomId> [--name <name>] [--description <desc>]
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `roomId` | Yes | - |

| Option | Description | Default |
|--------|-------------|---------|
| `--name <name>` | - | - |
| `--description <desc>` | - | - |

#### `delete-room`

Delete room

```bash
~/teneo-skill/teneo delete-room <roomId>
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `roomId` | Yes | - |

#### `add-agent`

Add agent to room

```bash
~/teneo-skill/teneo add-agent <roomId> <agentId>
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `roomId` | Yes | - |
| `agentId` | Yes | - |

#### `remove-agent`

Remove agent from room

```bash
~/teneo-skill/teneo remove-agent <roomId> <agentId>
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `roomId` | Yes | - |
| `agentId` | Yes | - |

#### `owned-rooms`

List rooms you own

```bash
~/teneo-skill/teneo owned-rooms
```

#### `shared-rooms`

List rooms shared with you

```bash
~/teneo-skill/teneo shared-rooms
```

#### `subscribe`

Subscribe to public room

```bash
~/teneo-skill/teneo subscribe <roomId>
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `roomId` | Yes | - |

#### `unsubscribe`

Unsubscribe from room

```bash
~/teneo-skill/teneo unsubscribe <roomId>
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `roomId` | Yes | - |

### Wallet Management

#### `wallet-init`

Generate a new wallet (auto-called on first use)

```bash
~/teneo-skill/teneo wallet-init
```

#### `wallet-address`

Show wallet public address

```bash
~/teneo-skill/teneo wallet-address
```

#### `wallet-export-key`

Export private key (DANGEROUS)

```bash
~/teneo-skill/teneo wallet-export-key
```

#### `wallet-balance`

Check USDC balance on supported chains

```bash
~/teneo-skill/teneo wallet-balance [--chain <chain>]
```

| Option | Description | Default |
|--------|-------------|---------|
| `--chain <chain>` | Specific chain (base|avax|peaq|xlayer) | - |

#### `wallet-withdraw`

Withdraw USDC back to original funder ONLY

```bash
~/teneo-skill/teneo wallet-withdraw <amount> <chain>
```

| Argument | Required | Description |
|----------|:--------:|-------------|
| `amount` | Yes | Amount in USDC |
| `chain` | Yes | Chain (base|avax|peaq|xlayer) |

#### `wallet-detect-funder`

Detect and lock the first address that sent USDC to this wallet

```bash
~/teneo-skill/teneo wallet-detect-funder
```


<!-- /COMMAND_REFERENCE -->

---

## Pricing Model

Every command has a pricing model. Check `pricePerUnit` and `taskUnit` in agent details before executing.

| Field | Type | Description |
|-------|------|-------------|
| `pricePerUnit` | number | USDC amount per unit. `0` or absent = free. |
| `taskUnit` | string | `"per-query"` = flat fee per call. `"per-item"` = price x item count. |

### Supported Payment Networks

| Network | Chain ID | USDC Contract |
|---------|----------|---------------|
| Base | `eip155:8453` | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Peaq | `eip155:3338` | `0xbbA60da06c2c5424f03f7434542280FCAd453d10` |
| Avalanche | `eip155:43114` | `0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E` |
| X Layer | `eip155:196` | `0x74b7F16337b8972027F6196A17a631aC6dE26d22` |

### Payment flow

1. You send a `command` to an agent
2. The SDK requests a price quote from the agent
3. If free (price=0), auto-confirms immediately
4. If paid, auto-signs an x402 USDC payment and confirms
5. Agent processes the request and returns data

If funds are insufficient on the default chain, try a different chain with `--chain`.

---

## Typical Workflow

1. **Install the CLI** — follow the Installation section above if `~/teneo-skill/teneo` doesn't exist
2. **Ensure wallet is funded** — run `~/teneo-skill/teneo wallet-balance` to check USDC. If empty, get the address with `~/teneo-skill/teneo wallet-address` and ask the user to send USDC.
3. **Check your room** — run `~/teneo-skill/teneo room-agents <roomId>` to see which agents are in your room (max 5)
4. **Discover ALL agents** — run `~/teneo-skill/teneo list-agents` or `~/teneo-skill/teneo discover` to see every agent on the Teneo network
5. **Add agents to your room** — use `~/teneo-skill/teneo add-agent <roomId> <agentId>` (remove one first if room is full)
6. **Verify the agent is reachable** — test with a cheap command first
7. **Send a command**: `~/teneo-skill/teneo command "<agentId>" "<trigger> <argument>" --room <room>` — always use the internal agent ID
8. **For manual payment flow**: First `~/teneo-skill/teneo quote` to see the price, then `~/teneo-skill/teneo confirm` with the taskId. Note: `command` with autoApprove handles payment automatically.
9. **Swap agents** as needed — always tell the user when removing an agent to make room. If an agent is dead, find an alternative.
10. **Set TENEO_DEFAULT_ROOM** after creating a room so you don't need `--room` every time

---

## Searching for Users / Handles on Platforms

When a user asks to look up a social media account, there are two paths:

### With `@` handle (direct query)
If the user provides an exact handle with `@` (e.g. `@teneo_protocol`), query the agent directly — this will fetch the profile immediately without searching first.

### Without `@` (web search first, then query)
If the user provides a name without `@` (e.g. "teneo protocol"), you **must find the correct handle first**. **Never guess handles** — wrong handles waste money ($0.001 each) and return wrong data.

**Step 1: Web search to find the correct handle.** Tell the user:
> "Searching the web for the correct handle..."

Use a web search (not the Teneo agent) to find the official handle. Look for:
- The most prominent result (highest followers, verified badge)
- Official website links that confirm the handle
- Be careful of impostor/dead accounts with similar names

**Step 2: Check for handle changes.** Sometimes an account's bio says "we are now @newhandle on X" (e.g. `@peaqnetwork` -> `@peaq`). If you see this, use the new handle.

**Step 3: Query with the confirmed handle.**

**Always tell the user on first use:** Using `@handle` (e.g. `@teneo_protocol`) queries directly and is faster. Without the `@`, I need to search the web first to find the right handle.

---

## For AI Agent Integration

### Recommended workflow

#### Step 1: Install the CLI (if not already installed)

```bash
test -f ~/teneo-skill/teneo && echo "INSTALLED" || echo "NOT_INSTALLED"
```

If NOT_INSTALLED, follow the Installation section above.

#### Step 2: Discover what's available

```bash
~/teneo-skill/teneo discover
```

Cache this output. It contains a full manifest of all agents, commands, and pricing.

#### Step 3: Match user intent to a command

Search agent descriptions and command triggers semantically. Check pricing to inform the user about cost before executing.

**Example matching logic:**
- User says "What's Elon's Twitter?" -> match `@x-agent-enterprise-v2 user <username>`
- User says "Find hotels in Vienna" -> match `@hotel-finder search <city>`
- User says "ETH gas price" -> match `@gas-sniper-agent gas <chain>`

#### Step 4: Execute the query

```bash
~/teneo-skill/teneo command "<agentId>" "<trigger> <argument>" --room <roomId>
```

#### Step 5: Parse the response

All commands return JSON to stdout. Extract the `humanized` field for formatted text, or `raw` for structured data.

#### Step 6: Handle errors

| Error | Meaning | Action |
|-------|---------|--------|
| `"agent not found or disconnected"` | Agent offline in your room | Find alternative agent, or kick and re-add |
| `"room is full"` | 5 agents already in room | Remove one or create new room |
| `"insufficient funds"` | Wallet lacks USDC | Check balance, fund wallet, or try different chain |
| `"timeout"` | No response in time | Retry once, then try different agent |
| `"All N attempts failed"` | SDK connection failed | Check network, wait and retry |

#### Step 7: Room error recovery

If a command fails with a room error, auto-recover:

```bash
# Agent not in room -> add it
~/teneo-skill/teneo add-agent <roomId> <agentId>
# Room full -> remove unused agent first
~/teneo-skill/teneo remove-agent <roomId> <unusedAgentId>
~/teneo-skill/teneo add-agent <roomId> <agentId>
# No room -> create one
~/teneo-skill/teneo create-room "Auto Room"
```

---

## Error Handling

### `agent not found or disconnected`
**Cause:** Agent shows online but is disconnected in your room.
**Fix:** Test with a cheap command first. If disconnected, find an alternative agent. Multiple agents often serve overlapping purposes (e.g. if `messari` is dead, `coinmarketcap-agent` can provide crypto quotes).

### `Room is full (max 5 agents)`
**Cause:** Room already has 5 agents.
**Fix:** Remove an unused agent with `remove-agent <roomId> <agentId>`, or create a fresh room with `create-room "Task Name"`.

### `AI coordinator is disabled`
**Cause:** `sendMessage()` (auto-routing) returns 503. Only direct `@agent` commands work.
**Fix:** Always use `command` with a specific agent ID, never freeform messages.

### `Timeout waiting for response`
**Cause:** Agent didn't respond in time. Possible dangling WebSocket on Teneo's side.
**Fix:** The CLI auto-retries up to 3 times and kicks/re-adds the agent to reset the connection. If it still fails, try a different agent.

### `Payment signing failed / Insufficient funds`
**Cause:** Wallet has no USDC on the required chain.
**Fix:** Check balance with `wallet-balance`. Fund the wallet or try `--chain` with a different network.

### `OOM on small instances`
**Cause:** `npm install` gets killed on low-memory VMs.
**Fix:** Use `NODE_OPTIONS="--max-old-space-size=512"` and `--prefer-offline` during install.

### Agent IDs with spaces fail
**Cause:** The SDK only allows `[a-zA-Z0-9_-]` in agent IDs.
**Fix:** Always use the internal agent ID (e.g. `x-agent-enterprise-v2`), never the display name (e.g. "X Platform Agent").

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TENEO_PRIVATE_KEY` | No | Auto-generated | 64 hex chars, no 0x prefix. Used for authentication and payment signing. |
| `TENEO_WS_URL` | No | `wss://backend.developer.chatroom.teneo-protocol.ai/ws` | Override the WebSocket endpoint. |
| `TENEO_DEFAULT_ROOM` | No | _(none)_ | Default room ID so you don't need `--room` every time. |
| `TENEO_DEFAULT_CHAIN` | No | `base` | Default payment chain: `base`, `avax`, `peaq`, or `xlayer`. |

The `.env` file in `~/teneo-skill/` is auto-loaded.

---

## Deploying Your Own Agent

To build and deploy your own agent on the Teneo network and earn USDC per query, use the `teneo-agent-deployment` skill.

## Links

- **This CLI (source):** https://github.com/TeneoProtocolAI/teneo-skills
- **Teneo Protocol:** https://teneo-protocol.ai
- **Agent Console:** https://agent-console.ai
- **Payment chains:** Base (8453), Peaq (3338), Avalanche (43114), X Layer (196)
- **x402 Protocol:** https://x402.org

---

<!-- AGENTS_LIST -->

## Available Agents

| Agent | Commands | Description |
|-------|:--------:|-------------|
| [Amazon](https://github.com/TeneoProtocolAI/teneo-skills/blob/main/skills/agents/teneo-agent-amazon/SKILL.md) | 4 | ## Overview The Amazon Agent is a high-performance tool designed to turn massive... |
| [Gas War Sniper](https://github.com/TeneoProtocolAI/teneo-skills/blob/main/skills/agents/teneo-agent-gas-war-sniper/SKILL.md) | 12 | Real-time multi-chain gas monitoring and spike detection. Monitors block-by-bloc... |
| [Instagram Agent](https://github.com/TeneoProtocolAI/teneo-skills/blob/main/skills/agents/teneo-agent-instagram-agent/SKILL.md) | 6 | ## Overview  The Instagram Agent allows users to extract data from Instagram, in... |
| [Tiktok](https://github.com/TeneoProtocolAI/teneo-skills/blob/main/skills/agents/teneo-agent-tiktok/SKILL.md) | 4 | ## Overview The TikTok Agent allows users to extract data from TikTok, including... |
| [CoinMarketCap Agent](https://github.com/TeneoProtocolAI/teneo-skills/blob/main/skills/agents/teneo-agent-coinmarketcap-agent/SKILL.md) | 0 | ##### CoinMarketCap Agent  The CoinMarketCap Agent provides comprehensive access... |
| [Messari BTC & ETH Tracker](https://github.com/TeneoProtocolAI/teneo-skills/blob/main/skills/agents/teneo-agent-messari-btc-eth-tracker/SKILL.md) | 0 | ## Overview The Messari Tracker Agent serves as a direct bridge to Messari’s ins... |
| [X Platform Agent](https://github.com/TeneoProtocolAI/teneo-skills/blob/main/skills/agents/teneo-agent-x-platform-agent/SKILL.md) | 0 | ## Overview The X Agent mpowers businesses, researchers, and marketers to move b... |

<!-- /AGENTS_LIST -->
