# MasterRepo Security / Authentication / Trust Model

## Purpose
This document locks the security, authentication, and trust architecture for Master Repo so gameplay, voxel edits, module systems, AI actions, tooling, web access, and collaboration all operate under a consistent and enforceable trust model.

---

## 1. Decision summary

### Locked decision
Master Repo will use a **role-based, authority-enforced, audit-driven trust model**.

That means:
- all actions are evaluated through roles and permissions
- authority enforces all trust decisions
- identities are authenticated explicitly
- sensitive actions are auditable
- AI and tooling are treated as actors with bounded permissions
- trust is never implicit based on client or environment alone

This is **not** a trust-by-client model and **not** a minimal security afterthought.

---

## 2. Core principles

1. **Authority enforces truth and trust**
2. **Every action has an actor identity**
3. **Permissions are explicit, not assumed**
4. **High-risk actions require auditability**
5. **AI is not privileged beyond defined roles**
6. **Local does not mean unrestricted**
7. **Security must not block development flow unnecessarily**

---

## 3. Identity model

## 3.1 Actor types
All interactions originate from an actor:

- HumanUser
- LocalOwner (primary machine owner)
- RemoteUser
- Service (internal system)
- AIWorker (Arbiter or other agents)
- Admin/System

## 3.2 Identity components
Each actor identity includes:
- ActorId
- Role(s)
- Authentication state
- SessionId
- Origin (local, remote, web, AI)
- Trust level

---

## 4. Authentication model

## 4.1 Authentication methods
Support:
- local trusted session (dev mode)
- username/password (basic)
- token/session-based auth
- optional API keys for services
- future extensibility (OAuth, etc.)

## 4.2 Local mode rule
Local owner has elevated permissions but still passes through permission checks.

---

## 5. Role-based access control (RBAC)

## 5.1 Core roles

- Observer (read-only)
- Player (gameplay actions)
- Builder (construction/editing)
- Reviewer (inspect/comment)
- Operator (tool execution)
- Admin (full control)
- LocalOwner (highest local trust)
- AIWorker (bounded automation)

## 5.2 Permission examples

| Action | Required Role |
|------|--------|
| Move player | Player |
| Place module | Builder |
| Edit structure | Builder |
| Run debug tools | Operator |
| Modify save data | Admin |
| Approve AI patch | Admin / Operator |
| View only | Observer |

---

## 6. Permission system

## 6.1 Permission checks
All mutation requests must pass:
- identity verification
- role check
- context check
- authority validation

## 6.2 Context-aware permissions
Permissions may vary based on:
- location (structure, region)
- ownership (player-owned vs shared)
- session type
- active mode (gameplay vs tooling)

---

## 7. Trust levels

Define trust tiers:

- Trusted (local owner)
- Verified (authenticated user)
- Limited (guest or restricted)
- Automated (AIWorker)
- System (internal)

Each level restricts capabilities accordingly.

---

## 8. AI trust model

## 8.1 AI as bounded actor
AI operates under:
- AIWorker role
- explicit permissions
- audit logging

## 8.2 AI limitations
AI cannot:
- bypass authority
- modify critical systems without approval
- perform destructive actions silently

---

## 9. Audit system

## 9.1 Audit requirements
Log:
- actor identity
- action performed
- timestamp
- target system/object
- result (success/failure)
- approval state if applicable

## 9.2 Critical actions
Require logging:
- save/load
- structure edits
- voxel edits
- permission changes
- AI actions
- admin operations

---

## 10. Secure communication

## 10.1 Network communication
- use secure channels (TLS-ready design)
- validate all incoming messages
- reject malformed or unauthorized requests

---

## 11. Data protection

## 11.1 Sensitive data
Protect:
- player data
- credentials
- session tokens
- admin actions
- AI logs where needed

## 11.2 Local storage
- avoid plain-text secrets where possible
- separate config vs secure data

---

## 12. Web server integration

## 12.1 Web access rules
- must authenticate
- role-based UI exposure
- limited surface for non-admin users
- sandboxed operations

---

## 13. Session management

## 13.1 Session lifecycle
- create session
- authenticate
- assign role
- track activity
- expire/terminate safely

---

## 14. Security vs usability balance

## 14.1 Development mode
- relaxed auth options
- logging still enabled
- warnings instead of hard blocks where safe

## 14.2 Production mode
- strict enforcement
- no bypass paths
- full audit

---

## 15. Failure handling

## 15.1 On auth failure
- deny request
- log attempt
- optionally notify admin

## 15.2 On permission failure
- deny action
- return clear error
- log event

---

## 16. Core interfaces

- AuthManager
- RoleManager
- PermissionService
- AuditLogger
- SessionManager
- SecurityContext

---

## 17. Hard rules

1. No action without identity
2. No mutation without permission
3. Authority validates all
4. AI is never unrestricted
5. All critical actions are logged
6. Local mode still respects system rules

---

## 18. Final outcome

Master Repo security architecture is:

**role-based, authority-enforced, auditable, and AI-aware**

This ensures:
- safe collaboration
- controlled AI integration
- secure web/tool access
- scalable multiplayer trust model
