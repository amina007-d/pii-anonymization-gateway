# Project Proposal

## 1. General information

| | |
|---|---|
| **Project title** | Development of a System for Detecting and Anonymizing Personal Data Before Sending Text to Artificial Intelligence Services |
| **Working name** | PII Anonymization Gateway |
| **Programme** | Software Engineering, Astana IT University |
| **Team** | Dossan Amina (SE-2422), team lead, backend and detection core<br>Abzhamal Nazerke (SE-2422), client application, test corpus and evaluation |
| **Supervisor** | Sakhipov A.A., PhD, Assistant Professor, School of Software Engineering |
| **Period** | October 2026 – May 2027 |

## 2. Problem statement

Generative AI services such as ChatGPT and Gemini have become everyday work tools. Employees and students paste contracts, correspondence, HR documents and client records into these services to summarize, translate or rewrite them [4]. Such text often contains personal data: full names, individual identification numbers (IIN), phone numbers, addresses, ID document and bank card numbers.

Once sent, this data is processed and potentially stored by a third-party provider outside the organization, usually outside Kazakhstan. This conflicts with the Law of the Republic of Kazakhstan "On Personal Data and Its Protection", which regulates the collection, processing and cross-border transfer of personal data [1]. Research shows that language models can memorize and leak personal data [5] and do not reliably keep private information even when instructed to [6]. Publicly reported incidents of confidential data leaking into AI services (e.g. Samsung, 2023 [2]) have led many organizations to restrict or ban AI tools entirely, losing their productivity benefits.

Manual removal of personal data before each request is slow and unreliable. Existing automated PII detection tools are designed mainly for English, do not recognize Kazakhstan-specific identifiers (IIN/BIN, local phone and address formats, Kazakh names), handle mixed Kazakh–Russian–English text poorly [7], [8], and typically mask data irreversibly, so the AI response loses the original names and values the user needs.

**Problem:** there is no practical tool that allows users in Kazakhstan to use external AI services on texts containing personal data without disclosing that data, while still receiving a usable response.

> Assumptions to be verified through user interviews (see `docs/evidence-of-relevance.md`): how often users send personal data to AI services, which data types are most frequent, whether organizations restrict AI tools, and which languages are used in prompts.

## 3. Target users

| User group | Need |
|---|---|
| Employees handling personal data (banking, HR, legal, healthcare, education) | Use AI tools on work documents without violating data protection rules |
| Teachers and students | Use AI tools on texts mentioning students, colleagues or clients |
| Information security teams / administrators | Define processing policies and monitor attempts to send personal data |

## 4. Aim

To develop a middleware system that, before text is sent to external AI services, automatically detects personal data in Kazakh, Russian and English, replaces it with reversible pseudonyms, and restores the original values in the AI response within the organization's infrastructure.

## 5. Objectives

1. Analyse legal requirements and existing PII detection approaches and tools; define the set of personal data categories to be supported.
2. Design the system architecture and the API between the client and the anonymization service.
3. Implement hybrid PII detection combining rule-based recognizers (with checksum validation for IIN/BIN and bank cards) and multilingual NER models, including adaptation for the Kazakh language.
4. Implement reversible pseudonymization with consistent pseudonyms for different word forms of the same entity, and restoration of original values in AI responses.
5. Secure the pseudonym mapping (encryption, limited retention) and exclude personal data from logs.
6. Implement a proxy API compatible with LLM provider interfaces (OpenAI, Gemini), including streaming responses.
7. Develop a browser extension that highlights detected data and lets the user confirm or edit it before sending, and an admin panel for policies and logs.
8. Create a synthetic annotated corpus in three languages and evaluate detection quality against a baseline solution.

## 6. Expected outcomes

- Working anonymization service with a documented REST API
- Browser extension and admin panel integrated with the service
- Synthetic annotated test corpus (Kazakh, Russian, English)
- Evaluation report: precision, recall and F1 per entity type, latency, and comparison with a baseline (Microsoft Presidio without customization [3])
- Target: recall ≥ 0.95 for structured identifiers (IIN/BIN, phone, e-mail, card number, IBAN)