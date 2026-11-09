# Evaluation plan

Evaluate each layer independently before evaluating an end-to-end agent.

## Retrieval

- Does a question about approval return the approval-policy chunk?
- Are returned source paths stable and visible to the caller?
- Does an unrelated query avoid claiming a strong match?

## Tools

- Does each period produce the expected deterministic risk calculation?
- Do invalid periods return a typed error?
- Are tools read-only?
- When the playbook is available but an operational input is missing, does the tool return
  `evidence_status: insufficient`, name the missing inputs, and avoid assigning a risk level?

## Agent behavior

- Does the recommendation cite retrieved evidence?
- Does it refuse to claim that a plan was changed?
- Does it ask for human review when the risk is high or evidence is incomplete?
- Does it turn an insufficient-evidence tool result into a clear request for the missing data,
  rather than guessing a recommendation?
- Does it avoid a tool that is irrelevant to the question?

Store these as fixtures and regression tests. A model change, prompt change, or tool change should be evaluated against the same cases.
