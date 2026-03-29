# Schema Reference: `Config/Engine.json`

| Path | Type | Sample |
|---|---|---|
| `$` | `object` | `object (4)` |
| `window` | `object` | `object (5)` |
| `window.title` | `string` | `'MasterRepo Engine'` |
| `window.width` | `int` | `1920` |
| `window.height` | `int` | `1080` |
| `window.fullscreen` | `bool` | `False` |
| `window.vsync` | `bool` | `True` |
| `renderer` | `object` | `object (4)` |
| `renderer.backend` | `string` | `'OpenGL'` |
| `renderer.msaa` | `int` | `4` |
| `renderer.shadows` | `bool` | `True` |
| `renderer.maxFPS` | `int` | `60` |
| `physics` | `object` | `object (3)` |
| `physics.backend` | `string` | `'Bullet'` |
| `physics.gravity` | `array` | `array (3)` |
| `physics.gravity[]` | `int` | `0` |
| `physics.fixedTimestep` | `float` | `0.016667` |
| `audio` | `object` | `object (2)` |
| `audio.backend` | `string` | `'OpenAL'` |
| `audio.masterVolume` | `float` | `1.0` |
