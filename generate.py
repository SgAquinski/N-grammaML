import re
import numpy as np

def print_dict(dic):
    j = 0
    for i in dic.keys():
        j += 1
        print(j, i, dic[i])

def generate(model, prefix , lenght):
    L = 0
    sentence = ""
    dict_of_count = {}

    with open("model.txt", encoding="utf-8") as f:
        for row in f:
            model_i = re.split(r"[():;\n]+", row)
            model_i.pop(0)
            model_i.pop(-1)
            key = tuple((model_i[0].split(", ")))
            dict_of_count[key] = []
            dict_of_count[key].append(model_i[1].split(", "))
            dict_of_count[key].append(list(np.array(model_i[2].split(", "), dtype=float)))

    keys = list(dict_of_count.keys())
    rand_ind = np.random.choice(range(0, len(keys)))

    for i in range(0, len(keys[rand_ind])):
        sentence = sentence + ' ' + keys[rand_ind][i]
    lenght -= len(keys[rand_ind])
    next_key = keys[rand_ind]

    while (L < lenght):
        next_word = np.random.choice(dict_of_count[next_key][0], 1, dict_of_count[next_key][1])
        sentence = sentence + ' ' + next_word[0]
        for i in dict_of_count.keys():
            if next_word[0] == i[-1] and next_key[1:-1] == i[0:-2]:
                next_key = i
        L += 1

    print(sentence)

#generate("model.txt",20,20)
