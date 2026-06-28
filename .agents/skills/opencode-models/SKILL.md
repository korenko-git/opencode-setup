---
name: opencode-models
description: Explain OpenCode models and providers. Invoke when selecting models, setting defaults, configuring provider/model options, using variants, or troubleshooting provider and model resolution.
compatibility: opencode
---

# OpenCode Models

Reference skill for model selection, provider setup, variants, and model-related config in OpenCode.

## When To Use

Use this skill when the task involves:

- choosing a default model,
- selecting a model in the UI or CLI,
- configuring providers or custom providers,
- setting `model` and `small_model` in config,
- tuning provider-specific model options,
- using or defining model variants,
- understanding model load precedence.

## Core Model Concepts

OpenCode supports many LLM providers through AI SDK and Models.dev, including local models.

Common related concepts:

- provider credentials,
- provider config,
- model identifiers,
- default model selection,
- lightweight helper model via `small_model`,
- provider-specific options and variants.

## Selecting A Model

Inside OpenCode, use:

```text
/models
```

This opens model selection after providers and credentials are available.

## Default Model In Config

Set the default model in `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-20250514"
}
```

Model IDs use the format:

```text
provider_id/model_id
```

## Small Model

Use `small_model` for lightweight or cheaper helper work:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-20250514",
  "small_model": "anthropic/claude-3-5-haiku-20241022"
}
```

## Provider Credentials

Popular providers are often preloaded. To add credentials, use provider login flows such as:

```text
opencode auth login
```

If credentials were added successfully, the provider becomes available when OpenCode starts.

## Custom Providers

For an OpenAI-compatible provider not already listed:

1. Run `opencode auth login`
2. Choose `Other`
3. Enter a unique provider ID
4. Add provider config in `opencode.json`

Example:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "myprovider": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "My Provider",
      "options": {
        "baseURL": "https://api.myprovider.com/v1"
      },
      "models": {
        "my-model": {
          "name": "My Model"
        }
      }
    }
  }
}
```

## Provider-Level Model Options

You can configure provider or model-specific options globally:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "openai": {
      "models": {
        "gpt-5": {
          "options": {
            "reasoningEffort": "high",
            "textVerbosity": "low",
            "reasoningSummary": "auto"
          }
        }
      }
    }
  }
}
```

Agent-specific model settings can override global ones when needed.

## Variants

Variants let you define multiple tuned configurations for the same base model.

Example:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "opencode": {
      "models": {
        "gpt-5": {
          "variants": {
            "high": {
              "reasoningEffort": "high",
              "textVerbosity": "low"
            },
            "low": {
              "reasoningEffort": "low",
              "textVerbosity": "low"
            }
          }
        }
      }
    }
  }
}
```

Built-in providers may already ship with default variants such as low or high reasoning modes.

## Model Load Precedence

OpenCode loads models in this order:

1. CLI `--model` or `-m`
2. `model` field in config
3. last used model
4. first available model by internal priority

## CLI And Session Usage

You can override the model at startup:

```bash
opencode --model anthropic/claude-sonnet-4-20250514
```

Or for one-shot execution:

```bash
opencode run --model anthropic/claude-sonnet-4-20250514 "Explain this repo"
```

## Choosing A Good Model Setup

```text
Need best coding and tool use ───────── main `model` should be your strongest coding model
Need cheap helper work ─────────────── set `small_model`
Need multiple speed/quality profiles ─ define variants
Need proxy or custom endpoint ─────── configure a custom provider
Need one-off override ─────────────── use `--model`
```

## Best Practices

1. Keep one strong default coding model for normal sessions.
2. Use `small_model` for cheaper background or helper tasks.
3. Put provider credentials in auth flows, not directly in shared config unless necessary.
4. Use variants instead of duplicating near-identical model entries.
5. Prefer explicit `provider/model` IDs everywhere for clarity.
