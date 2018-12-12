import ID3, parse, random
import matplotlib.pyplot as plt
import numpy as np

def testID3AndEvaluate():
  data = [dict(a=1, b=0, Class=1), dict(a=1, b=1, Class=1)]
  tree = ID3.ID3(data, 0)
  if tree != None:
    ans = ID3.evaluate(tree, dict(a=1, b=0))
    if ans != 1:
      print("ID3 test failed.")
    else:
      print("ID3 test succeeded.")
  else:
    print("ID3 test failed -- no tree returned")

def testPruning():
  # data = [dict(a=1, b=1, c=1, Class=0), dict(a=1, b=0, c=0, Class=0), dict(a=0, b=1, c=0, Class=1), dict(a=0, b=0, c=0, Class=1), dict(a=0, b=0, c=1, Class=0)]
  # validationData = [dict(a=0, b=0, c=1, Class=1)]
  data = [dict(a=0, b=1, c=1, d=0, Class=1), dict(a=0, b=0, c=1, d=0, Class=0), dict(a=0, b=1, c=0, d=0, Class=1), dict(a=1, b=0, c=1, d=0, Class=0), dict(a=1, b=1, c=0, d=0, Class=0), dict(a=1, b=1, c=0, d=1, Class=0), dict(a=1, b=1, c=1, d=0, Class=0)]
  validationData = [dict(a=0, b=0, c=1, d=0, Class=1), dict(a=1, b=1, c=1, d=1, Class = 0)]
  tree = ID3.ID3(data, 0)
  ID3.prune(tree, validationData)
  if tree != None:
    ans = ID3.evaluate(tree, dict(a=0, b=0, c=1, d=0))
    if ans != 1:
      print("pruning test failed.")
    else:
      print("pruning test succeeded.")
  else:
    print("pruning test failed -- no tree returned.")


def testID3AndTest():
  trainData = [dict(a=1, b=0, c=0, Class=1), dict(a=1, b=1, c=0, Class=1), 
  dict(a=0, b=0, c=0, Class=0), dict(a=0, b=1, c=0, Class=1)]
  testData = [dict(a=1, b=0, c=1, Class=1), dict(a=1, b=1, c=1, Class=1), 
  dict(a=0, b=0, c=1, Class=0), dict(a=0, b=1, c=1, Class=0)]
  tree = ID3.ID3(trainData, 0)
  fails = 0
  if tree != None:
    acc = ID3.test(tree, trainData)
    if acc == 1.0:
      print("testing on train data succeeded.")
    else:
      print("testing on train data failed.")
      fails = fails + 1
    acc = ID3.test(tree, testData)
    if acc == 0.75:
      print("testing on test data succeeded.")
    else:
      print("testing on test data failed.")
      fails = fails + 1
    if fails > 0:
      print("Failures: ", fails)
    else:
      print("testID3AndTest succeeded.")
  else:
    print("testID3andTest failed -- no tree returned.")	

# inFile - string location of the house data file
def testPruningOnHouseData(inFile):
  withPruning = []
  withoutPruning = []
  data = parse.parse(inFile)
  for i in range(10):
    random.shuffle(data)
    train = data[:len(data)//2]
    valid = data[len(data)//2:3*len(data)//4]
    test = data[3*len(data)//4:]

    tree = ID3.ID3(train, 4)
    acc = ID3.test(tree, train)
    print("training accuracy: ",acc)
    acc = ID3.test(tree, valid)
    print("validation accuracy: ",acc)
    acc = ID3.test(tree, test)
    print("test accuracy: ",acc)
  
    ID3.prune(tree, valid)
    acc = ID3.test(tree, train)
    print("pruned tree train accuracy: ",acc)
    acc = ID3.test(tree, valid)
    print("pruned tree validation accuracy: ",acc)
    acc = ID3.test(tree, test)
    print("pruned tree test accuracy: ",acc)
    withPruning.append(acc)

    tree = ID3.ID3(train+valid, 4)
    acc = ID3.test(tree, test)
    print("no pruning test accuracy: ",acc)
    withoutPruning.append(acc)
  print(withPruning)
  print(withoutPruning)
  print("average with pruning",sum(withPruning)/len(withPruning)," without: ",sum(withoutPruning)/len(withoutPruning))



def SimilarOnHouseData(data, trainSize):
    res=[]
    withPruning = []
    withoutPruning = []
    trainPartSize=int(trainSize/2)
    validSize=int(3*trainSize/4)
    for i in range(100):
        random.shuffle(data)
        train = data[:trainPartSize]
        valid = data[trainPartSize:validSize]
        test = data[validSize:]

        tree = ID3.ID3(train, 'democrat')
        acc = ID3.test(tree, train)
        acc = ID3.test(tree, valid)
        acc = ID3.test(tree, test)

        ID3.prune(tree, valid)
        acc = ID3.test(tree, train)
        acc = ID3.test(tree, valid)
        acc = ID3.test(tree, test)
        withPruning.append(acc)

        tree = ID3.ID3(train + valid, 'democrat')
        acc = ID3.test(tree, test)
        withoutPruning.append(acc)
    print("average with pruning", sum(withPruning) / len(withPruning), " without: ",sum(withoutPruning) / len(withoutPruning))
    res.append(sum(withPruning) / len(withPruning))
    res.append(sum(withoutPruning) / len(withoutPruning))
    return res

def graphtest(infile):
    data = parse.parse(infile)
    pruneRes=[]
    WithoutPruneRes=[]
    for trainSize in range(10,301,10):
        result=SimilarOnHouseData(data,trainSize)
        pruneRes.append(result[0])
        WithoutPruneRes.append(result[1])

    x_axis=np.arange(10,301,10)

    axes = plt.gca()
    axes.set_ylim([0.6, 1])

    plt.figure(1, dpi=50)
    plt.plot(x_axis, pruneRes, color='r',marker='.')
    plt.plot(x_axis, WithoutPruneRes, color='b', marker='.')
    labels=['average with pruning', 'average without pruning']
    plt.legend(labels,loc=4)
    plt.title('average accuracy between different training sizes')
    plt.xlabel('number of training examples')
    plt.ylabel('accuracy on test data')


    plt.show()