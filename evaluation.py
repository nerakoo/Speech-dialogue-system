# This is the evaluation file for three metrics
# EO, RC, CT
# -----------------------2024.2.17-------------------------
from __future__ import division

def examine_overlap(word_array1, word_array2):
    """
    examine whether there exists overlapping
    arr1 length >= arr2 length
    """
    if len(word_array1) < len(word_array2):
        arr1 = word_array1
        word_array1 = word_array2
        word_array2 = arr1

    for i in range(len(word_array2)):
        if word_array2[i] != word_array1[i]:
            return False

    return True


def fill_list(my_list, length, fill=None):
    if len(my_list) >= length:
        return my_list
    else:
        return my_list + (length - len(my_list)) * [fill]


def estimate_EO(word2word_sentence, incremental_sentence_word2word):
    """
    EO = unnecessary_edit / overall_edit, EO ∈ [0,1]
    Lower EO value represents higher efficiency in making necessary operations

    example:
    Edit number in total: 9
    Edit number necessary: 7
    Edit number unnecessary: 2

    EO = 0.2222222222222222
    """
    necessary_edit = len(word2word_sentence)
    overall_edit = 0
    index = 0
    incremental_sentence_word2word.reverse()

    for i in range(len(word2word_sentence)):
        old_word = word2word_sentence[index]
        for unit in incremental_sentence_word2word:
            unit = fill_list(unit, len(word2word_sentence), " ")
            # print(unit)
            if unit[index] != old_word:
                overall_edit = overall_edit + 1
                old_word = unit[index]
        index = index + 1
    incremental_sentence_word2word.reverse()
    overall_edit = overall_edit+len(incremental_sentence_word2word[0]) # FOR the first word adding!!!!
    unnecessary_edit = overall_edit-necessary_edit
    # print("Edit number in total:", overall_edit)
    # print("Edit number necessary:", necessary_edit)
    # print("Edit number unnecessary:", overall_edit-necessary_edit)
    EO = unnecessary_edit / overall_edit
    return EO

def estimate_RC(word2word_sentence, incremental_sentence_word2word):
    """
    RC = overlap sentences / overall sentences, RC ∈ [0,1]
    Higher RC value means that the system outputs were most of the time correct prefixes of the non-incremental output

    example:
    overlap = 16
    overall = 17

    RC = 0.9411764705882353
    """
    overlap = 0
    overall = len(incremental_sentence_word2word)
    for unit in incremental_sentence_word2word:
        flag = examine_overlap(word2word_sentence, unit)
        if flag:
            overlap = overlap + 1
    RC = overlap / overall
    # print(overall)
    # print(overlap)
    return RC


def estimate_CT(word2word_sentence, incremental_sentence_word2word):
    """
    CT =  Sum the FD-FO values of all words / total number of words in output sentences
    The lower CT value is, the sooner final decisions were made

    example:

    Occurance: can [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    Occurance time: can 17
    FO: can 0
    FD: can 0

    Occurance: you [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    Occurance time: you 17
    FO: you 0
    FD: you 0

    Occurance: book [7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    Occurance time: book 10
    FO: book 7
    FD: book 7

    Occurance: a [10, 11, 12, 13, 14, 15, 16]
    Occurance time: a 7
    FO: a 10
    FD: a 10

    Occurance: restaurant [12, 13, 14, 15, 16]
    Occurance time: restaurant 5
    FO: restaurant 12
    FD: restaurant 12

    Occurance: for [14, 15, 16]
    Occurance time: for 3
    FO: for 14
    FD: for 14

    Occurance: me [15, 16]
    Occurance time: me 2
    FO: me 15
    FD: me 15

    CTscore = 0.0
    """
    index = 0
    occurance = []
    FD_flag = False
    CT = 0
    FD = 0
    FO = 0
    for word in word2word_sentence:
        for unit in incremental_sentence_word2word:
            if word in unit:
                occurance.append(index)
            index = index + 1
        # print("Occurance:", word, occurance)
        iterations = max(occurance) - min(occurance) + 1
        # print("Occurance time:", word, iterations)

        FO = min(occurance)
        # print("FO:", word, FO)

        occurance.reverse()
        minus = 0
        for i in range(len(occurance)):
            if occurance[i] != len(incremental_sentence_word2word) - 1 - minus:
                FD = occurance[i - 1]
                # print("FD:", word, FD)
                FD_flag = True
                break
            minus = minus + 1
        if not FD_flag:
            FD = min(occurance)
            # print("FD:", word, min(occurance))
        index = 0
        occurance = []
        FD_flag = False
        CT = (FD - FO) / iterations + CT

    CTscore = CT / len(word2word_sentence)

    return CTscore


def test():
    sentences = ['can you book a restaurant for me']
    incremental_sentence = ['can you', 'can you put', 'can you', 'can you', 'can you', 'can you', 'can you', 'can you book', 'can you book', 'can you book', 'can you book a', 'can you book a', 'can you book a restaurant', 'can you book a restaurant', 'can you book a restaurant for', 'can you book a restaurant for me', 'can you book a restaurant for me']
    word_by_word = []
    incre_word_by_word = []
    for sentence in sentences:
        word_by_word.append(sentence.split())

    print(word_by_word) # [['whats', 'the', 'weather', 'like', 'today']]

    for incre_sentence in incremental_sentence:
        incre_word_by_word.append(incre_sentence.split())
    print(incremental_sentence)

    EO = estimate_EO(word_by_word[0], incre_word_by_word)
    print("============= EO: ", EO)

    RC = estimate_RC(word_by_word[0], incre_word_by_word)
    print("============= RC: ", RC)

    CTscore = estimate_CT(word_by_word[0], incre_word_by_word)
    print("============= CTscore: ", CTscore)


# test()