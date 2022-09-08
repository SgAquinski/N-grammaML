import re
import numpy as np
import pickle
import os
import argparse

def formatting_write(dict_of_count, key):
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

def formatting_read(model, dict_of_count):
    with open(model, encoding="utf-8") as f:
        for row in f:
            model_i = re.split(r"[():;\n]+", row)
            model_i.pop(0)
            model_i.pop(-1)
            key = tuple((model_i[0].split(", ")))
            dict_of_count[key] = []
            dict_of_count[key].append(model_i[1].split(", "))
            dict_of_count[key].append(list(np.array(model_i[2].split(", "),
                                                    dtype=float)))

class N_gram():

    def __init__(self):
        self.N = 1
        self.seed = 0
        self.pickled_dict = bytes()

    def fit(self, input_dir, model):
        dict_of_count = {}

        with open(input_dir, "r", encoding="utf-8") as f:
            text = f.read()
            text = text.lower()
            list_of_words = np.array(re.split(r"[ ()«»\n;.,!?:—]+", text))

        n_gram = np.array(np.zeros((list_of_words.size - self.N + 1, self.N)),
                          dtype='str')
        for i in range(0, list_of_words.size - self.N + 1):
            n_gram[i] = list_of_words[i:i + self.N]

        for i in range(self.N, list_of_words.size - 1):
            key = tuple(n_gram[i - self.N])
            if key in dict_of_count.keys():
                dict_of_count[key].append(list_of_words[i])
            else:
                dict_of_count[key] = list([list_of_words[i]])

        for key in dict_of_count.keys():
            uniq_word, count = np.unique(dict_of_count[key],
                                         return_counts=True)
            count = count / len(dict_of_count[key])
            uniq_word = list(uniq_word)
            dict_of_count[key].clear()
            dict_of_count[key].append(uniq_word)
            dict_of_count[key].append(list(count))

        self.pickled_dict = pickle.dumps(dict_of_count)

        with open(model, "a", encoding="utf-8") as f:
            for key in dict_of_count.keys():
                f.write(formatting_write(dict_of_count, key) + "\n")
        dict_of_count.clear()

    def generate(self, model, prefix, lenght):
        sentence = ""
        dict_of_count = {}

        if (not os.path.exists(model)) or (os.stat(model).st_size == 0):
            dict_of_count = pickle.load(self.pickled_dict)
        else:
            formatting_read(model, dict_of_count)

        if prefix is None \
                or prefix == "None" \
                or prefix == '' \
                or tuple(prefix) not in dict_of_count.keys():
            keys = list(dict_of_count.keys())
            rand_ind = np.random.choice(range(0, len(keys)))
            for i in range(0, len(keys[rand_ind])):
                sentence = sentence + ' ' + keys[rand_ind][i]
            lenght -= len(keys[rand_ind])
            next_key = keys[rand_ind]
        else:
            prefix = re.split(r"[ ()«»\n;.,!?:—_]+", prefix.lower())
            for i in range(len(prefix)):
                sentence = sentence + ' ' + prefix[i]
            lenght -= len(prefix)
            next_key = tuple(prefix)

        while (lenght > 0):
            next_word = np.random.choice(dict_of_count[next_key][0],
                                         1, dict_of_count[next_key][1])
            sentence = sentence + ' ' + next_word[0]
            for key in dict_of_count.keys():
                if next_word[0] == key[-1] and next_key[1:-1] == key[0:-2]:
                    next_key = key
            lenght -= 1
        print(sentence)

        dict_of_count.clear()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=str)
    parser.add_argument("--model", type=str)
    arg = parser.parse_args()

    t = N_gram()
    for filename in os.listdir(arg.input_dir):
        t.fit(os.path.join(arg.input_dir, filename), arg.model)
