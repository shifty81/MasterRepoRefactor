# Schema Reference: `CMakePresets.json`

| Path | Type | Sample |
|---|---|---|
| `$` | `object` | `object (5)` |
| `version` | `int` | `3` |
| `cmakeMinimumRequired` | `object` | `object (3)` |
| `cmakeMinimumRequired.major` | `int` | `3` |
| `cmakeMinimumRequired.minor` | `int` | `20` |
| `cmakeMinimumRequired.patch` | `int` | `0` |
| `configurePresets` | `array` | `array (8)` |
| `configurePresets[]` | `object` | `object (5)` |
| `configurePresets[].name` | `string` | `'base'` |
| `configurePresets[].hidden` | `bool` | `True` |
| `configurePresets[].binaryDir` | `string` | `'${sourceDir}/Builds/${presetName}'` |
| `configurePresets[].installDir` | `string` | `'${sourceDir}/Builds/${presetName}/install'` |
| `configurePresets[].cacheVariables` | `object` | `object (1)` |
| `configurePresets[].cacheVariables.CMAKE_EXPORT_COMPILE_COMMANDS` | `string` | `'ON'` |
| `buildPresets` | `array` | `array (6)` |
| `buildPresets[]` | `object` | `object (3)` |
| `buildPresets[].name` | `string` | `'debug'` |
| `buildPresets[].configurePreset` | `string` | `'debug'` |
| `buildPresets[].jobs` | `int` | `0` |
| `testPresets` | `array` | `array (2)` |
| `testPresets[]` | `object` | `object (4)` |
| `testPresets[].name` | `string` | `'debug'` |
| `testPresets[].configurePreset` | `string` | `'debug'` |
| `testPresets[].output` | `object` | `object (1)` |
| `testPresets[].output.outputOnFailure` | `bool` | `True` |
| `testPresets[].execution` | `object` | `object (1)` |
| `testPresets[].execution.jobs` | `int` | `4` |
