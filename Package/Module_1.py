from googletrans import Translator, LANGUAGES

def TransLate(text: str, scr: str, dest: str) -> str:
    translator = Translator()

    # Якщо scr або dest не є кодом мови, перетворюємо його
    source_lang = CodeLang(scr.lower()) if len(scr) > 2 else scr.lower()
    target_lang = CodeLang(dest.lower()) if len(dest) > 2 else dest.lower()

    # Якщо визначена мова є 'auto', спробуємо визначити її автоматично
    if scr == 'auto':
        source_lang = LangDetect(text, 'lang')

    try:
        translation = translator.translate(text, src=source_lang, dest=target_lang)
        return translation.text
    except Exception as e:
        return f"Помилка перекладу: {str(e)}"

# Функція для визначення мови тексту
def LangDetect(text: str, set: str = 'all') -> str:
    translator = Translator()
    try:
        detected = translator.detect(text)
        if set == 'lang':
            return detected.lang
        elif set == 'confidence':
            return str(detected.confidence)
        else:
            return f"Мова: {detected.lang}, Коефіцієнт довіри: {detected.confidence}"
    except Exception as e:
        return f"Помилка визначення мови: {str(e)}"

# Функція для перетворення між кодом мови та її назвою
def CodeLang(lang: str) -> str:
    if lang in LANGUAGES:
        return LANGUAGES[lang]
    else:
        for code, name in LANGUAGES.items():
            if name.lower() == lang:
                return code
        return "Помилка: Мова не знайдена"

#Функція LanguageList виводить список мов і, якщо заданий текст, перекладає його на кожну мову.
def LanguageList(out: str = "screen", text: str = "") -> str:
    translator = Translator()
    output = []
    output.append(f"№  Language      ISO-639 code  Text")
    output.append(f"--------------------------------------------------------")

    num = 1
    for code, name in LANGUAGES.items():
        line = f"{num}  {name.capitalize():<12}  {code:<12}"

        if text:
            try:
                translation = translator.translate(text, dest=code)
                line += f"  {translation.text}"
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


if __name__ == "__main__":
    txt = input("Введіть текст: ")
    target_language = input("Введіть мову або код мови для перекладу: ")

    # Визначення мови тексту
    lang_detected = LangDetect(txt, "all")
    print(f"Виявлена мова та коефіцієнт довіри: {lang_detected}")

    # Переклад тексту
    translated_text = TransLate(txt, 'auto', target_language)
    print(f"Перекладений текст: {translated_text}")

    LanguageList(out="screen", text=txt)
    result = LanguageList(out="file", text=txt)
    print(result)