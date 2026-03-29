# Compliance Rules

See also:
- [Core Runtime Framework](Core_Runtime_Framework.md)
- [Known Gaps and Risks](Known_Gaps_and_Risks.md)

## Mandatory standards

- Naming conventions match repo terminology.
- Player suit terminology is **rig**, not generic suit.
- No direct gameplay input handling inside actors that should rely on centralized input contexts.
- No hardcoded gameplay tuning that belongs in config.
- All major systems expose debug information.
- Stateful systems must expose save/load integration.
- Data must be schema-driven where defined.
- Tooling code must not be referenced directly from runtime domain code.

## Refactor triggers

Refactor existing code if it:
- duplicates ownership already defined by a subsystem
- bypasses global state or transition coordination
- ignores input context routing
- hardcodes config values
- lacks save hooks for runtime state
- lacks validation or debug visibility
- conflicts with tier, rig, or schema terminology

## Acceptance criteria for 'Master Repo compliant'

A system is compliant when it:
1. Has clear owner subsystem/component.
2. Uses correct state/input/interaction integration.
3. Reads gameplay values from config.
4. Emits logs in the proper category.
5. Exposes debug state.
6. Participates in save/load if stateful.
7. Uses current naming and terminology.
8. Passes repo audit checks.

## Compliance review checklist

- Does it fit ownership rules?
- Does it use the event bus or justified direct dependency?
- Does it respect runtime startup order?
- Does it use the current tier and rig terminology?
- Does it expose enough diagnostics to debug it?
