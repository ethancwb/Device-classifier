import dns_data_processor
import  pandas as pd
from sklearn.tree import DecisionTreeClassifier ,export_graphviz
from sklearn.metrics import accuracy_score,confusion_matrix
from os import walk
import  numpy as np
import matplotlib.pyplot as plt
import sys
from sklearn import linear_model

Y_train=set()
X_train=pd.DataFrame(columns=["Device Mac"])
X_train.set_index("Device Mac")
files = []
path='E:\\MonIOTr\\'
for (dirpath, dirnames, filenames) in walk(path):
        files.extend(filenames)
        break


for each in files:
        val= each.split("-")

        if len(val)>3:
                Y_train.add( "-".join(val[0:6]))
        else:
                print(each)
                Y_train.add(each.split("-")[0])
print(Y_train)

Y_Train=set()
for each in Y_train:
        dns = path+each+'-dns.csv'
        http = path+each+'-http.csv'

        try:
                df = pd.read_csv(dns,error_bad_lines=False,sep='\t')
                df_http = pd.read_csv(http,error_bad_lines=False,sep='\t')
                if df.shape[0]!=0 or df_http.shape[0]!=0:
                        Y_Train.add(each)
                print()
                fe_obj = dns_data_processor.data_feature_extractor(df,df_http)
                features_dict=fe_obj.formatted_output()
                for obj in features_dict:
                        if len(features_dict[obj])>0 and isinstance(features_dict[obj],dict):
                                for i,val in features_dict[obj].items():
                                        X_train.ix[each,i]=1
        except:
                pass


X_train=X_train.fillna(0)
features_list=list(X_train.columns.values)
X_train=X_train.as_matrix()
X_Test=pd.DataFrame(columns=features_list)


y_True=set()
for each in Y_train:
        dns = path+each+'-test-dns.csv'
        http = path+each+'-test-http.csv'

        try:
                df = pd.read_csv(dns,error_bad_lines=False,sep='\t')
                df_http = pd.read_csv(http,error_bad_lines=False,sep='\t')
                if df.shape[0]!=0 or df_http.shape[0]!=0:
                        y_True.add(each)

                fe_obj = dns_data_processor.data_feature_extractor(df,df_http)
                features_dict=fe_obj.formatted_output()

                for obj in features_dict:

                        if len(features_dict[obj])>0 and isinstance(features_dict[obj],dict):

                                for i,val in features_dict[obj].items():

                                        if i in features_list:
                                                X_Test.ix[each,i]=1

        except:
                pass

X_Test=X_Test.fillna(0)

X_Test=X_Test.as_matrix()
dt = linear_model.LogisticRegression()
#dt = DecisionTreeClassifier(random_state=99)

dt.fit(X_train, list(Y_Train))

y_pred=dt.predict(X_Test)

with open("fruit_classifier.txt", "w") as f:
        f = export_graphviz(dt, out_file=f)


cnf_matrix = confusion_matrix(list(y_True), y_pred)
np.set_printoptions(precision=2)
print(cnf_matrix)
