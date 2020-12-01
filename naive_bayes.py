

"""
This is the main entry point for MP3. You should only modify code
within this file and the last two arguments of line 34 in mp3.py
and if you want-- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
from collections import Counter
import math

def naiveBayesHelp(train_labels, train_set):
    i = len(train_set) - 1
    countP = Counter()
    countN = Counter()
    sumP = 0
    sumN = 0
    stop = ['a', 'an', 'and', 'but', 'the', 'so']
    while i >= 0:
        filtered = []
        for j in train_set[i]:
            if j in stop: continue
            filtered.append(j.lower())
        if train_labels[i] > 0:
            sumP += len(filtered)
            countP.update(filtered)
        else:
            sumN += len(filtered)
            countN.update(filtered)
        i -= 1

    return countP, countN, sumP, sumN, len(countP.keys()), len(countN.keys()), 0.0, 0.0, []


def naiveBayes(train_set, train_labels, dev_set, smoothing_parameter=0.8, pos_prior=0.8):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was  positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    smoothing_parameter - The smoothing parameter --laplace (1.0 by default)
    pos_prior - The prior probability that a word is positive. You do not need to change this value.
    """
    # TODO: Write your code here
    # return predicted labels of development set

    countP, countN, addP, sumN, uniqueP, uniqueN, posP, posN, output = naiveBayesHelp(train_labels, train_set)
    stop = ['a', 'an', 'and', 'but', 'the', 'so']
    for listofwords in dev_set:
        for word in listofwords:
            word1 = word.lower()
            if word1 in stop: continue
            #if word1 not in countN
               # uniqueP += 1
            #    uniqueN += 1
            if word1 == listofwords[1]:
                posP += math.log((smoothing_parameter + countP[word1]) * (1 / ((uniqueP +1) * smoothing_parameter + addP)))
                posP += math.log(pos_prior)
                posN += math.log((smoothing_parameter + countN[word1]) * (1 / ((uniqueN +1) * smoothing_parameter + sumN)))
                posN += math.log(1 - pos_prior)
            else:
                posP += math.log((smoothing_parameter + countP[word1]) * (1 / ((uniqueP )*smoothing_parameter + addP)))
                posN += math.log((smoothing_parameter+countN[word1]) * (1 / ((uniqueN )*smoothing_parameter + sumN)))
        if posP <= posN: output.append(0)
        else: output.append(1)
        posP = 0
        posN = 0
    return output

def bigramBayes(train_set, train_labels, dev_set, unigram_smoothing_parameter=0.99, bigram_smoothing_parameter=0.4, bigram_lambda=0.01,pos_prior=0.8):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    unigram_smoothing_parameter - The smoothing parameter for unigram model (same as above) --laplace (1.0 by default)
    bigram_smoothing_parameter - The smoothing parameter for bigram model (1.0 by default)
    bigram_lambda - Determines what fraction of your prediction is from the bigram model and what fraction is from the unigram model. Default is 0.5
    pos_prior - The prior probability that a word is positive. You do not need to change this value.
    """
    # TODO: Write your code here
    # return predicted labels of development set using a bigram model
    countP, countN, addP, sumN, uniqueP, uniqueN, posP, posN, output = naiveBayesHelp(train_labels, train_set)
    stop = ['a', 'an', 'and', 'but', 'the', 'so']
    bigramP = Counter()
    bigramN = Counter()
    bipostP = 0
    bipostN = 0
    sumPbi = 0
    sumNbi = 0

    i = 0
    while i < len(train_labels):
            temp = []
            j = 0
            while j < len(train_set[i]) - 1:
                temp.append(train_set[i][j].lower() + train_set[i][j + 1].lower())
                j += 1
            #maybe check next as well
            if train_labels[i] > 0:
                bigramP.update(temp)
                sumPbi += len(temp)
            else:
                bigramN.update(temp)
                sumNbi += len(temp)
            i += 1

    for listofwords in dev_set:
        for word in listofwords:
            word1 = word.lower()
            if word1 in stop: continue
            # if word1 not in countN
            # uniqueP += 1
            #    uniqueN += 1
            if word1 == listofwords[1]:
                posP += math.log(
                    (unigram_smoothing_parameter + countP[word1]) * (1 / ((uniqueP + 1) * unigram_smoothing_parameter + addP)))
                posP += math.log(pos_prior)
                posN += math.log(
                    (unigram_smoothing_parameter + countN[word1]) * (1 / ((uniqueN + 1) * unigram_smoothing_parameter + sumN)))
                posN += math.log(1 - pos_prior)
            else:
                posP += math.log((unigram_smoothing_parameter + countP[word1]) * (1 / ((uniqueP) * unigram_smoothing_parameter + addP)))
                posN += math.log((unigram_smoothing_parameter + countN[word1]) * (1 / ((uniqueN) * unigram_smoothing_parameter + sumN)))
        # maybe do just bigram lambda for p
        k = 0

        while k < len(listofwords) - 1:
            phrase = listofwords[k].lower() + listofwords[k + 1].lower()
            # if word1 not in countN
            # uniqueP += 1
            #    uniqueN += 1
            if k == 0:
                bipostP += math.log((bigram_smoothing_parameter +bigramP[phrase]) * (bigram_smoothing_parameter * len(bigramP.keys()) + sumPbi))
                bipostP += math.log(pos_prior)
                bipostN += math.log((bigram_smoothing_parameter +bigramN[phrase]) * (bigram_smoothing_parameter * len(bigramN.keys()) + sumNbi))
                bipostN += math.log(1 - pos_prior)
            else:
                bipostP += math.log((bigram_smoothing_parameter +bigramP[phrase]) * (1 / (bigram_smoothing_parameter * len(bigramP.keys()) + sumPbi)))
                bipostN += math.log((bigram_smoothing_parameter +bigramN[phrase]) * (1 / (bigram_smoothing_parameter * len(bigramN.keys()) + sumNbi)))
            k += 1
        if (posP * (1 - bigram_lambda) + bipostP * bigram_lambda) >= (posN * (1 - bigram_lambda) + bipostN * bigram_lambda):
            output.append(1)
        else:
            output.append(0)
        posP = 0
        posN = 0
        bipostP = 0
        bipostN = 0
    return output