# PII Anonymization Gateway for AI Services

**Development of a System for Detecting and Anonymizing Personal Data Before Sending Text to Artificial Intelligence Services**

Diploma project, Software Engineering, Astana IT University (2026–2027).

## Brief description

A middleware layer between the user and generative AI services (ChatGPT, Gemini). Before a prompt leaves the organization, the system detects personal data in the text, replaces it with reversible pseudonyms, sends only the anonymized text to the AI service, and then restores the original values in the model's response.

```
User ──► Browser extension ──► Anonymization service ──► AI service (ChatGPT / Gemini)
                                  │  detect PII                    │
                                  │  replace with pseudonyms       │
User ◄── restored response ◄──────┘  restore original values ◄─────┘
```

Example:

| Stage | Text |
|---|---|
| Original prompt | Write a reminder to Aigerim Nurlanova (IIN 950101400123, +7 701 123 45 67) about the contract payment. |
| Sent to AI service | Write a reminder to `<PERSON_1>` (IIN `<IIN_1>`, `<PHONE_1>`) about the contract payment. |
| Response shown to user | Dear Aigerim Nurlanova, … |

*All personal data in examples is fictional.*

## Problem statement

Employees and students routinely paste documents, correspondence and client data into generative AI services. This transfers personal data to third parties, often across borders, contrary to the Law of the Republic of Kazakhstan "On Personal Data and Its Protection". Many organizations respond by banning AI tools altogether. Existing PII detection tools are designed mainly for English and do not recognize Kazakhstan-specific identifiers (IIN/BIN, local phone and address formats, Kazakh names) or mixed Kazakh–Russian–English text.

## Target users

- Employees of organizations that handle personal data (banks, HR, legal, healthcare, education)
- Teachers and students using AI tools for work and study
- Information security teams that define and monitor data-handling policies

## Expected outcomes

- Anonymization service with a documented API: hybrid PII detection (rules + NER) for Kazakh, Russian and English, reversible pseudonymization and response restoration
- Browser extension that intercepts prompts, highlights detected data and lets the user confirm or edit it before sending
- Admin panel for processing policies and detection logs
- Synthetic annotated test corpus in three languages
- Quantitative evaluation: precision / recall / F1 per entity type, compared with a baseline (Presidio without customization); target recall for structured identifiers ≥ 0.95

## Project scope

**In scope**

- Text input only
- Languages: Kazakh, Russian, English
- PII categories: full names, IIN/BIN (with checksum validation), phone numbers, e-mail, addresses, ID document numbers, IBAN, bank card numbers (Luhn check)
- AI services: ChatGPT and Gemini
- On-premise deployment within the organization's infrastructure

**Out of scope**

- Images, PDF and scanned documents (OCR)
- Audio and video
- Mobile applications
- AI services other than those listed above

## Team

| Member | Role | Responsibilities |
|---|---|---|
| Dossan Amina | Team lead, backend | PII categories and legal requirements, hybrid detection (rules + NER), reversible pseudonymization, secure mapping storage, LLM proxy API, admin panel backend, testing and deployment |
| Abzhamal Nazerke | Frontend, evaluation | Browser extension, admin panel UI, UX prototype, synthetic test corpus, quality evaluation, user testing |

**Supervisor:** Sakhipov A.A., PhD, Assistant Professor, School of Software Engineering

## Current status

**Stage: analysis and design (October 2026).** Pre-defense 1 materials are being prepared.

- [ ] Project proposal and scope
- [ ] Evidence of relevance (user interviews)
- [ ] Literature review
- [ ] Existing system comparison
- [ ] Technology comparison
- [ ] Requirements specification
- [ ] Architecture diagrams
- [ ] UX prototype
- [ ] Verification and evaluation plan
- [ ] Project plan and risks

## Selected technologies

| Area | Technologies |
|---|---|
| Backend | Python, FastAPI |
| PII detection | Microsoft Presidio, spaCy, Hugging Face Transformers (PyTorch), KazNERD |
| Storage | PostgreSQL (policies, logs), Redis (temporary pseudonym mapping) |
| Security | AES encryption (cryptography), JWT, role-based access control |
| AI integration | OpenAI API, Google Gemini API |
| Client | JavaScript, HTML/CSS, WebExtensions API (Manifest V3), React |
| Evaluation | pandas, Faker, Label Studio |
| Testing | pytest, Jest, Postman |
| DevOps | Docker, Docker Compose, GitHub Actions |
| Design | Figma, draw.io |

The rationale for these choices is documented in [`docs/technology-comparison.md`](docs/technology-comparison.md).

## Links

- YouTrack project: https://pii-gateway.youtrack.cloud/projects/DIP
- Figma prototype: *(link)*
- Documentation: [`docs/`](docs/)
- Diagrams: [`diagrams/`](diagrams/)

## Repository structure

```
├── docs/          # proposal, literature review, comparisons, requirements, evaluation plan, supervisor feedback
├── diagrams/      # editable sources (.drawio) and exports (.png)
├── src/
│   ├── backend/   # anonymization service (FastAPI)
│   └── extension/ # browser extension
├── tests/         # automated tests and test materials
└── config/        # configuration examples (.env.example)
```

## Setup, execution and testing

Instructions will be added as soon as runnable code is available.

## Development workflow

- Every work item is a YouTrack task (`DIP-<n>`).
- Branch naming: `DIP-<n>-short-description`, e.g. `DIP-5-technology-comparison`.
- Commit messages start with the task ID: `DIP-5: Add server platform comparison`.
- Changes are merged into `main` through pull requests reviewed by the other team member.
- Each pre-defense submission is tagged: `pre-defense-1`, `pre-defense-2`, `final-pre-defense`.
- Secrets, API keys and real personal data are never committed; use `config/.env.example` with placeholder values.
