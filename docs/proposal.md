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

## 7. Scope

**In scope**

- Text input entered or pasted by the user
- Languages: Kazakh, Russian, English, including mixed-language text
- PII categories: full names, IIN/BIN, phone numbers, e-mail addresses, postal addresses, ID document numbers, IBAN, bank card numbers
- Target AI services: ChatGPT and Gemini (web interfaces via extension, APIs via proxy); the choice will be confirmed by user interviews. The extension uses a separate adapter per service, so other services (e.g. Claude, Copilot, DeepSeek) can be added without changing the core
- Processing policies per data type: replace, block sending, warn
- On-premise deployment (Docker)

**Out of scope**

- Images, PDF and scanned documents (OCR)
- Audio and video content
- Mobile applications
- AI services other than ChatGPT and Gemini
- Detection of non-personal confidential information (trade secrets, source code)

## 8. Engineering complexity

- **Multilingual NER with limited resources:** few annotated datasets and models exist for Kazakh; texts often switch between languages within one sentence.
- **Morphology-aware pseudonymization:** Kazakh and Russian names change form by case and suffix; all forms of one entity must map to the same pseudonym, and restoration must still work after the AI model inflects or reformulates the pseudonym.
- **Preserving meaning:** anonymized text must remain useful for the AI model, so pseudonyms must keep the entity type and context.
- **Security of the system itself:** the pseudonym mapping contains the same personal data the system protects and must be encrypted and short-lived.
- **Streaming integration:** pseudonyms may be split across chunks of a streamed AI response.
- **Performance:** processing must not noticeably delay the user's request.

## 9. Constraints and risks (summary)

| Risk | Mitigation |
|---|---|
| Limited Kazakh NER data and models | Use KazNERD and synthetic data; rule-based recognizers for structured identifiers |
| AI service web interfaces change and break interception | Limit extension support to two services; provide proxy API as a stable alternative |
| Real personal data cannot be used for testing | Generate a synthetic corpus with fake but valid-format identifiers |
| Schedule slippage | MVP first (rules + basic NER + extension), extensions later |

A detailed plan and risk register are maintained in `docs/project-plan.md` and the YouTrack project.

## 10. References

[1] Law of the Republic of Kazakhstan No. 94-V "On Personal Data and Its Protection", 21 May 2013 (current edition). https://adilet.zan.kz/rus/docs/Z1300000094
[2] Bloomberg. Samsung Bans Staff's AI Use After Spotting ChatGPT Data Leak, 2 May 2023. https://www.bloomberg.com/news/articles/2023-05-02/samsung-bans-chatgpt-and-other-generative-ai-use-by-staff-after-leak
[3] Microsoft Presidio documentation. https://presidio.dataprivacystack.org/
[4] Cyberhaven. Employees are pasting company data into ChatGPT. https://www.cyberhaven.com/blog/4-2-of-workers-have-pasted-company-data-into-chatgpt
[5] N. Lukas et al. Analyzing Leakage of Personally Identifiable Information in Language Models. IEEE S&P 2023.
[6] N. Mireshghallah et al. Can LLMs Keep a Secret? Testing Privacy Implications of Language Models via Contextual Integrity Theory. ICLR 2024.
[7] R. Yeshpanov, Y. Khassanov, H. A. Varol. KazNERD: Kazakh Named Entity Recognition Dataset. LREC 2022.
[8] Existing system comparison and Presidio baseline test: `docs/existing-systems.md`.