import json
from Package.Module_2 import TransLate, LangDetect

def count_sentences(text):
    return text.count('.') + text.count('!') + text.count('?')

def file_info(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            text = file.read()

            # Лічильники
            char_count = len(text)
            word_count = len(text.split())
            sentence_count = count_sentences(text)

            return text, char_count, word_count, sentence_count
    except FileNotFoundError:
        print("Файл не знайдено.")
        return None, 0, 0, 0

def load_config(config_file):
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Конфігураційний файл не знайдено.")
        return None

if __name__ == "__main__":
    # Завантаження конфігурації
    config = load_config("config.json")

    if config:
        text_file = config['file_name']
        target_lang = config['target_language']
        output_option = config['output_option']
        max_chars = config['max_chars']
        max_words = config['max_words']
        max_sentences = config['max_sentences']

        # Інформація про файл
        text, char_count, word_count, sentence_count = file_info(text_file)

        if text:
            print(f"Файл: {text_file}")
            print(f"Кількість символів: {char_count}")
            print(f"Кількість слів: {word_count}")
            print(f"Кількість речень: {sentence_count}")

            detected_lang = LangDetect(text)
            print(f"Мова тексту: {detected_lang}")

            # Перевірка обмежень
            text_to_translate = text
            if char_count > max_chars or word_count > max_words or sentence_count > max_sentences:
                print("Текст перевищує задані параметри, скорочення...")
                text_to_translate = text[:max_chars]

            # Переклад тексту
            translated_text = TransLate(text_to_translate, 'auto', target_lang)

            if output_option == 'screen':
                print(f"Перекладений текст: {translated_text}")
            elif output_option == 'file':
                output_file = f"{text_file.split('.')[0]}_{target_lang}.txt"
                with open(output_file, 'w', encoding='utf-8') as file:
                    file.write(translated_text)
                print(f"Ok: Перекладений текст збережено у файл {output_file}")
            else:
                print("Помилка: Невідома опція виводу")
