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
