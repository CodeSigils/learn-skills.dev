---
name: speech-engine
description: Add real-time voice conversations to a custom LLM, OpenClaw, or similar agent runtime with ElevenLabs Speech Engine. Use when building Speech Engine servers, WebSocket handlers, WebRTC browser clients, conversation token endpoints, interruption-aware streaming responses, or voice-enabled chat agents that connect a developer-owned LLM to ElevenLabs speech-to-text and text-to-speech.
license: MIT
compatibility: Requires internet access, an ElevenLabs API key (ELEVENLABS_API_KEY), and usually an LLM API key such as OPENAI_API_KEY.
metadata: {"openclaw": {"requires": {"env": ["ELEVENLABS_API_KEY"]}, "primaryEnv": "ELEVENLABS_API_KEY"}}
---

# ElevenLabs Speech Engine

Add a real-time voice interface to a custom LLM-backed agent. ElevenLabs handles microphone audio, speech-to-text, turn-taking, text-to-speech, and browser playback; your server exposes a Speech Engine WebSocket endpoint and streams the LLM response text back.

> **Setup:** See [Installation Guide](references/installation.md). For JavaScript, use `@elevenlabs/*` packages only. For deeper SDK details, read [JavaScript SDK Reference](references/javascript-sdk-reference.md) or [Python SDK Reference](references/python-sdk-reference.md).

## When to Use

Use Speech Engine when the user wants to:

- Add voice to an existing chat app or custom LLM pipeline
- Add voice to OpenClaw, Hermes, or a similar agent runtime while keeping agent logic on the developer-owned server
- Build a developer-hosted WebSocket server for ElevenLabs voice conversations
- Stream OpenAI, Anthropic, Gemini, or custom LLM responses back as spoken audio
- Handle user interruptions while an LLM response is still streaming
- Build a browser client with `@elevenlabs/react` or `@elevenlabs/client` using a server-issued conversation token

Use the `agents` skill instead when the user is creating or configuring a hosted ElevenLabs Conversational AI agent with platform-managed prompts, tools, workflows, phone numbers, or widgets.

## How It Works

Each Speech Engine WebSocket connection represents one conversation.

1. The browser sends user audio to ElevenLabs.
2. ElevenLabs transcribes speech and sends the full transcript to your server.
3. Your server calls the LLM with that conversation history.
4. Your server streams text back through the SDK.
5. ElevenLabs converts the response to speech and plays it in the browser.

The SDK manages WebSocket routing, request verification, session lifecycle, ping/pong, turn-taking, and interruption handling. `sendResponse()` / `send_response()` accepts a string, an async iterable, or provider streams from OpenAI, Anthropic, or Google Gemini.

## Implementation Flow

1. Install server dependencies and configure `ELEVENLABS_API_KEY` plus the LLM provider key.
2. Expose your Speech Engine server through a public HTTPS URL for local development, for example with `ngrok http 3001`.
3. Create a Speech Engine resource with `ws_url` / `wsUrl` pointing at the public URL plus `/ws`.
4. Store the returned Speech Engine ID, for example in `ELEVENLABS_SPEECH_ENGINE_ID`.
5. Start a Speech Engine server with `engine.serve(...)` in Python or `speechEngine.attach(...)` in TypeScript.
6. Issue browser conversation tokens from a server endpoint. Never put `ELEVENLABS_API_KEY` in browser code.
7. Start the client session with `conversationToken`; optionally set `overrides.agent.firstMessage` if the agent should greet first.

## Create a Speech Engine

### Python

```python
import asyncio
import os

from dotenv import load_dotenv
from elevenlabs import AsyncElevenLabs

load_dotenv()

elevenlabs = AsyncElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

async def main():
    engine = await elevenlabs.speech_engine.create(
        name="My Speech Engine",
        speech_engine={"ws_url": os.environ["PUBLIC_WS_URL"]},
    )
    print(engine.engine_id)

asyncio.run(main())
```

### TypeScript

```typescript
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";
import "dotenv/config";

const elevenlabs = new ElevenLabsClient({
  apiKey: process.env.ELEVENLABS_API_KEY,
});

const engine = await elevenlabs.speechEngine.create({
  name: "My Speech Engine",
  speechEngine: { wsUrl: process.env.PUBLIC_WS_URL! },
});

console.log(engine.engineId);
```

`PUBLIC_WS_URL` should look like `https://example.ngrok.app/ws` locally or your production WebSocket route in deployment.

The create request can also configure `tts`, `asr`, `turn`, `speech_engine.request_headers` / `speechEngine.requestHeaders`, and `privacy` for custom voices, transcription keywords, turn-taking, server auth headers, and recording behavior. See the SDK reference files for expanded examples.

## Server Examples

### Python

```python
import asyncio
import os

from dotenv import load_dotenv
from elevenlabs import AsyncElevenLabs
from openai import AsyncOpenAI

load_dotenv()

elevenlabs = AsyncElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def on_transcript(transcript, session):
    stream = await openai.responses.create(
        model=os.environ["OPENAI_MODEL"],
        instructions="You are a concise, conversational voice assistant.",
        input=[
            {
                "role": "assistant" if message.role == "agent" else message.role,
                "content": message.content,
            }
            for message in transcript
        ],
        stream=True,
    )
    await session.send_response(stream)

async def main():
    engine = await elevenlabs.speech_engine.get(os.environ["ELEVENLABS_SPEECH_ENGINE_ID"])
    await engine.serve(
        port=3001,
        path="/ws",
        debug=True,
        on_transcript=on_transcript,
    )

asyncio.run(main())
```

### TypeScript

```typescript
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";
import { createServer } from "node:http";
import OpenAI from "openai";
import "dotenv/config";

const elevenlabs = new ElevenLabsClient({
  apiKey: process.env.ELEVENLABS_API_KEY,
});
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const httpServer = createServer();

await elevenlabs.speechEngine.attach(
  process.env.ELEVENLABS_SPEECH_ENGINE_ID!,
  httpServer,
  "/ws",
  {
    debug: true,
    async onTranscript(transcript, signal, session) {
      const response = await openai.responses.create(
        {
          model: process.env.OPENAI_MODEL!,
          instructions: "You are a concise, conversational voice assistant.",
          input: transcript.map((message) => ({
            role: message.role === "agent" ? "assistant" : message.role,
            content: message.content,
          })),
          stream: true,
        },
        { signal },
      );

      session.sendResponse(response);
    },
  },
);

httpServer.listen(3001);
```

In TypeScript, pass the `AbortSignal` from `onTranscript` to the LLM request so user interruptions cancel the in-flight response. In Python, the SDK cancels the previous transcript handler when a newer transcript arrives.

## Browser Client

Create a server-side token endpoint and have the browser request a token before starting the microphone session. Keep the Speech Engine ID and API key on the server.

```typescript
import express from "express";
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";
import "dotenv/config";

const app = express();
const elevenlabs = new ElevenLabsClient();

app.get("/api/token", async (_req, res) => {
  const response = await elevenlabs.conversationalAi.conversations.getWebrtcToken({
    agentId: process.env.ELEVENLABS_SPEECH_ENGINE_ID!,
  });
  res.json({ token: response.token });
});
```

React clients can use `@elevenlabs/react`:

```tsx
import { useConversation } from "@elevenlabs/react";

export function VoiceControls() {
  const conversation = useConversation({
    onConnect: () => console.log("connected"),
    onDisconnect: () => console.log("disconnected"),
    onError: (error) => console.error(error),
  });

  async function startConversation() {
    await navigator.mediaDevices.getUserMedia({ audio: true });
    const { token } = await fetch("/api/token").then((res) => res.json());

    await conversation.startSession({
      conversationToken: token,
      overrides: {
        agent: { firstMessage: "Hello! How can I help you today?" },
      },
    });
  }

  return <button onClick={startConversation}>Start conversation</button>;
}
```

If a WebRTC browser session stalls or logs `/rtc/v1` 404s, `v1 RTC path not found`, or `could not establish pc connection`, pin `livekit-client` to `2.16.1` in the app's `package.json` until the upstream LiveKit compatibility issue is resolved:

```json
{
  "overrides": {
    "livekit-client": "2.16.1"
  }
}
```

## Callbacks and Events

| Event | TypeScript callback | Python callback | Notes |
| --- | --- | --- | --- |
| `user_transcript` | `onTranscript(transcript, signal, session)` | `on_transcript(transcript, session)` | Full conversation history for the current turn |
| `init` | `onInit(conversationId, session)` | `on_init(conversation_id, session)` | Conversation ID becomes available |
| `close` | `onClose(session)` | `on_close(session)` | Clean disconnect |
| `disconnected` | `onDisconnect(session)` | `on_disconnect(session)` | Unexpected WebSocket drop |
| `error` | `onError(error, session)` | `on_error(error, session)` | Protocol or WebSocket error |

Transcript messages use role `"user"` or `"agent"`. Map `"agent"` to `"assistant"` when passing history to LLM APIs that expect OpenAI-style roles.

## References

- [Installation Guide](references/installation.md)
- [JavaScript SDK Reference](references/javascript-sdk-reference.md)
- [Python SDK Reference](references/python-sdk-reference.md)
