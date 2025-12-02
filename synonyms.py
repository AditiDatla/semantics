'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 20, 2023.
'''

import math

#normalize the vector
def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as 
    described in the handout for Project 3.
    '''
    sum_of_squares = 0.0  
    #calculate sum of squares for each value in the dict
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)

#compute the dot product of each vector using the normalized values and return cosine similarity
def cosine_similarity(vec1, vec2):
    # dot product over matching keys
    dot = 0.0
    # iterate through the keys (unqiue words) in the given vector
    for k, v in vec1.items():
        #only calculate dot product if the key exists in the given text (vec2)
        if k in vec2:
            dot += v * vec2[k]

    n1 = norm(vec1)
    n2 = norm(vec2)
    if n1 == 0 or n2 == 0:
        return -1.0
    return dot / (n1 * n2)

#builds a dictionary of unique words from each "sentence" from the lists of words in sentences
def build_semantic_descriptors(sentences):
    word_occ = {}

    for sentence in sentences:
        unique_words = list(set(sentence))

        for word in unique_words:
            #initialize the word in the dictionary if not already present
            if word not in word_occ:
                word_occ[word] = {}

            #count occurrences of duplicate words in the same sentence
            for other in unique_words:
                if other != word: 
                    word_occ[word][other] = word_occ[word].get(other, 0) + 1

    return word_occ

#split text into sentences based on punctuation
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

#build a dictionary of unique words from files
def build_semantic_descriptors_from_files(filenames):
    punctuation_to_remove = [",", "-", "--", ":", ";"]
    descriptors = {}

    #read all files, concatenate their text and remove capitalization
    file_text = ""
    for filename in filenames:
        with open(filename, "r", encoding="latin1") as f:
            file_text += " " + f.read().lower()

    # Remove non-essential punctuation
    for p in punctuation_to_remove:
        file_text = file_text.replace(p, " ")

    #split text into sentences and build semantic descriptors
    sentences = split_into_sentences(file_text)
    descriptors = build_semantic_descriptors(sentences)

    return descriptors

#find the most similar word from the choices based on the similarity function
def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    #initialize best choice and similarity
    best_choice = choices[0]
    best_sim = -1

    #loop through all choices to find the most similar word
    for i in range(len(choices)):
        choice = choices[i]
        
        if word not in semantic_descriptors or choice not in semantic_descriptors:
            sim = -1
        else:
            #compute similarity of the two words
            sim = similarity_fn(semantic_descriptors[word], semantic_descriptors[choice])

        #update best choice if current similarity is greater
        if sim > best_sim:
            best_sim = sim
            best_choice = choice
    
    return best_choice

#run similarity test on the given file
def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    total = 0
    correct = 0

    #read the test file line by line
    with open(filename, "r", encoding="latin1") as f:
        for line in f:
            parts = line.split()

            #extract the word, answer, and options from the line
            word = parts[0]
            answer = parts[1]
            options = parts[2:]

            #get the guessed word using the most similar word function
            guess = most_similar_word(word, options, semantic_descriptors, similarity_fn)

            total += 1
            if guess == answer:
                correct += 1

    #calculate and return the percentage of correct guesses
    if total == 0:
        return 0.0
    else:
        return ((correct / total) * 100.0)


# Example usage
weirdo = [["i", "am", "a", "sick", "man"], ["i", "am", "a", "spiteful", "man"], ["i", "am", "an", "unattractive", "man"], ["i", "believe", "my", "liver", "is", "diseased"], ["however", "i", "know", "nothing", "at", "all", "about", "my", "disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]


if __name__ == '__main__':
    #test variables from Notes from the Underground
    word_of_choice = "man"
    mychoices = ['i', 'am', 'a']
    my_descriptors = build_semantic_descriptors(weirdo)

    #test the test case file testytesty.txt
    sem_descriptors = build_semantic_descriptors_from_files(['semanticssubject1.txt', 'semanticssubject2.txt']) 
    res = run_similarity_test('testytesty.txt', sem_descriptors, cosine_similarity) 
    print(res, "% of the guesses were correct") #percantage should be between 67.5% and 72.5%


