# SeekTruth.py : Classify text objects into two categories
#Teammates:
#Akhil Yenisetty: nyeniset,Prasad hegde: phegde,Hanish Chidipothu: hachid
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#
def classifier(train_data, test_data):
    # This is just dummy code -- put yours here!
    
    special_chars = {'~', ':', "'", '+', '[', '\\', '@', '^', '{', '%', '(', '-', '"', '*', '|', ',', '&', '<', '`', '}', '.', '_', '=',
     ']', '!', '>', ';', '?', '#', '$', ')', '/'}
    numbers = {'1','2','3','4','5','6','7','8','9','0'}
    bag_of_words = []
    dict_of_words = {}
    for i in range(len(train_data["objects"])):
        for sp in special_chars:
            train_data["objects"][i] = train_data["objects"][i].replace(sp," "+sp+" ")
        for num in numbers:
            train_data["objects"][i] = train_data["objects"][i].replace(num,"")
        bag_of_words.extend(words.strip().lower() for words in train_data["objects"][i].strip().split())
    bag_of_words = set(bag_of_words)
    
    
    for word in bag_of_words:
        true,deceptive = 0,0
        for i in range(len(train_data["objects"])):
            if word in train_data["objects"][i].lower():
                if train_data["labels"][i] == 'deceptive':
                    deceptive+=1
                elif train_data["labels"][i] == 'truthful':
                    true+=1
        tp = true/(true+deceptive)
        dp = deceptive/(true+deceptive)
        dict_of_words.update({word :(tp,dp)})
    
    label =[]
   
    for i in range(len(test_data["objects"])):
        for sp in special_chars:
            test_data["objects"][i] = test_data["objects"][i].replace(sp," "+sp+" ")
        words = []
        words.extend(word.strip().lower() for word in test_data["objects"][i].strip().split())
        prob_true = train_data["labels"].count("truthful")/(train_data["labels"].count("truthful")+train_data["labels"].count("deceptive"))
        prob_decep = train_data["labels"].count("deceptive")/(train_data["labels"].count("truthful")+train_data["labels"].count("deceptive"))
        for word in words:
            if word in bag_of_words:
                t,d = dict_of_words[word]
                if t!=0:
                    prob_true *= t
                if d!=0:
                    prob_decep *= d
        if prob_true/prob_decep >1:
            label.append("truthful")
        else:
           label.append("deceptive")
    return label
        


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
