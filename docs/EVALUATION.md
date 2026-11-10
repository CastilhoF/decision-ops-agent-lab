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
- After every requested input is supplied, does the tool recalculate from the complete evidence,
  return `analysis_status: revised`, and stop listing the resolved fields as missing?
- Does a revised request remain read-only, leaving a later request without supplements incomplete?

## Agent behavior

- Does the recommendation cite retrieved evidence?
- Does it refuse to claim that a plan was changed?
- Does it ask for human review when the risk is high or evidence is incomplete?
- Does it turn an insufficient-evidence tool result into a clear request for the missing data,
  rather than guessing a recommendation?
- After the user supplies all requested data, does it call the tool again and use the revised
  result rather than repeating the same question?
- Does it avoid a tool that is irrelevant to the question?

Store these as fixtures and regression tests. A model change, prompt change, or tool change should be evaluated against the same cases.
