from deep_translator import GoogleTranslator



def translate_text(text, target_lang, source_lang='auto'):
    """
    Переводит текст через GoogleTranslator.

    Параметры:
    text (str) - текст для перевода
    target_lang (str) - язык перевода (например: 'en')
    source_lang (str) - исходный язык (по умолчанию auto)

    Возвращает:
    str - переведённый текст
    """

    # Словарь языков
    languages = {
        "английский": "en",
        "русский": "ru",

    }

    # Если пользователь ввёл название языка
    target_code = languages.get(target_lang.lower(), target_lang)

    # Перевод
    translated = GoogleTranslator(
        source=source_lang,
        target=target_code
    ).translate(text)

    return translated