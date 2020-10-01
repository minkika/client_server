"""
4. Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

WORDS = ['разработка','администрирование','protocol','standard']

def handle_word(word):
    word_bytes = word.encode(encoding="utf-8")
    return f'Слово {word} в байтовом представлении: {word_bytes} и обратно: {word_bytes.decode(encoding="utf-8")}'

for word in WORDS:
    print(handle_word(word))
