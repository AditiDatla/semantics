'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 20, 2023.
'''

import math
import numpy as np

def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as 
    described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    #kind of not efficient... could be better? LMAO I JUST REALIZED THERE'S ALRADY A NORM FUNCTION
    vector_1 = []
    vector_2 = []
    vecta1 = []
    vecta2 = []

    for key, value in vec1.items():
        vecta1.append(value)
        if key in vec2:
            vector_1.append(value)
    for key, value in vec2.items():
        vecta2.append(value)
        if key in vec1:
            vector_2.append(value)
    
    dot_product = np.dot(vector_1, vector_2)

    vector_1_mag = np.linalg.norm(vecta1)
    vector_2_mag = np.linalg.norm(vecta2)


    #return vector_2_mag*vector_1_mag
    return (dot_product/(vector_1_mag*vector_2_mag))

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
    #THIS IS NOT FINISHED OR TESTED!!! NEEDS WORK
    punctuation_to_remove = [",", "-", "--", ":", ";"]
    #seperators = [".", "!", "?"]

    file_contents = {}
    for filename in filenames:
        with open(filename, "r", encoding="latin1") as f:
            file_contents[filename] = f.read()
    
    for value in file_contents.values():
        for punc in punctuation_to_remove:
            value = value.replace(punc,"") #removing non essential punctuation
        
        value = split_into_sentences(value)

    #for value in file_contents.values():
    #    words = value.split() -> previous attempt



def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    pass


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    pass


weirdo = [["i", "am", "a", "sick", "man"], ["i", "am", "a", "spiteful", "man"], ["i", "am", "an", "unattractive", "man"], ["i", "believe", "my", "liver", "is", "diseased"], ["however", "i", "know", "nothing", "at", "all", "about", "my", "disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]


if __name__ == '__main__':

    #function tests
    print(cosine_similarity({"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6})) # shuld be ~0.70
    print(build_semantic_descriptors(weirdo)) # should be really long idk
    print(split_into_sentences("This is a sentence. This is another sentence. Genshin gooners are crazy! What the hell?")) #should look like weirdo