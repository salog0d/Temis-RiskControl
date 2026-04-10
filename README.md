## Contribution Guidelines

Clear and consistent contributions are required to maintain code quality and development speed.

---

## Pull Requests (PRs)

### Naming Convention

Use the format:

```
Sprint#-ShortDescription
```

Examples:

* `Sprint2-ImplementLogin`
* `Sprint3-AddFraudDetectionRules`

### Rules

* One PR should contain only one feature or fix
* Keep PRs small and easy to review
* Every PR must include:

  * Clear description of the change
  * Context explaining why it is needed
  * Evidence if applicable (screenshots, logs, etc.)

---

## Commits

### Structure (Conventional Commits)

```
<type>(scope): short description
```

### Types

* `feat:` new feature
* `fix:` bug fix
* `docs:` documentation updates
* `chore:` maintenance or dependencies
* `refactor:` internal code improvements
* `test:` tests added or updated

### Examples

```
feat(auth): add login endpoint
fix(api): handle null response in transaction service
docs(readme): update setup instructions
chore(deps): update spring boot version
```

---

## Best Practices

* Commit per logical change, not large batches
* Keep messages concise and explicit
* Avoid vague messages such as:

  * `fix stuff`
  * `update`
* Prefer descriptive messages:

  * `fix(auth): validate JWT expiration`
  * `feat(risk): add anomaly scoring`

---

## Code Quality Expectations

* Follow established architecture and naming conventions
* Ensure code compiles and runs correctly
* Tests must pass when applicable
* Do not introduce breaking changes without prior discussion

---
Agent state machine
<img width="3585" height="629" alt="Untitled-2026-04-10-1345(1)" src="https://github.com/user-attachments/assets/f4af7d5e-4639-46e7-8a2c-b6cbad6a521c" />
Stack diagram
<img width="2751" height="2017" alt="Untitled-2026-04-10-1345(2)" src="https://github.com/user-attachments/assets/c7dee67a-3626-4b46-847c-ca3024b06e33" />
Relational model
<img width="2023" height="1776" alt="Untitled(1)" src="https://github.com/user-attachments/assets/3cc397a9-a04a-4778-b6c6-49ab19f1c932" />


