# Agent Design

Each agent extends a shared `Agent` abstract base class and follows:

1. Think
2. Act
3. Observe
4. Reflect

The `execute()` method orchestrates this loop and appends auditable logs into shared state.

## Roles
- Planner: decomposes topic into task DAG
- Researcher: gathers web findings with credibility heuristics
- Analyst: extracts insights, comparisons, and gaps
- Writer: generates markdown report from analysis
- Critic: scores report and returns revision suggestions
