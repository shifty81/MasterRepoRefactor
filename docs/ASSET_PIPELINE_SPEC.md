# ASSET_PIPELINE_SPEC.md

## Purpose

This document defines the asset pipeline for the consolidated **MasterRepo** architecture, with:

- **Atlas** as the native engine/runtime/editor backend
- **AtlasAI** as the WPF tooling/orchestration layer
- **NovaForge** as the primary game/content layer

The asset pipeline must support:

- deterministic asset import and rebuild
- editor-time authoring and validation
- runtime-safe cooked asset consumption
- cache reuse and incremental rebuilds
- dependency tracking
- hot reload where safe
- service-based operation for WPF tooling
- future automation support from AtlasAI

---

# 1. Core Principles

## 1.1 Source vs Derived separation

Every asset exists in one of these forms:

- **Source Asset**  
  Human-authored original input such as:
  - meshes
  - textures
  - sounds
  - voxel source data
  - materials
  - prefabs
  - mission definitions
  - dialogue files
  - balance tables

- **Imported Intermediate**  
  Normalized engine-facing representation created by importers.

- **Cooked Runtime Asset**  
  Final runtime-ready representation for Atlas.

- **Cache / Build Artifact**  
  Temporary or reusable outputs used to accelerate rebuilds.

The source asset is never treated as the runtime format.

---

## 1.2 Asset identity is GUID-based

Every asset must have a stable **Asset GUID** that survives file moves and renames.

Human-readable paths are not identity.

### Asset identity components
- `AssetGuid`
- source path
- asset type
- importer version
- source hash
- dependency hashes
- cook profile / target profile
- produced artifact hashes

---

## 1.3 Pipeline stages are deterministic

Given the same:
- source content
- importer version
- dependency graph
- platform profile
- cook settings

the pipeline should produce the same result.

This matters for:
- debugging
- multiplayer consistency
- cache validity
- CI reproducibility

---

## 1.4 Import and cook are separate concepts

### Import
Turns source files into Atlas-understandable structured asset data.

### Cook
Turns imported data into optimized runtime-ready data for a target.

This separation is required so:
- editor tooling can inspect normalized imported data
- runtime builds can optimize differently by target
- invalidation stays precise

---

## 1.5 WPF tooling is a client, not the pipeline owner

AtlasAI WPF tools may:
- trigger import
- preview status
- inspect metadata
- request recook
- show dependency graphs

They do not directly implement the core import/cook logic.

The pipeline is owned by:
- `AtlasAssetService`
- native asset pipeline modules
- shared asset contracts

---

# 2. High-Level Asset Lifecycle

```text
Source Asset
    ↓
Discovery
    ↓
Registration
    ↓
Import
    ↓
Validation
    ↓
Intermediate Representation
    ↓
Dependency Resolution
    ↓
Cook / Bake
    ↓
Runtime Package / Cache Output
    ↓
Asset Registry Update
    ↓
Editor Preview / Runtime Load
```

---

# 3. Pipeline Stages

## 3.1 Discovery

The pipeline scans configured content roots for source assets.

### Content roots
- `/Content`
- approved plugin content roots
- optional external workspace-linked content roots

### Discovery responsibilities
- find new files
- find deleted files
- find moved/renamed files
- detect type by extension and rules
- map path to asset registration rules

### Output
Discovered source asset entries.

---

## 3.2 Registration

Registration creates or updates the authoritative asset record.

### Registration record contains
- Asset GUID
- canonical source path
- asset type
- importer type
- source timestamp
- source content hash
- dependency references
- labels / tags
- ownership namespace
- package grouping
- status flags

### Rules
- asset GUID must survive rename/move
- registration must not require full import unless content changed
- deleted assets must be tombstoned until cleanup pass confirms removal

---

## 3.3 Import

The importer parses source files into engine-normalized intermediate data.

### Examples
- texture file → normalized texture descriptor + pixel payload
- mesh file → normalized mesh topology and material slots
- material definition → shader graph/material instance data
- voxel source → chunked voxel data + metadata
- mission JSON/YAML → validated mission graph
- prefab → entity/component authoring description
- dialogue file → conversation nodes + localization bindings

### Import responsibilities
- syntax parsing
- semantic normalization
- schema upgrade where possible
- default-value filling
- source-level validation
- metadata generation
- importer diagnostics

### Import must not
- perform runtime-only platform compression unless part of a downstream cook step
- depend on WPF UI
- write directly into runtime memory formats without an intermediate form

---

## 3.4 Validation

Validation occurs at multiple levels.

### Validation levels
- syntax validation
- schema validation
- semantic validation
- dependency validation
- policy validation
- performance-budget validation
- project rule validation

### Examples
- missing texture reference
- invalid material parameter
- prefab circular dependency
- mission reward table mismatch
- voxel chunk size policy violation
- unsupported shader feature for target
- interior prefab missing nav markers

Validation results must be first-class data visible in tooling.

---

## 3.5 Dependency resolution

Every asset declares or discovers dependencies.

### Dependency classes
- **Hard dependency**: required for asset correctness
- **Soft dependency**: optional or lazy-resolved
- **Build dependency**: required to produce cooked output
- **Editor dependency**: needed for preview/authoring but not runtime
- **Runtime dependency**: needed by runtime loader

### Dependency examples
- material depends on textures and shader definitions
- prefab depends on mesh, material, collision, script data
- station archetype depends on modular pieces and economy tables
- planet biome definition depends on texture sets and generation rules

The graph must support:
- reverse lookup
- change invalidation
- build ordering
- dependency visualization in AtlasAI tooling

---

## 3.6 Cook / Bake

Cook transforms imported data into runtime-target outputs.

### Cook targets
- editor preview
- debug runtime
- release runtime
- dedicated server
- headless simulation
- test harness targets

### Cook operations may include
- compression
- transcoding
- mesh optimization
- LOD generation
- collision bake
- nav data bake
- texture mip generation
- shader variant generation
- voxel streaming chunk bake
- prefab flattening
- mission graph indexing
- localization table bake

### Cook outputs
- target-specific runtime blobs
- metadata manifests
- lookup tables
- content package entries
- streaming chunk fragments

---

## 3.7 Packaging / cache output

Cooked outputs are stored in a build cache and optionally packaged.

### Cache requirements
- content-addressable where practical
- invalidation by precise hash/version changes
- fast existence lookup
- safe cleanup policy
- separate editor preview cache from release package cache where useful

### Packaging requirements
- group by logical content packages
- allow partial rebuilds
- allow streaming-friendly package layout
- support dedicated server exclusion of client-only assets

---

## 3.8 Registry update

The asset registry is updated after successful import/cook.

### Registry stores
- asset identity
- type
- source info
- dependency graph
- import state
- validation state
- cooked target availability
- package membership
- version data
- preview availability
- editor annotations

The registry is the source of truth for:
- editor browsing
- dependency graphing
- runtime lookup indirection
- hot reload planning
- CI validation

---

# 4. Asset Classes

## 4.1 Core runtime asset classes
- textures
- materials
- meshes
- skeletons
- animations
- sounds
- music
- VFX descriptors
- fonts
- UI runtime assets

## 4.2 World and gameplay asset classes
- prefabs
- entity archetypes
- ship modules
- station modules
- interior room modules
- mission templates
- encounter definitions
- faction data references
- economy templates
- crafting definitions
- loot tables
- progression data bundles

## 4.3 Voxel / world-generation asset classes
- voxel palettes
- material layers
- terrain rules
- biome definitions
- planet generation profiles
- asteroid generation profiles
- ruin generation kits
- chunk templates
- destruction profiles

## 4.4 Tooling / editor-facing asset classes
- design graph files
- workspace layouts
- editor presets
- validation profiles
- asset import presets
- preview scenes

---

# 5. Directory Strategy

## 5.1 Source locations

Primary source content should live in:
- `/Content`
- `/Data`
- `/Config` for non-asset config-like data where appropriate

### Suggested layout
```text
/Content
    /Prefabs
    /Ships
    /Stations
    /Interiors
    /Characters
    /Props
    /Planets
    /Biomes
    /Templates
    /Dialogue
    /Missions
    /Audio
    /VFX
    /Textures
    /Materials
    /Meshes

/Data
    /Balance
    /Factions
    /Economy
    /Rules
    /Loot
    /Crafting
    /Progression
    /Encounters
```

---

## 5.2 Generated locations

Generated outputs should not be mixed with authored sources.

### Suggested generated locations
```text
/Build/AssetCache
/Build/Cooked
/Build/DerivedData
/Build/PackageStaging
```

Optional local-only developer caches may live outside repo.

---

# 6. Asset Registry Design

## 6.1 Registry responsibilities
The asset registry must answer:

- what assets exist
- what type they are
- what they depend on
- what depends on them
- whether they are valid
- whether they are cooked for a target
- where their cooked outputs live
- whether they support hot reload
- what importer produced them
- what versions/hashes produced current outputs

---

## 6.2 Minimum registry fields

- `AssetGuid`
- `CanonicalPath`
- `DisplayName`
- `AssetType`
- `ImporterId`
- `ImporterVersion`
- `SourceHash`
- `SchemaVersion`
- `ValidationStatus`
- `DependencyList`
- `ReverseDependencyList`
- `CookedTargets`
- `LastImportTime`
- `LastCookTime`
- `PackageGroup`
- `HotReloadPolicy`
- `OwnershipArea`

---

# 7. Importers

## 7.1 Importer contract

Every importer must define:
- supported extensions / source types
- importer version
- import settings schema
- validation rules
- output intermediate type
- dependency discovery rules
- hot reload support class

### Importer interface conceptually
```text
CanImport(source)
Import(source, settings, context) -> IntermediateAsset
Validate(intermediate, context) -> Diagnostics
DiscoverDependencies(intermediate) -> DependencyList
```

---

## 7.2 Importer versioning

Importer version must be part of cache invalidation.

If importer logic changes:
- dependent assets may require reimport
- cooked outputs become stale
- validation may need rerun

---

## 7.3 Import presets

Common presets should be supported for:
- textures
- materials
- collision generation
- LOD generation
- voxel import
- prefab import
- dialogue validation strictness

Presets must be stored as data, not hardcoded UI assumptions.

---

# 8. Cook Profiles

## 8.1 Profile examples
- `EditorPreview`
- `DebugClient`
- `ReleaseClient`
- `DedicatedServer`
- `HeadlessSimulation`
- `AutomatedTest`

## 8.2 Profile-specific behavior

### EditorPreview
- fast turnaround
- less aggressive optimization
- rich metadata retained
- preview thumbnails and diagnostics allowed

### ReleaseClient
- aggressive compression
- stripped editor-only metadata
- streaming layout optimized
- package integrity hardened

### DedicatedServer
- exclude client-only rendering/audio assets when possible
- keep simulation-relevant data
- strip preview payloads

---

# 9. Invalidation Rules

## 9.1 Reimport triggers
Reimport is required when:
- source hash changes
- importer version changes
- schema version changes
- import settings change
- importer-discovered dependency structure changes

## 9.2 Recook triggers
Recook is required when:
- imported intermediate changes
- cook profile changes
- cook tool version changes
- build dependency changes
- target platform rules change

## 9.3 Reverse invalidation
When a dependency changes:
- dependents are marked stale
- stale reason is recorded
- WPF tooling may display affected asset list

---

# 10. Hot Reload Rules

## 10.1 Hot reload categories

### Safe hot reload
- textures
- materials with compatible parameter layout
- some audio
- data tables
- mission tuning
- loot tables
- dialogue text
- balance values

### Conditional hot reload
- meshes
- prefabs
- entity archetypes
- shader variants
- some voxel chunks

### Unsafe / restart-required
- schema-breaking prefab changes
- incompatible skeleton changes
- save-format-critical data shape changes
- deep runtime layout changes

Hot reload policy must be declared per asset class.

---

## 10.2 Editor/live preview policy
Editor preview reloads may happen more aggressively than runtime live reloads.

Simulation integrity always wins over convenience.

---

# 11. Runtime Loading Model

## 11.1 Runtime loaders consume cooked assets only

Runtime systems should never load arbitrary source authoring formats directly in production paths.

### Runtime asset access flow
```text
Runtime system
    ↓
Asset handle / GUID reference
    ↓
Asset registry or package manifest lookup
    ↓
Cooked package / cache blob
    ↓
Runtime loader
    ↓
Runtime object/material/mesh/data instance
```

---

## 11.2 Asset handles

Code should prefer:
- GUID-backed handles
- typed runtime handles
- late-binding lookup through registry/package system

Avoid:
- raw source paths in gameplay systems
- direct filesystem assumptions inside runtime logic

---

# 12. AtlasAI and WPF Tooling Integration

## 12.1 WPF tooling capabilities
AtlasAI tooling should be able to:
- browse asset registry
- inspect metadata
- view dependency graphs
- preview validation issues
- trigger import/reimport/recook
- show stale assets
- batch-fix naming/organization issues where safe
- surface asset diagnostics from services

## 12.2 AtlasAI automation capabilities
AtlasAI may:
- suggest asset grouping changes
- detect orphaned assets
- propose dependency cleanup
- identify large rebuild hotspots
- recommend import preset changes
- find repeated validation failures

AtlasAI must not:
- directly mutate cooked outputs
- bypass asset service validation
- invent asset metadata outside defined schemas

---

# 13. Asset Service Responsibilities

`AtlasAssetService` owns the service-facing asset workflow.

## Responsibilities
- discovery orchestration
- import job scheduling
- cook job scheduling
- dependency graph updates
- registry updates
- diagnostics aggregation
- preview request handling
- cache cleanup policies
- build integration hooks

## Must expose
- asset query API
- validation query API
- import/reimport commands
- cook commands
- dependency graph API
- preview readiness API
- stale asset reporting
- progress events

---

# 14. Preview System

## 14.1 Preview types
- thumbnail previews
- mesh previews
- material previews
- prefab previews
- voxel previews
- audio preview metadata
- mission graph previews
- dialogue graph previews

## 14.2 Preview rules
Previews should be generated from imported data or preview cooks, not from arbitrary ad hoc UI code.

This keeps preview results consistent.

---

# 15. Versioning Strategy

Asset versioning must include:

- schema version
- importer version
- cook tool version
- package format version
- runtime loader compatibility version

Versioning exists to support:
- migration
- targeted rebuilds
- backward compatibility decisions
- detection of stale outputs

---

# 16. Failure and Recovery Strategy

## 16.1 Import failure
If import fails:
- previous valid cooked output may remain marked as last known good
- asset status becomes invalid/stale
- diagnostics are recorded
- dependents are warned

## 16.2 Partial cook failure
If one target cook fails:
- other target outputs remain valid if unaffected
- failed target marked unavailable
- diagnostics include target profile context

## 16.3 Registry integrity
Registry updates should be transactional where possible.

Do not leave half-written registry state as the authoritative record.

---

# 17. CI / Build Farm Considerations

The pipeline must support:
- headless import/cook
- deterministic rebuild checks
- stale asset detection in CI
- package integrity validation
- content linting
- size regression tracking
- asset dependency cycle detection

---

# 18. Performance Requirements

The pipeline must optimize for:
- fast no-op scans
- incremental rebuilds
- content-addressable reuse where practical
- parallel import/cook execution
- dependency-aware scheduling
- minimal editor stall time

Avoid a design where every small content change forces broad recooks.

---

# 19. Recommended Initial Implementation Order

1. Asset GUID + registry
2. basic discovery and registration
3. importer contracts
4. validation framework
5. dependency graph
6. cook profile framework
7. asset service APIs
8. preview generation
9. hot reload rules
10. cache cleanup and CI validation

---

# 20. Bottom Line

The Atlas asset pipeline should be:

- GUID-based
- deterministic
- service-driven
- cache-aware
- dependency-aware
- WPF-consumable
- runtime-safe
- editor-friendly
- ready for AtlasAI automation

That gives MasterRepo a content foundation strong enough to support Atlas, AtlasAI, and NovaForge without asset chaos.
