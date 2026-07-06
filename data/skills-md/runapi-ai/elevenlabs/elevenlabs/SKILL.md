---
name: elevenlabs
description: Generate speech, dialogue, and sound with ElevenLabs through RunAPI. Use when the user asks an agent to create speech, dialogue, or sound effects, or transcribe audio with ElevenLabs. Default to the RunAPI CLI for one-off generation; use SDKs only when the user is integrating RunAPI into an app or backend.
documentation: https://runapi.ai/models/elevenlabs.md
provider_page: https://runapi.ai/providers/elevenlabs.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/elevenlabs
    requires:
      bins:
      - runapi
    install:
    - kind: brew
      formula: runapi-ai/tap/runapi
      bins:
      - runapi
    envVars:
    - name: RUNAPI_API_KEY
      required: false
      description: Optional RunAPI API key; agents should prefer environment auth or saved CLI config. Browser login is interactive fallback only.
---

# ElevenLabs on RunAPI

Generate speech, dialogue, and sound with ElevenLabs through RunAPI. The default path for one-off agent tasks is the `runapi` CLI; SDKs are for application integration.

## Critical: Integration Runtime

- Integration work (app, backend, worker, library, Rails service, Node service, Go service, webhook pipeline, or production codebase) uses the **SDK integration path** for the target language.
- One-off generation, editing, transformation, manual smoke tests, debugging, or user-requested CLI runs use the **CLI path** with the `runapi` binary. For full CLI-specific agent guidance, see https://github.com/runapi-ai/cli-skill.
- Never shell out to the `runapi` CLI as the production runtime integration layer.

## SDK integration path

When integrating ElevenLabs into an app, backend, worker, library, Rails service, Node service, Go service, webhook pipeline, or production workflow, start by checking the current SDK package and official usage. Confirm install commands, client methods (`create`, `get`, `run`), request fields, response shape, and error classes before using CLI help or raw HTTP examples. Use a RunAPI SDK package:

- JavaScript / TypeScript: `@runapi.ai/elevenlabs`
- Ruby: `runapi-elevenlabs`
- Go: `github.com/runapi-ai/elevenlabs-sdk/go`

## CLI path

The `runapi` binary is the one-off and manual testing runtime dependency. For full CLI-specific agent guidance, see https://github.com/runapi-ai/cli-skill. Run `runapi auth status` first. For agents and headless runs, prefer `RUNAPI_API_KEY` or import it into saved config with `printf '%s' "$RUNAPI_API_KEY" | runapi auth import-token --token -`. Use `runapi login` only when the user explicitly wants interactive browser auth.

Inspect the available commands and request fields with CLI help:

```shell
runapi elevenlabs --help
runapi elevenlabs text-to-speech --help
```

Run a one-off task (synchronous — polls until the task completes):

```shell
runapi elevenlabs text-to-speech --input-file request.json
```

Submit asynchronously and poll separately:

```shell
runapi elevenlabs text-to-speech --async --input-file request.json
runapi wait <task-id> --service elevenlabs --action text-to-speech
```

Available commands: `text-to-speech`, `text-to-dialogue`, `text-to-sound`, `speech-to-text`, `isolate-audio`.

## Generated file storage

RunAPI-generated file URLs are temporary. Download and store generated images, videos, audio, or other files in your own durable storage within 7 days; do not treat returned URLs as long-term assets.

## References

- Model overview, pricing, and rate limits: https://runapi.ai/models/elevenlabs.md
- Provider comparison: https://runapi.ai/providers/elevenlabs.md
- Full model catalog: https://runapi.ai/models.md

## Variants

- [Turbo v2.5 text to speech](https://runapi.ai/models/elevenlabs/text-to-speech-turbo-v2.5.md)
- [Multilingual v2 text to speech](https://runapi.ai/models/elevenlabs/text-to-speech-multilingual-v2.md)
- [Dialogue v3](https://runapi.ai/models/elevenlabs/text-to-dialogue-v3.md)
- [Sound effects v2](https://runapi.ai/models/elevenlabs/sound-effect-v2.md)
- [Speech to text](https://runapi.ai/models/elevenlabs/speech-to-text.md)
- [Audio isolation](https://runapi.ai/models/elevenlabs/audio-isolation.md)

