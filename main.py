import numpy as np
import re

N = 2
lenght = 20
L = 0
sentence = ""

def print_dict(dic):
    j = 0
    for i in dic.keys():
        j += 1
        print(j, i, dic[i])

with open("data/МертвыеДуши.txt", "r", encoding="utf-8") as t:
    text = t.read()
    text = text.lower()
    list_of_words = np.array(re.split(r"[ ()«»\n;.,!?:—]+", text))

n_gram = np.array(np.zeros((list_of_words.size - N + 1, N)), dtype='str')
for i in range(0, list_of_words.size - N + 1):
    n_gram[i] = list_of_words[i:i+N]

dict_of_count = {}
for i in range(N, list_of_words.size):
    key = tuple(n_gram[i - N])
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

#print_dict(dict_of_count)

keys = list(dict_of_count.keys())
rand_ind = np.random.choice(range(0, len(keys)))
print(rand_ind)

for i in range(0, len(keys[rand_ind])):
    sentence = sentence + ' ' + keys[rand_ind][i]
lenght -= len(keys[rand_ind])
next_key = keys[rand_ind]

while(L < lenght):
    next_word = np.random.choice(dict_of_count[next_key][0],
                                 1,
                                 dict_of_count[next_key][1])
    sentence = sentence + ' ' + next_word[0]
    for i in dict_of_count.keys():
        if next_word[0] == i[-1] and next_key[1:-1] == i[0:-2]:
            next_key = i
    L += 1
print(sentence)

dict_of_count1 = {}
with open("model.txt", encoding="utf-8") as f:
    for row in f:
        model_i = re.split(r"[():;\n]+", row)
        model_i.pop(0)
        model_i.pop(-1)
        print(model_i)
        key = tuple((model_i[0].split(", ")))
        dict_of_count1[key] = []
        dict_of_count1[key].append(model_i[1].split(", "))
        print(key)
        #print(model_i[1].split(", "), model_i[2].split(", "), sep='\t')
        #dict_of_count[key].append(list(np.array(model_i[2].split(", "), dtype=float)))
print_dict(dict_of_count1)

#dict_of_count.pop()
