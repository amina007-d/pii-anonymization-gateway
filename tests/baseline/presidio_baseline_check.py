from collections import defaultdict

from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_analyzer.predefined_recognizers import (
    CreditCardRecognizer,
    EmailRecognizer,
    IbanRecognizer,
    PhoneRecognizer,
    SpacyRecognizer,
)

SAMPLES = [
    ("kk", "Сәлеметсіз бе, менің атым Айгерім Нұрланқызы, ЖСН 950101400002.",
     [("Айгерім Нұрланқызы", "PERSON"), ("950101400002", "IIN")]),
    ("kk", "Қайрат Серікбаевқа +7 701 234 56 78 нөміріне хабарласыңыз.",
     [("Қайрат Серікбаевқа", "PERSON"), ("+7 701 234 56 78", "PHONE")]),
    ("kk", "Шартты Астана қаласы, Абай даңғылы 12-үйге жіберіңіз, e-mail: dana.omarova@example.kz",
     [("Астана", "LOCATION"), ("Абай даңғылы 12", "ADDRESS"), ("dana.omarova@example.kz", "EMAIL")]),
    ("kk", "Жалақыны KZ75125KZT1001300335 шотына аударыңыз, алушы Ерлан Жұмабаев.",
     [("KZ75125KZT1001300335", "IBAN"), ("Ерлан Жұмабаев", "PERSON")]),
    ("kk", "Әсем Бекова туралы анықтама жазыңыз, ол 8 777 345 67 89 телефонымен тіркелген.",
     [("Әсем Бекова", "PERSON"), ("8 777 345 67 89", "PHONE")]),
    ("kk", "Карта нөмірі 4111 1111 1111 1111, иесі Нұржан Сапаров, ЖСН 880512300005.",
     [("4111 1111 1111 1111", "CARD"), ("Нұржан Сапаров", "PERSON"), ("880512300005", "IIN")]),
    ("ru", "Составь письмо для Иванова Сергея Петровича, ИИН 850315300009, тел. +7 (705) 111-22-33.",
     [("Иванова Сергея Петровича", "PERSON"), ("850315300009", "IIN"), ("+7 (705) 111-22-33", "PHONE")]),
    ("ru", "Клиентка Мария Ким проживает по адресу г. Алматы, ул. Сатпаева, д. 5, кв. 10.",
     [("Мария Ким", "PERSON"), ("Алматы", "LOCATION"), ("ул. Сатпаева, д. 5, кв. 10", "ADDRESS")]),
    ("ru", "Переведи оплату на счёт KZ75125KZT1001300335, получатель ТОО «Альфа Сервис».",
     [("KZ75125KZT1001300335", "IBAN"), ("ТОО «Альфа Сервис»", "ORG")]),
    ("ru", "Напиши ответ Ахметову Тимуру на почту t.akhmetov@example.com по поводу договора.",
     [("Ахметову Тимуру", "PERSON"), ("t.akhmetov@example.com", "EMAIL")]),
    ("ru", "Номер карты сотрудника 5555 5555 5555 4444, оформлена на Ольгу Смирнову.",
     [("5555 5555 5555 4444", "CARD"), ("Ольгу Смирнову", "PERSON")]),
    ("ru", "Студент Даурен Касымов, ИИН 020730500005, телефон 87071234567.",
     [("Даурен Касымов", "PERSON"), ("020730500005", "IIN"), ("87071234567", "PHONE")]),
    ("en", "Please draft a reminder to John Carter about the invoice, his phone is +1 202 555 0143.",
     [("John Carter", "PERSON"), ("+1 202 555 0143", "PHONE")]),
    ("en", "Summarize the complaint from Aliya Sultanova, email aliya.s@example.org, IIN 970214400000.",
     [("Aliya Sultanova", "PERSON"), ("aliya.s@example.org", "EMAIL"), ("970214400000", "IIN")]),
    ("en", "Transfer the refund to card 4111 1111 1111 1111 owned by Emily Stone.",
     [("4111 1111 1111 1111", "CARD"), ("Emily Stone", "PERSON")]),
    ("en", "Our client Arman Tokayev lives in Almaty, phone +7 701 555 12 34.",
     [("Arman Tokayev", "PERSON"), ("Almaty", "LOCATION"), ("+7 701 555 12 34", "PHONE")]),
    ("mix", "Привет, Айжан Мұратқызы просила отправить договор на aizhan.m@example.kz до пятницы.",
     [("Айжан Мұратқызы", "PERSON"), ("aizhan.m@example.kz", "EMAIL")]),
    ("mix", "Бүгін Болат Ахметов позвонил с номера +7 747 890 12 34, ИИН 910405300001.",
     [("Болат Ахметов", "PERSON"), ("+7 747 890 12 34", "PHONE"), ("910405300001", "IIN")]),
    ("mix", "Please translate: Мадина Әлиева, Қарағанды, ул. Ерубаева 20, тел. 8 701 999 88 77.",
     [("Мадина Әлиева", "PERSON"), ("Қарағанды", "LOCATION"), ("ул. Ерубаева 20", "ADDRESS"),
      ("8 701 999 88 77", "PHONE")]),
    ("mix", "Счёт KZ75125KZT1001300335, иесі Санжар Омаров, email s.omarov@example.com.",
     [("KZ75125KZT1001300335", "IBAN"), ("Санжар Омаров", "PERSON"), ("s.omarov@example.com", "EMAIL")]),
]


def default_engine():
    return AnalyzerEngine()


def multilingual_engine():
    provider = NlpEngineProvider(nlp_configuration={
        "nlp_engine_name": "spacy",
        "models": [
            {"lang_code": "en", "model_name": "en_core_web_lg"},
            {"lang_code": "ru", "model_name": "ru_core_news_lg"},
            {"lang_code": "xx", "model_name": "xx_ent_wiki_sm"},
        ],
    })
    nlp_engine = provider.create_engine()
    registry = RecognizerRegistry(supported_languages=["en", "ru", "xx"])
    registry.load_predefined_recognizers(languages=["en"], nlp_engine=nlp_engine)
    for lang in ("ru", "xx"):
        registry.add_recognizer(SpacyRecognizer(supported_language=lang,
                                                supported_entities=["PERSON", "LOCATION", "ORGANIZATION"]))
        registry.add_recognizer(EmailRecognizer(supported_language=lang))
        registry.add_recognizer(PhoneRecognizer(supported_language=lang, supported_regions=("KZ", "RU", "US")))
        registry.add_recognizer(CreditCardRecognizer(supported_language=lang))
        registry.add_recognizer(IbanRecognizer(supported_language=lang))
    return AnalyzerEngine(nlp_engine=nlp_engine, registry=registry, supported_languages=["en", "ru", "xx"])


LANG_FOR_B = {"en": "en", "ru": "ru", "kk": "xx", "mix": "xx"}


CORRECT_TYPES = {
    "PERSON": {"PERSON"},
    "LOCATION": {"LOCATION"},
    "ADDRESS": {"LOCATION"},
    "ORG": {"ORGANIZATION"},
    "EMAIL": {"EMAIL_ADDRESS"},
    "PHONE": {"PHONE_NUMBER"},
    "CARD": {"CREDIT_CARD"},
    "IBAN": {"IBAN_CODE"},
    "IIN": set(),
}


def evaluate(engine, lang_map):
    per_type = defaultdict(lambda: [0, 0, 0])
    per_lang = defaultdict(lambda: [0, 0, 0])
    false_pos, misses = [], []
    for lang, text, gold in SAMPLES:
        results = engine.analyze(text=text, language=lang_map(lang))
        gold_spans = []
        for value, gtype in gold:
            start = text.index(value)
            end = start + len(value)
            gold_spans.append((start, end))
            hits = [r for r in results if r.start < end and r.end > start]
            masked = bool(hits)
            correct = any(r.entity_type in CORRECT_TYPES[gtype] for r in hits)
            for counter in (per_type[gtype], per_lang[lang]):
                counter[0] += masked
                counter[1] += correct
                counter[2] += 1
            if not masked:
                misses.append((lang, gtype, value, "-"))
            elif not correct:
                misses.append((lang, gtype, value, "wrong type: " + ", ".join(sorted({r.entity_type for r in hits}))))
        for r in results:
            if not any(r.start < e and r.end > s for s, e in gold_spans):
                false_pos.append((lang, r.entity_type, text[r.start:r.end]))
    return per_type, per_lang, false_pos, misses


def fmt(found, total):
    return f"{found}/{total} ({found / total:.2f})"


def main():
    setups = {
        "A: default (en)": (default_engine(), lambda lang: "en"),
        "B: + ru/multilingual": (multilingual_engine(), lambda lang: LANG_FOR_B[lang]),
    }
    results = {name: evaluate(engine, lang_map) for name, (engine, lang_map) in setups.items()}
    types = sorted({g for _, _, gold in SAMPLES for _, g in gold})
    names = list(results)

    head = f"{'':<10}" + "".join(f"{n + ' masked':<30}{n + ' correct type':<34}" for n in names)
    for title, idx, keys in (("Recall by entity type", 0, types), ("Recall by language", 1, ["kk", "ru", "en", "mix"])):
        print("\n" + title)
        print(head)
        for k in keys:
            row = f"{k:<10}"
            for n in names:
                m, c, t = results[n][idx][k]
                row += f"{fmt(m, t):<30}{fmt(c, t):<34}"
            print(row)

    for n in names:
        m = sum(v[0] for v in results[n][0].values())
        c = sum(v[1] for v in results[n][0].values())
        t = sum(v[2] for v in results[n][0].values())
        print(f"\n{n}: masked {fmt(m, t)}, correct type {fmt(c, t)}, false positives {len(results[n][2])}")
        for lang, gtype, value, why in results[n][3]:
            print(f"   miss [{lang}] {gtype:<8} {value:<28} {why}")
        for lang, etype, value in results[n][2]:
            print(f"   FP   [{lang}] {etype:<16} {value}")


if __name__ == "__main__":
    main()
