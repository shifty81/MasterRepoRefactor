# Global State Input Interaction

This is the control spine of the project.

## Core states

- OnFoot
- EVA
- InMech
- InShip
- ToolingMode
- Transitioning

## Core flow

```text
State
 -> choose input context
 -> resolve interactable
 -> perform transition
 -> lock / unlock controls safely
```

## Rule

Only one primary control context at a time.
