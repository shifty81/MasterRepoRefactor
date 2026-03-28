# BUILDER + SALVAGE SMOKE TEST

## Goal
Verify the builder and salvage chain in one Dev World session.

## Test sequence

### 1. Start Atlas Suite
- Open NovaForge
- Launch Dev World

### 2. Spawn test construct
- Ensure `dev_builder_salvage_construct` loads
- Verify at least one starter hull part is present

### 3. Enter builder mode
- Open Builder Debug panel
- Select `hull_plate_mk1_a`
- Enable ghost placement preview

### 4. Place part
- Preview valid snap point
- Confirm placement
- Verify state = `placed_unwelded`

### 5. Validate construct
- Run validation pass
- Verify response returns at least `structure`, `mount`, and `clearance`

### 6. Weld/finalize
- Finalize placed part
- Verify state = `welded`
- Verify construct delta updated

### 7. Apply damage
- Use debug damage action on finalized part
- Verify durability decreases
- Verify part can enter `damaged` state

### 8. Mark for salvage
- Open Salvage Debug panel
- Mark damaged part as salvage target
- Verify salvage state recorded

### 9. Cut/detach
- Execute detach action
- Verify part removed from active placement graph
- Verify salvage recovery record created

### 10. Recover output
- Verify one or more recovery outputs created
- Route output to test loot container
- Verify container manifest updated

### 11. Save/reload
- Save Dev World state
- Reload Dev World state
- Confirm finalized placements and salvage deltas persist safely

## Pass criteria
- Placement preview works
- Placement state changes are correct
- Validation is callable
- Welding commits builder state
- Damage affects part state
- Salvage mark/cut/detach completes without crash
- Recovery outputs are created deterministically
- Save/reload preserves builder and salvage data
