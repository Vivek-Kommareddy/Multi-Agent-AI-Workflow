# Architecture

The project is organized around four subsystems: agents, tools, orchestrator, and APIs/UI.

- **Dependency Injection**: `Router` composes agents with tool dependencies.
- **Factory Pattern**: `llm/provider.py` exposes provider creation.
- **Strategy Pattern**: agents choose tools through `act()` based on task context.
- **Observer Pattern**: `Workflow` emits events consumed by API/WebSocket clients.

All agent communication flows through `SharedState` for auditability.
