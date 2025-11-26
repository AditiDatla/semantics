'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 20, 2023.
'''

import math

def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as 
    described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    # dot product over matching keys I FIXED IT TO USE CRAP RIGHT
    dot = 0.0
    for k, v in vec1.items():
        if k in vec2:
            dot += v * vec2[k]

    n1 = norm(vec1)
    n2 = norm(vec2)
    if n1 == 0 or n2 == 0:
        return -1.0
    return dot / (n1 * n2)

def build_semantic_descriptors(sentences):
    word_occ = {}

    for sentence in sentences:
        unique_words = list(set(sentence))

        for word in unique_words:
            if word not in word_occ:
                word_occ[word] = {}

            for other in unique_words:
                if other != word:
                    word_occ[word][other] = word_occ[word].get(other, 0) + 1

    return word_occ

def split_into_sentences(text):
    sentences = []
    current = ""

    for char in text:
        if char in ".?!":
            if current.strip(): #avoiding empty sentences
                sentences.append(current.strip().split())

            current = ""
        else:
            current += char
    
    return sentences

def build_semantic_descriptors_from_files(filenames):
    punctuation_to_remove = [",", "-", "--", ":", ";"]
    descriptors = {}

    file_text = ""
    for filename in filenames:
        with open(filename, "r", encoding="latin1") as f:
            file_text += " " + f.read().lower()

    # Remove non-essential punctuation
    for p in punctuation_to_remove:
        file_text = file_text.replace(p, " ")

    sentences = split_into_sentences(file_text)

    for sentence in sentences:
        unique_words = set(sentence)
        for w in unique_words:
            if w not in descriptors:
                descriptors[w] = {}
            for other in unique_words:
                if other == w:
                    continue
                descriptors[w][other] = descriptors[w].get(other, 0) + 1

    return descriptors


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    best_choice = choices[0]
    best_sim = -1

    for i in range(len(choices)):
        choice = choices[i]

        if word not in semantic_descriptors or choice not in semantic_descriptors:
            sim = -1
        else:
            sim = similarity_fn(semantic_descriptors[word], semantic_descriptors[choice])

        if sim > best_sim:
            best_sim = sim
            best_choice = choice
    
    return best_choice


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    total = 0
    correct = 0

    with open(filename, "r", encoding="latin1") as f:
        for line in f:
            parts = line.split()

            word = parts[0]
            answer = parts[1]
            options = parts[2:]

            guess = most_similar_word(word, options, semantic_descriptors, similarity_fn)

            total += 1
            if guess == answer:
                correct += 1

    
    if total == 0:
        return 0.0
    else:
        return ((correct / total) * 100.0)



weirdo = [["i", "am", "a", "sick", "man"], ["i", "am", "a", "spiteful", "man"], ["i", "am", "an", "unattractive", "man"], ["i", "believe", "my", "liver", "is", "diseased"], ["however", "i", "know", "nothing", "at", "all", "about", "my", "disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]


if __name__ == '__main__':

    word_of_choice = "man"
    mychoices = ['i', 'am', 'a']
    my_descriptors = build_semantic_descriptors(weirdo)

    #function tests
    print(cosine_similarity({"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6})) # shuld be ~0.70
    print(build_semantic_descriptors(weirdo)) # should be really long idk
    print(split_into_sentences("This is a sentence. This is another sentence. Genshin gooners are crazy! What the hell?")) #should look like weirdo
    #print(build_semantic_descriptors_from_files(myfile)) #holy guacamole be careful running this
    print(most_similar_word(word_of_choice, mychoices, my_descriptors, cosine_similarity)) #I think a is right? but idk ngl

    sem_descriptors = build_semantic_descriptors_from_files(['semanticssubject1.txt', 'semanticssubject2.txt']) 
    res = run_similarity_test('testytesty.txt', sem_descriptors, cosine_similarity) 
    print(res, "% of the guesses were correct") #we are at 70% rn..... could be better ehehehe


