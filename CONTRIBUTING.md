# Contributing to AI Lead Qualification Engine

Thanks for your interest in contributing to **AI Lead Qualification Engine**.

This project is a reference implementation for building transparent and testable AI-assisted lead qualification systems using:

- structured lead input
- deterministic qualification rules
- configurable scoring
- human-review fallback
- FastAPI
- automated testing

---

## Development Setup

Clone the repository:

```bash
git clone https://github.com/prashant6788/ai-lead-qualification-engine.git
cd ai-lead-qualification-engine
```

Create a virtual environment.

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## Run the Application

Start the FastAPI development server:

```bash
python -m uvicorn app.main:app --reload
```

Open the interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

Available endpoints include:

```text
GET  /health
POST /qualify
```

---

## Testing

Run all tests before submitting changes:

```bash
python -m pytest -q
```

The project includes tests for:

- qualification logic
- ambiguous leads
- human-review scenarios
- commercial exceptions
- API health endpoint
- qualification API endpoint
- invalid API input

Please add or update tests whenever qualification behavior changes.

---

## What Contributions Are Welcome?

Useful contributions include:

- additional qualification test cases
- input-validation improvements
- human-review patterns
- clearer configuration handling
- API improvements
- documentation improvements
- optional AI-provider integrations
- security improvements
- logging and observability improvements
- edge-case handling
- additional example payloads

---

## Design Principles

Please keep contributions aligned with the core architecture.

### 1. Separate Interpretation From Business Policy

The interpretation layer may extract information from unstructured input.

Qualification policy should remain explicit and testable.

```text
Interpretation
↓
Structured Data
↓
Business Rules
↓
Qualification
↓
Human Review if Required
```

### 2. Do Not Invent Missing Lead Data

If budget, location, timeline or another field is unavailable, keep it unknown rather than generating a value.

### 3. Prefer Structured Outputs

New interpretation providers should return predictable structured data that can be validated before downstream processing.

### 4. Keep Rules Configurable

Where practical, business rules should remain in:

```text
config/qualification-rules.json
```

rather than being scattered throughout application code.

### 5. Preserve Human Review

Do not remove human-review paths simply to increase automation.

Ambiguous, unsupported, sensitive or exceptional cases should remain recoverable by a human.

### 6. Keep the Core Engine Provider-Neutral

External AI providers may be added as optional interpretation layers, but the qualification engine should not depend on one specific provider.

---

## Code Style

Keep code:

- clear
- readable
- focused
- testable
- documented where behavior is not obvious

Prefer small, understandable changes over large rewrites.

When modifying qualification logic, update or add tests that demonstrate the intended behavior.

---

## Security

Never commit:

- API keys
- passwords
- access tokens
- private keys
- webhook secrets
- CRM credentials
- production customer data

Use environment variables for secrets.

The repository provides:

```text
.env.example
```

Real `.env` files must remain outside version control.

---

## Customer Data

Do not use real customer information in examples or tests.

Use fictional or safely sanitized data.

Avoid committing:

- real names
- phone numbers
- email addresses
- CRM exports
- conversation transcripts
- payment information
- confidential business information
- internal customer notes

---

## External AI Providers

External LLM integrations are welcome as optional provider implementations.

They should:

- keep credentials outside source control
- return structured output
- validate model responses
- preserve deterministic qualification rules
- maintain human-review fallback
- avoid making uncontrolled commercial decisions
- avoid inventing missing customer information

A provider integration should preserve the same general flow:

```text
Lead
↓
Interpretation Provider
↓
Structured Extraction
↓
Validation
↓
Qualification Rules
↓
Decision
↓
Human Review if Required
```

---

## Configuration Changes

If you change:

```text
config/qualification-rules.json
```

please make sure the change is:

- documented
- covered by tests
- clearly explained in the pull request

Default scoring values in this repository are illustrative examples, not universal lead-scoring benchmarks.

---

## Code Changes

Keep pull requests focused.

Prefer:

```text
One improvement
+
Relevant tests
+
Relevant documentation changes
```

Avoid combining multiple unrelated architectural changes in one pull request.

---

## Pull Request Checklist

Before submitting a pull request:

- [ ] Application runs locally
- [ ] Existing tests pass
- [ ] New behavior has tests
- [ ] No secrets are included
- [ ] No real customer data is included
- [ ] Qualification rules remain understandable
- [ ] Human-review behavior is preserved where required
- [ ] Documentation is updated if behavior changes
- [ ] Configuration changes are explained
- [ ] The pull request has a focused scope

---

## Commit Messages

Use clear commit messages.

Examples:

```text
Add API validation tests
Improve service classification
Add human-review edge case
Update qualification documentation
Add optional AI provider interface
```

Avoid vague commit messages such as:

```text
update
changes
fix stuff
final
```

---

## Reporting Issues

When reporting a problem, include:

- what you expected
- what happened
- steps to reproduce
- Python version
- relevant error output

Do not include credentials or private customer data.

---

## Feature Requests

Feature requests are welcome when they improve the reference implementation without making the core unnecessarily complex.

Good examples include:

- additional provider adapters
- stronger validation
- better error handling
- audit logging
- configurable qualification profiles
- observability
- CRM integration examples

Large production features may be better implemented as separate extensions rather than being added directly to the core engine.

---

## Documentation Contributions

Documentation improvements are welcome.

Useful improvements include:

- clearer setup instructions
- additional API examples
- architecture explanations
- troubleshooting guidance
- test documentation
- safer deployment guidance

Please keep documentation factual and avoid unsupported performance claims.

---

## License

By contributing to this repository, you agree that your contribution may be distributed under the project's [MIT License](LICENSE).

---

## Maintainer

**Prashant Rajput**  
Founder, [Touchstone Infotech](https://www.touchstoneinfotech.com/)

- [GitHub](https://github.com/prashant6788)
- [LinkedIn](https://www.linkedin.com/in/prashant6788/)
