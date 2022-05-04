#! /usr/bin/python3

from collections import defaultdict

if __name__ == '__main__':

    # принятие Input и создания dict слов
    with open('resourse_1.txt', encoding='utf-8') as fin:
        text = fin.read()
        words = text.split()
        words_dict = defaultdict(int)
        for w in words:
            words_dict[w] += 1

    # сортировка значений
    words_sorted = sorted(words_dict.items(),
                          key=lambda x: (-x[1], x[0]))

    # вывод результат в output
    with open('result.txt', 'w', encoding='utf-8') as output:
        for word, count in words_sorted:
            print(word, count, file=output)
