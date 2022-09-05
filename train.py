import re
import numpy as np

N = 1

def complete_write(dict_of_count, key):
    sen = '(' + key[0]
    for i in range(1, len(key)):
        sen = sen + ", " + key[i]
    sen += "):((" + dict_of_count[key][0][0]

    for i in range(1, len(dict_of_count[key][0])):
        sen = sen + ", " + dict_of_count[key][0][i]
    sen += ");(" + str(dict_of_count[key][1][0])

    for i in range(1, len(dict_of_count[key][1])):
        sen = sen + ", " + str(dict_of_count[key][1][i])
    sen += "))"

    return sen

def train(input_dir, model):
    with open(input_dir, "r", encoding="utf-8") as f:
        text = f.read()
        text = text.lower()
        list_of_words = np.array(re.split(r"[ ()«»\n;.,!?:—]+", text))

    n_gram = np.array(np.zeros((list_of_words.size - N - 1, N)), dtype='str')
    for i in range(0, list_of_words.size - N - 1):
        n_gram[i] = list_of_words[i:i + N]

    dict_of_count = {}
    for i in range(N, list_of_words.size):
        key = tuple(n_gram[i - N - 1])
        if key in dict_of_count.keys():
            dict_of_count[key].append(list_of_words[i])
        else:
            dict_of_count[key] = list([list_of_words[i]])

    for i in dict_of_count.keys():
        uniq_word, count = np.unique(dict_of_count[i], return_counts=True)
        count = count / len(dict_of_count[i])
        uniq_word = list(uniq_word)
        dict_of_count[i].clear()
        dict_of_count[i].append(uniq_word)
        dict_of_count[i].append(list(count))

    with open(model, "w", encoding="utf-8") as f:
        for i in dict_of_count.keys():
            f.write(complete_write(dict_of_count, i) + "\n")

#train("text.txt", "model.txt")