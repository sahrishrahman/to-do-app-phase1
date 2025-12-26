# Evolution of Todo - Project Constitution

This constitution governs all development for the "Evolution of Todo" project across all five phases. It is the supreme governing document and takes precedence over all other project documentation.

## Core Principles

### I. Spec-Driven Development (MANDATORY)

All work MUST follow the mandated development order:

1. **Constitution** → The supreme authority governing all decisions
2. **Specifications** → Detailed feature requirements approved by humans
3. **Plan** → Technical architecture and approach derived from specs
4. **Tasks** → Atomic, testable implementation steps derived from plans
5. **Implementation** → Code written only to fulfill approved tasks

**Non-Negotiable Rules:**
- No agent may write code without approved specifications and tasks
- No agent may deviate from approved specifications
- Refinements MUST occur at the spec level, never at the code level
- If implementation reveals issues, the agent MUST request spec updates, not self-correct

### II. Human-Authorship Prohibition

Agents MUST NOT write code that will be committed to the repository. This prohibition includes:
- No manual coding by human operators
- No direct agent code generation for production code
- All code must emerge from the Spec → Plan → Tasks → Implementation flow with human approval at each stage

**Rationale:** This ensures human oversight, prevents agent hallucination, and maintains architectural integrity.

### III. No Feature Invention

Agents operate within strict boundaries:
- Features MUST be derived exclusively from approved specifications
- No inventing APIs, data structures, or behaviors not in the specs
- No "improvements" or "optimizations" not explicitly requested
- Scope creep MUST be flagged and approved by humans

**When in doubt:** Ask for clarification rather than assume.

### IV. Phase Isolation

Each phase is strictly scoped by its specification:
- Phase I features MUST NOT include Phase II-V capabilities
- Future-phase technologies MUST NOT be introduced early
- Architecture may only evolve through updated specs and plans
- Technical debt from earlier phases MUST be addressed within that phase's scope

**Phase Boundaries:**
- **Phase I**: Python/FastAPI backend with basic todo operations
- **Phase II**: Next.js frontend integration, user interface
- **Phase III**: AI agent integration, intelligent features
- **Phase IV**: Distributed architecture, messaging, scaling
- **Phase V**: Advanced orchestration, full automation

### V. Refinement at Spec Level

When implementation reveals gaps or issues:
1. Document the issue clearly
2. Propose spec-level changes
3. Await human approval before proceeding
4. Never silently adapt code to compensate for incomplete specs

**Rationale:** Maintaining spec integrity ensures the project roadmap remains visible and controllable.

## Technology Stack

### Backend (Phases I-III)
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon (PostgreSQL)
- **AI Integration**: OpenAI Agents SDK, MCP (Model Context Protocol)

### Frontend (Phases II+)
- **Framework**: Next.js
- **Language**: TypeScript
- **Styling**: Tailwind CSS (or project-standard)

### Infrastructure (Phases IV-V)
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **Messaging**: Kafka
- **Distributed Primitives**: Dapr

### Development Tools
- **Version Control**: Git
- **Testing**: pytest (backend), appropriate frontend framework
- **Linting/Formatting**: Project-standard tools

## Quality Principles

### A. Clean Architecture
- Clear separation of concerns
- Dependencies point inward (domain depends on nothing, infrastructure depends on domain)
- Business logic isolated from framework and delivery mechanisms
- Each component has a single, well-defined responsibility

### B. Stateless Services
- Services MUST be stateless where required for horizontal scaling
- State MUST be persisted to appropriate storage (database, cache)
- No in-memory state that prevents load balancing
- Session state handled via tokens or external storage

### C. Separation of Concerns
- API layer handles HTTP concerns only
- Service layer handles business logic only
- Data layer handles persistence only
- No layer knows about implementation details of other layers

### D. Cloud-Native Readiness
- Configuration via environment variables
- No hardcoded credentials or endpoints
- Health check endpoints for orchestration
- Graceful degradation patterns
- Observable metrics and logging

### E. API Design
- RESTful principles for HTTP APIs
- Clear contract (OpenAPI specification)
- Versioned APIs for breaking changes
- Idempotent operations where appropriate
- Proper HTTP status codes and error responses

## Development Workflow

### Phase Gates

Each phase MUST complete these gates before proceeding:

1. **Specification Gate**: All features documented and approved
2. **Plan Gate**: Technical approach reviewed and approved
3. **Tasks Gate**: Implementation tasks breakdown approved
4. **Implementation Gate**: Code written, tested, reviewed
5. **Acceptance Gate**: Human verification of functionality

### Specification Requirements

Every feature specification MUST include:
- User stories with clear acceptance criteria
- Functional requirements (MUST/SHOULD verbs)
- Non-functional requirements (performance, security, scale)
- Edge cases and error conditions
- Success metrics

### Plan Requirements

Every implementation plan MUST include:
- Technical context (languages, dependencies, storage)
- Constitution compliance verification
- Project structure definition
- Complexity tracking (deviations from principles must be justified)

### Task Requirements

Every task MUST be:
- Atomic (single responsibility)
- Testable (can verify completion independently)
- Sized (can be completed in reasonable time)
- Traceable (linked to specification requirement)

## Governance

### Constitution Supremacy
This constitution supersedes all other project documentation. In case of conflict, this document takes precedence.

### Amendment Process
Amendments require:
1. Documentation of proposed change
2. Rationale for change
3. Impact assessment on existing phases
4. Human approval
5. Version increment following semantic versioning

### Versioning
- **MAJOR**: Backward-incompatible governance changes
- **MINOR**: New principles, expanded guidance
- **PATCH**: Clarifications, wording, typo fixes

### Compliance
- All PRs/reviews MUST verify constitution compliance
- Complexity deviations MUST be documented and justified
- Template files MUST remain synchronized with constitution

## Version Information

**Version**: 1.0.0
**Ratified**: 2025-12-25
**Last Amended**: 2025-12-25
