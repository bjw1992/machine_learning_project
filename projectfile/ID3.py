from node import Node
from collections import Counter
import copy
import math

def ID3(examples, default):
    '''
    Takes in an array of examples, and returns a tree (an instance of Node)
    trained on the examples.  Each example is a dictionary of attribute:value pairs,
    and the target class variable is a special attribute with the name "Class".
    Any missing attributes are denoted with a value of "?"
    '''
    completeData = missingProcess(examples)
    classify_values = [data['Class'] for data in completeData]

    if len(completeData) == 0:
        return Node('Class', {}, default, True)

    # only have one classfication group
    elif classify_values.count(classify_values[0]) == len(classify_values):
        return Node('Class', {}, classify_values[0], True)

    # only have one attribute
    elif len(completeData[0]) == 1:
        return Node('Class', {}, mostCommon(completeData, 'Class'), True)

    else:
        best = chooseAttr(completeData)  # this is the best attribute, attribute can not be the 'Class'
        root = Node(best, {}, None, False)

        for value in bestAttrValues(completeData, best):
            newData = getExamplesWithValue(completeData, best, value)
            subtree = ID3(newData, mostCommon(newData, 'Class'))
            root.children[value] = subtree
    return root


# according to the gainfeature, find attr which has the maximum gainfeature
def chooseAttr(examples):
    # max_attr = list(examples[0])[0]
    # if max_attr == 'Class' and len(examples[0].keys()) > 1:
    #     max_attr = list(examples[0])[1]

    max = 0
    max_attr = ''
    for key in examples[0].keys():

        if key != 'Class':
            gain = gainfeature(examples, key)
            if max <= gain:
                max = gain
                max_attr = key

    return max_attr


def test(node, examples):
    '''
    Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
    of examples the tree classifies correctly).
    '''
    examples = missingProcess(examples)
    correct = 0.0
    for i in examples:
        if evaluate(node, i) == i['Class']:
            correct += 1.0

    result=correct / len(examples)
    return result

def evaluate(node, example):

    '''
    Takes in a tree and one example.  Returns the Class value that the tree
    assigns to the example.
    '''
    if node == None:
        return example['Class']
    if node.get_children() == {}:
        result = node.get_label()
        return result
    return evaluate(node.get_child(example[node.get_atrribute()]), example)


def missingProcess(examples):
    '''
    For each attribute, find the most common value for this
    :param example: [dict(a=1, b=0, Class=1),
                     dict(a=1, b=0, Class=1)
                     dict(a=0, b=1, Class=1)]
    :return: dict(a=1, b=0)
    '''
    commonDic = {}
    for key in examples[0].keys():
        if key != "Class":
            commonDic[key] = mostCommon(examples, key)

    # update the examples again
    for example in examples:
        for key in example.keys():
            if example[key] == 'NaN':
                example[key] = commonDic[key]

    return examples


def mostCommon(examples, key):
    valueDic = {}
    #templen=len(examples)
    #for i in range(templen):
        #if 'Android Ver' not in examples[i].keys():
            #print(i)
    values = [example[key] for example in examples]
    # for each key, make a dict to store all their value and its frequence
    for v in values:
        if v in valueDic:
            valueDic[v] += 1.0
        else:
            valueDic[v] = 1.0

    # return the max frequence's value
    max_value = ''
    max = 0.0
    for value in valueDic.keys():
        if max < valueDic.get(value):
            max = valueDic[value]
            max_value = value
    return max_value


def entropy(examples):
    data = [example['Class'] for example in examples]
    index = {}
    for i in data:
        if i not in index:
            index[i] = 1
        else:
            index[i] += 1
    result = 0.0
    for j in index:
        result += index[j] / len(data) * (math.log2(index[j] / len(data)))
    return result * -1

def gainfeature(examples,attri):
    data = [example[attri] for example in examples]
    index = {}
    for i in data:
        if i not in index:
            index[i] = 1
        else:
            index[i] += 1
    result = 0.0
    for j in index:
        testexample = [example for example in examples if example[attri] == j]
        result += index[j] / len(data) * entropy(testexample)
    result = entropy(examples) - result
    return result

def getExamplesWithValue(data, attribute, value):
    '''
    Takes in a complete set of examples, the target attribute and the value
    find all examples that the attribute' field is equal to value
    :param data:
    :param attribute:
    :param value:
    :return: array of dictionary
    '''
    # res = []
    # for example in data:
    #     if example[attribute] == value:
    #         res.append(example)
    # return res
    res = []
    for example in data:
        if example[attribute] == value:
            newExample = {}
            for key, val in example.items():
                if key != attribute:
                    newExample[key] = val
            res.append(newExample)
    return res

# find all different values of attribute in examples
def bestAttrValues(examples, attribute):
    '''
    Takes in a complete set of examples and the target attribute, find all the unique
    values in the attribute
    :param examples: list of dictionary
    :param attribute:
    :return: a list of values
    '''
    res = []
    for data in examples:
        if data[attribute] not in res:
            res.append(data[attribute])

    return res


def prune(node, examples):
    '''
    Takes in a trained tree and a validation set of examples.  Prunes nodes in order
    to improve accuracy on the validation data; the precise pruning strategy is up to you.
    '''
    return pruneWithroot(node, examples, node)

def pruneWithroot(node, examples, root):
    if node.isLeaf == True:
        return node

    if isChildAllLeaf(node):
        currentScore = test(root, examples)
        label = mostFreLabel(node)
        node.set_to_leaf(label)
        AfterScore = test(root, examples)
        if currentScore > AfterScore:
            node.recoveprune()
        return node
    else:
        for child in node.children:
            evaluateNode = pruneWithroot(node.children[child], examples, root)
            node.children[child] = evaluateNode
        return node

def isChildAllLeaf(node):
    '''
    for the given node, check the node position, is the position of node could be pruned?
    :param node:
    :return: True or False
    '''
    test_children = node.get_children()
    for child in test_children.values():
        if not child.isLeaf:
            return False
    return True

def mostFreLabel(node):
    labelList = [child.get_label() for child in node.get_children().values()]
    mostfrelabel = Counter(labelList).most_common(1)
    return mostfrelabel[0][0]