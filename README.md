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

Employees and students routinely paste documents, correspondence and client data into generative AI services. This transfers personal data to third parties, often across borders, contrary to the Law of the Republic of Kazakhstan "On Personal Data and Their Protection". Many organizations respond by banning AI tools altogether. Existing PII detection tools are designed mainly for English and do not recognize Kazakhstan-specific identifiers (IIN/BIN, local phone and address formats, Kazakh names) or mixed Kazakh–Russian–English text.

A user survey (n = 35) confirmed the problem: 49% of respondents have pasted other people's personal data into AI services, 71% write prompts in several languages or mix them, and 66% would use an automatic protection tool. Details are in [Evidence of Relevance](docs/evidence-of-relevance/).

## Target users

- Employees of organizations that handle personal data (banks, HR, legal, healthcare, education)
- Teachers and students using AI tools for work and study
- Information security teams that define and monitor data-handling policies

## Expected outcomes

- Anonymization service with a documented API: hybrid PII detection (rules + NER) for Kazakh, Russian and English, reversible pseudonymization and response restoration
- Browser extension that intercepts prompts, highlights detected data and lets the user confirm or edit it before sending
- API proxy compatible with the OpenAI and Gemini interfaces for internal systems
- Admin panel for processing policies, users and detection logs
- Synthetic annotated test corpus in Kazakh, Russian, English and mixed language
- Quantitative evaluation: precision, recall, F1 and F2 per entity type and language, compared with a baseline (Presidio without customization); target recall and precision for structured identifiers ≥ 0.95

## Project scope

**In scope**

- Text input only
- Languages: Kazakh, Russian, English and mixed-language text
- PII categories: full names, IIN/BIN (with checksum validation), phone numbers, e-mail, addresses, ID document numbers, IBAN, bank card numbers (Luhn check), organization names
- AI services: ChatGPT and Gemini (other services can be added through separate extension adapters)
- Processing policies per data type: replace, warn, block
- On-premise deployment within the organization's infrastructure (Docker Compose)

**Out of scope**

- Images, PDF and scanned documents (OCR)
- Audio and video
- Mobile applications
- Health data and non-personal confidential information (recorded as future work)

## Team

| Member | Role | Responsibilities |
|---|---|---|
| Dossan Amina | Team lead, backend | Requirements, UX prototype, architecture and diagrams; hybrid detection (rules + NER); reversible pseudonymization and secure mapping storage; REST API and LLM proxy; admin panel backend; security testing and deployment |
| Abzhamal Nazerke | Frontend, evaluation | Existing system comparison, user survey, evaluation plan, project plan; browser extension; admin panel UI; synthetic test corpus; quality evaluation and usability testing |

**Supervisor:** Sakhipov A.A., PhD, Assistant Professor, School of Software Engineering

## Current status

**Stage: analysis and design completed — Pre-defense 1 (24 October 2026).** Next stage: feasibility check of the NER model, implementation of the detection core and the tasks from the supervisor feedback (DIP-20–DIP-24, November 2026).

- [x] [Project proposal and scope](docs/proposal/)
- [x] [Evidence of relevance (user survey, n = 35)](docs/evidence-of-relevance/) — [questionnaire and anonymized responses](docs/survey/)
- [x] [Literature review](docs/literature-review/)
- [x] [Existing system comparison](docs/existing-systems/) — [Presidio baseline test](tests/baseline/)
- [x] [Technology comparison](docs/technology-comparison/)
- [x] [Requirements specification](docs/requirements/)
- [x] [Architecture and design diagrams](docs/diagrams/): system context, component (draft), use case, sequence and ER diagrams — [editable sources](diagrams/)
- [x] [UX prototype](docs/ux-prototype/)
- [x] [Verification and evaluation plan](docs/evaluation-plan/)
- [x] [Project plan and risks](docs/project-plan/)
- [x] [Supervisor feedback log](docs/supervisor-feedback/) — comments of 24 Oct 2026 and team decisions

## Pre-defense 1 submission

- **Tag:** `pre-defense-1`
- **Completed:** analysis and design stage — proposal and scope, user survey and evidence of relevance, literature review (16 sources), existing system comparison with a Presidio baseline check, technology comparison, requirements with acceptance criteria, diagrams, UX prototype, verification and evaluation plan, project plan and risks, supervisor feedback with team decisions. All work items are tracked in YouTrack and merged through reviewed pull requests.
- **Known limitations:**
  - no runnable code yet (implementation starts in November 2026, see the project plan);
  - the evidence of relevance is based on an online survey (n = 35, convenience sample, mostly students and IT staff); interviews with information security specialists are planned (DIP-21);
  - the Presidio check is preliminary (20 synthetic texts);
  - the prototype is static except for the main scenario U1–U4.
- **Outstanding tasks:** supervisor feedback points 2–5 — DIP-20 (novelty), DIP-21 (interviews), DIP-22 (replacement method and grammatical restoration), DIP-23 (independent test set and second baseline), DIP-24 (threat model and legal wording); then the NER feasibility check and the detection core.

## UX prototype

The prototype consists of 18 screens: the main user scenario U1–U4, alternative scenarios U5–U8, the extension window X1–X2, the admin panel A1–A6 and the API P1. The exported screens and the description with the screen–requirement mapping are in [`docs/ux-prototype/`](docs/ux-prototype/).

**How to walk through the main scenario in Figma:**

1. Open the [clickable prototype](https://www.figma.com/proto/Dlm5RuJotH1XFJACEj3E2D/PII-Gateway-%E2%80%94-UX-Prototype?node-id=1-39). If it opens on the overview screen, click «Открыть основной сценарий» (*Open main scenario*).
2. For the best view, click the settings icon in the top right corner and choose **Fit width and height**.
3. Follow the buttons (the interface of the screens is in Russian):
   - **U1** — «Проверить найденное» (*Check detected data*) → U2
   - **U2** — «Далее: что получит ИИ» (*Next: what the AI will receive*) → U3; «Назад» (*Back*) → U1
   - **U3** — «Отправить обезличенный текст» (*Send anonymized text*) → U4; «Назад к проверке» (*Back to review*) → U2
   - **U4** — «К обзору прототипа» (*Back to the overview*)
4. Clicking on an empty area highlights the clickable zones; **Restart** (key **R**) starts the scenario again.

The other screens are static and can be viewed in the [design file](https://www.figma.com/design/Dlm5RuJotH1XFJACEj3E2D/PII-Gateway-%E2%80%94-UX-Prototype?node-id=1-40). All data on the screens is fictitious.

## Selected technologies

| Area | Technologies |
|---|---|
| Backend | Python, FastAPI |
| PII detection | Microsoft Presidio, spaCy, Hugging Face Transformers (PyTorch), XLM-RoBERTa, KazNERD |
| Storage | PostgreSQL (users, policies, logs), Redis (temporary encrypted pseudonym mapping) |
| Security | AES-256-GCM (cryptography), JWT, role-based access control |
| AI integration | OpenAI API, Google Gemini API |
| Client | JavaScript, HTML/CSS, WebExtensions API (Manifest V3), React |
| Evaluation | pandas, Faker, Label Studio, Locust |
| Testing | pytest, Jest, Playwright, Postman |
| DevOps | Docker, Docker Compose, GitHub Actions |
| Design | Figma, draw.io |

The rationale for these choices is documented in [`docs/technology-comparison/`](docs/technology-comparison/).

## Links

- YouTrack project: https://pii-gateway.youtrack.cloud/projects/DIP
- Figma prototype: [clickable prototype](https://www.figma.com/proto/Dlm5RuJotH1XFJACEj3E2D/PII-Gateway-%E2%80%94-UX-Prototype?node-id=1-39), [design file](https://www.figma.com/design/Dlm5RuJotH1XFJACEj3E2D/PII-Gateway-%E2%80%94-UX-Prototype?node-id=1-40)
- Documentation: [`docs/`](docs/)
- Diagrams: [`diagrams/`](diagrams/)

## Repository structure

```
├── docs/
│   ├── proposal/               # project proposal
│   ├── survey/                 # questionnaire and anonymized responses
│   ├── evidence-of-relevance/  # survey analysis
│   ├── literature-review/      # literature review
│   ├── existing-systems/       # comparison of existing systems
│   ├── technology-comparison/  # technology decisions
│   ├── requirements/           # requirements specification
│   ├── ux-prototype/           # prototype document, screens (PNG) and sources
│   ├── diagrams/               # design diagrams document
│   ├── evaluation-plan/        # verification and evaluation plan
│   ├── project-plan/           # project plan and risk register
│   └── supervisor-feedback/    # supervisor feedback log
├── diagrams/                   # editable sources (.drawio) and exports (.png)
├── src/
│   ├── backend/                # anonymization service (FastAPI)
│   └── extension/              # browser extension
├── tests/
│   └── baseline/               # Presidio baseline test and results
└── config/                     # configuration examples (.env.example)
```

Documents are written in LaTeX; each folder contains the source (`.tex`) and the compiled `.pdf`.

## Setup, execution and testing

Instructions will be added as soon as runnable code is available (planned for November–December 2026).

The Presidio baseline test can already be run with Python 3.12:

```
python3.12 -m venv .venv
source .venv/bin/activate
pip install presidio-analyzer
python -m spacy download en_core_web_lg
python -m spacy download ru_core_news_lg
python -m spacy download xx_ent_wiki_sm
python tests/baseline/presidio_baseline_check.py
```

## Development workflow

- Every work item is a YouTrack task (`DIP-<n>`).
- Branch naming: `DIP-<n>-short-description`, e.g. `DIP-14-diagrams`.
- Commit messages start with the task ID: `DIP-14: Add architecture and sequence diagrams`.
- Pull request descriptions contain three sections — *What*, *Task* (link to the YouTrack task) and *How checked*.
- Changes are merged into `main` only through pull requests approved by the other team member.
- Each pre-defense submission is tagged: `pre-defense-1`, `pre-defense-2`, `final-pre-defense`.
- Secrets, API keys and real personal data are never committed; use `config/.env.example` with placeholder values. Only synthetic data is used for testing.