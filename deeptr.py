from Package.Module_2 import TransLate, LangDetect, LanguageList

# Демонстрація роботи функцій з Module_2

if __name__ == "__main__":
    text = "Привіт, як справи?"
    target_language = "en"

    # Визначення мови тексту
    detected_lang = LangDetect(text)
    print(f"Виявлена мова: {detected_lang}")

    # Переклад тексту
    translated_text = TransLate(text, 'auto', target_language)
    print(f"Перекладений текст: {translated_text}")

    # Виведення списку мов з перекладами
    LanguageList(out="screen", text=text)
