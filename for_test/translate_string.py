import re
from exception.custom_exception import TranslateError
from googletrans import Translator

# def define_language(user_text: str):
#     lang = None
#     en = r'[a-zA-Z\s]+$'
#     ru = r'[а-яА-ЯёЁ\s]+$'
#     if re.fullmatch(en, user_text):
#         lang = 'en'
#     elif re.fullmatch(ru, user_text):
#         lang = 'ru'
#     else:
#         raise TranslateError()
#     result = translate_to_english(user_text, lang)
#     return result

def translate_to_english(text):
    translator = Translator()
    try:
        translated = translator.translate(text, src='auto', dest='en')
        return translated.text
    except TranslateError as e:
        return f"Ошибка перевода: {e}"
