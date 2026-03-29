# Known Gaps and Risks

See also:
- [Implementation Roadmap](Implementation_Roadmap.md)
- [Core Runtime Framework](Core_Runtime_Framework.md)

## Major remaining gaps

### Character
- Full-body first-person implementation detail
- Injury/survival depth
- Character creator/NPC generation implementation detail

### Mech
- Cockpit UX and HUD
- Detailed movement tuning
- Regional damage and repair depth

### Ship
- Deep ship systems simulation
- Docking and transfer depth
- Crew/seat complexity

### Vehicles
- Rover and hover bike runtime architecture remains mostly open

### EVA
- Exact tether math and hazard consequences
- Collision and movement tuning

### Salvage
- Structural detach logic depth
- Loot scaling and pacing balance

### Derelicts
- Persistence breadth
- Deeper danger layer

### Factions and missions
- Full runtime mission reservation/abandon/failure rules
- Faction consequence depth

### Sectors
- Full simulation cadence and spawn balancing

### Titan and seasonal loop
- Runtime contribution model
- Collapse pacing implementation

### Tooling
- Full validator implementation
- Asset lifecycle/versioning/refactor tooling

### Audio and animation
- Largely open compared to gameplay architecture

## Biggest risk

Building too many systems in parallel before the first vertical slice is stabilized.
