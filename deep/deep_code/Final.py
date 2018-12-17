
from keras.models import Sequential
from keras.layers import Dense
import firebase_admin
from firebase_admin import credentials
import numpy
import tensorflow as tf
from firebase_admin import db

PAHT_CRED='../deep_code/Key.json'
URL_DB='https://pyrebasetest-92dd3.firebaseio.com/'
cred=credentials.Certificate(PAHT_CRED)
firebase_admin.initialize_app(cred,{'databaseURL':URL_DB})
ref=db.reference('/home/deep')

seed=0
numpy.random.seed(seed)
tf.set_random_seed(seed)

Data_set = numpy.loadtxt("../dataset/input.csv", delimiter=",")
Data_tester_set=numpy.loadtxt("../dataset/tester.csv", delimiter=",")

# week,h,m,s
X = Data_set[:,0:3]
Y = Data_set[:,3]

X_set=Data_tester_set[:,0:3]

model = Sequential()
model.add(Dense(100, input_dim=3, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
model.fit(X, Y, epochs=30, batch_size=10)

print("\n Accuracy: %.4f" % (model.evaluate(X, Y)[1]))
predict=model.predict(X_set)


i=0
c=0
# week,h,m,s
for x in predict:
    if x>0.6:
        predict[i]=1
    elif x>0.2:
        predict[i]=predict[i-1]
    else:
        predict[i]=0
    if predict[i]!=c:
        ref.update({(str(int(X_set[i,0]))+str(int(X_set[i,1]))+str(int(X_set[i,2]))):{'day':int(X_set[i,0]),'deep_num':1,'hour':int(X_set[i,1]),'minute':int(X_set[i,2]),'state':int(predict[i])}})
        c=predict[i]
    i=i+1

print(predict)