import csv
import codecs
import numpy as np
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd

data=pd.read_csv('googleplaystore.csv')
print(len(data))
data.dropna(how ='any', inplace = True)
print(len(data))
le = preprocessing.LabelEncoder()
le.fit(data['Category'])
data['Category']=le.transform(data['Category'])
le.fit(data['Type'])
data['Type']=le.transform(data['Type'])
le.fit(data['Content Rating'])
data['Content Rating']=le.transform(data['Content Rating'])
le.fit(data['Genres'])
data['Genres']=le.transform(data['Genres'])
le.fit(data['Rating'])
data['Rating']=le.transform(data['Rating'])
data['Installs'] = data['Installs'].apply(lambda x: x.replace('+', '') if '+' in str(x) else x)
data['Installs'] = data['Installs'].apply(lambda x: x.replace(',', '') if ',' in str(x) else x)
data['Installs'] = data['Installs'].apply(lambda x: int(x))
data['Size'] = data['Size'].apply(lambda x: str(x).replace('Varies with device', 'NaN') if 'Varies with device' in str(x) else x)
data['Size'] = data['Size'].apply(lambda x: str(x).replace('M', '') if 'M' in str(x) else x)
data['Size'] = data['Size'].apply(lambda x: str(x).replace(',', '') if 'M' in str(x) else x)
data['Size'] = data['Size'].apply(lambda x: float(str(x).replace('k', '')) / 1000 if 'k' in str(x) else x)
data['Size'] = data['Size'].apply(lambda x: float(x))
data['Installs'] = data['Installs'].apply(lambda x: float(x))
data['Price'] = data['Price'].apply(lambda x: str(x).replace('$', '') if '$' in str(x) else str(x))
data['Price'] = data['Price'].apply(lambda x: float(x))
data['Reviews'] = data['Reviews'].apply(lambda x: int(x))
data.dropna(how ='any', inplace = True)
#data['Rating'].describe()
#data.head(5)
data= data.drop('App', 1)
data= data.drop('Last Updated', 1)
data= data.drop('Current Ver', 1)
data= data.drop('Android Ver', 1)
#print(data.head(5))
target=data['Rating'].apply(lambda x: int(x))
data= data.drop('Rating', 1)

#data.head(5)

train_data = np.array(data)
train_x_list=train_data.tolist()
target_data = np.array(target)
target_y_list=target_data.tolist()
train = train_x_list[:len(train_x_list)//2]
train_y=target_y_list[:len(target_y_list)//2]
test = train_x_list[len(train_x_list)//2:]
test_y=target_y_list[len(target_y_list)//2:]


knn = KNeighborsClassifier(n_neighbors=33)
knn.fit(train, train_y)

iris_y_predict = knn.predict(test)
probility=knn.predict_proba(test)
#neighborpoint=knn.kneighbors(iris_x_test[-1],5,False)
score=knn.score(test,test_y,sample_weight=None)

print(score)