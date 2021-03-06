"""
2. Каждое из слов «class», «function», «method» записать в байтовом формате
без преобразования в последовательность кодов (не используя методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.

Подсказки:
--- b'class' - используйте маркировку b''
--- используйте списки и циклы, не дублируйте функции
"""

WORDS = [b'class', b'function', b'method']

def handle_word(word):
    return f'Слово {word} имеет тип {type(word)}'

for word in WORDS:
    print(handle_word(word))
