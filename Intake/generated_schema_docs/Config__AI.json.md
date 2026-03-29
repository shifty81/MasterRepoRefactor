# Schema Reference: `Config/AI.json`

| Path | Type | Sample |
|---|---|---|
| `$` | `object` | `object (11)` |
| `enabled` | `bool` | `True` |
| `offline` | `bool` | `True` |
| `modelProvider` | `string` | `'ollama'` |
| `defaultModel` | `string` | `'deepseek-coder'` |
| `models` | `object` | `object (3)` |
| `models.code` | `string` | `'deepseek-coder'` |
| `models.chat` | `string` | `'llama3'` |
| `models.embedding` | `string` | `'nomic-embed-text'` |
| `sessionTimeout` | `int` | `3600` |
| `maxTokens` | `int` | `4096` |
| `temperature` | `float` | `0.7` |
| `sandbox` | `bool` | `True` |
| `allowedPaths` | `array` | `array (3)` |
| `allowedPaths[]` | `string` | `'Projects/'` |
| `memory` | `object` | `object (3)` |
| `memory.enabled` | `bool` | `True` |
| `memory.maxEntries` | `int` | `10000` |
| `memory.embeddingDimension` | `int` | `384` |
