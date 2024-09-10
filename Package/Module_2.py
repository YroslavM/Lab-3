from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

DetectorFactory.seed = 0

# Функція для перекладу тексту
def TransLate(text: str, scr: str, dest: str) -> str:
    source_lang = CodeLang(scr.lower()) if len(scr) > 2 else scr.lower()
    target_lang = CodeLang(dest.lower()) if len(dest) > 2 else dest.lower()

    # Якщо визначена мова є 'auto', автоматично визначаємо мову
    if scr == 'auto':
        source_lang = LangDetect(text, 'lang')

    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translation = translator.translate(text)
        return translation
    except Exception as e:
        return f"Помилка перекладу: {str(e)}"

# Функція для визначення мови тексту
def LangDetect(text: str, set: str = 'all') -> str:
    try:
        detected_lang = detect(text)
        if set == 'lang':
            return detected_lang
        else:
            return f"Мова: {detected_lang}"
    except LangDetectException as e:
        return f"Помилка визначення мови: {str(e)}"

# Функція для перетворення між кодом мови та її назвою
def CodeLang(lang: str) -> str:
    translator = GoogleTranslator()  # Створюємо екземпляр перекладача
    supported_languages = translator.get_supported_languages(as_dict=True)
    if lang in supported_languages:
        return lang
    else:
        for code, name in supported_languages.items():
            if name.lower() == lang:
                return code
        return "Помилка: Мова не знайдена"

# Функція LanguageList виводить список мов і, якщо заданий текст, перекладає його на кожну мову.
def LanguageList(out: str = "screen", text: str = "") -> str:
    translator = GoogleTranslator()  # Створюємо екземпляр перекладача
    supported_languages = translator.get_supported_languages(as_dict=True)
    output = []
    output.append(f"№  Language      ISO-639 code  Text")
    output.append(f"--------------------------------------------------------")

    num = 1
    for code, name in supported_languages.items():
        line = f"{num}  {name.capitalize():<12}  {code:<12}"

        if text:
            try:
                translation = GoogleTranslator(target=code).translate(text)
                line += f"  {translation}"
            except Exception as e:
                line += f"  Помилка перекладу: {str(e)}"

        output.append(line)
        num += 1

    # Виведення на екран або у файл
    if out == "screen":
        for line in output:
            print(line)
    elif out == "file":
        try:
            with open("language_list.txt", "w", encoding="utf-8") as file:
                for line in output:
                    file.write(line + "\n")
            return "Ok: Дані збережено у файл 'language_list.txt'"
        except Exception as e:
            return f"Помилка збереження у файл: {str(e)}"

    return "Ok"

# Основна програма
if __name__ == "__main__":
    txt = input("Введіть текст: ")
    target_language = input("Введіть мову або код мови для перекладу: ")

    # Визначення мови тексту
    lang_detected = LangDetect(txt, "lang")
    print(f"Виявлена мова: {lang_detected}")

    # Переклад тексту
    translated_text = TransLate(txt, 'auto', target_language)
    print(f"Перекладений текст: {translated_text}")

    # Виведення списку мов з перекладами
    LanguageList(out="screen", text=txt)
    result = LanguageList(out="file", text=txt)
    print(result)
