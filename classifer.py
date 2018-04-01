import dns_data_processor
import  pandas as pd
from sklearn.tree import DecisionTreeClassifier ,export_graphviz

from os import walk,path
import  numpy as np
import configuration
import pickle
import glob
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from subprocess import call
from sklearn.externals.six import StringIO
from IPython.display import Image
from sklearn.tree import export_graphviz
import pydotplus

import os


#List all the training files

def readfiles(trainpath):

        files=[]
        for (dirpath, dirnames, filenames) in walk(trainpath):
                files.extend(filenames)
                break
        return files
def y_values(files):

        Y_train=set()
        for each in files:
                val= each.split("-")

                if len(val)>3:
                        Y_train.add( "-".join(val[0:6]))
                else:
                        Y_train.add(each.split("-")[0])
        return Y_train

def processXY(Y,trainpath,modelpath,train_files,type="Train",features="None"):
        if type=="Train":
                X=pd.DataFrame(columns=["Device Mac"])
                X.set_index("Device Mac")
                tail_dns='-dns.csv'
                tail_http='-http.csv'
                tail_dstport='-dstport.csv'
                tail_general='-general.csv'
                tail_payload='-payload.csv'

        elif type=="Test":
                X=pd.DataFrame(columns=features)
                tail_dns='-test-dns.csv'
                tail_http='-test-http.csv'
                tail_dstport='-test-dstport.csv'
                tail_general='-test-general.csv'
                tail_payload='-test-payload.csv'
        for each in Y:

                dns = trainpath+each+tail_dns
                http = trainpath+each+tail_http

                dstport = trainpath+each+tail_dstport
                general = trainpath+each+tail_general
                payload = trainpath+each+tail_payload

                try:

                        print("Processing train data for device",each)
                        df = pd.read_csv(dns, error_bad_lines=False, sep='\t', low_memory=False)
                        df_http = pd.read_csv(http, error_bad_lines=False, sep='\t', low_memory=False)
                        df_dstport = pd.read_csv(dstport, error_bad_lines=False, sep='\t', low_memory=False)
                        df_general = pd.read_csv(general, error_bad_lines=False, sep='\t', low_memory=False)
                        df_payload = pd.read_csv(payload, error_bad_lines=False, sep='\t', low_memory=False)


                        d = dns_data_processor.data_feature_extractor(df, df_http, df_general, df_dstport, df_payload)
                        features_dict=d.formatted_output()
                        print("Number of featueres for Device:-",len(features_dict))

                        for obj in features_dict:

                                if obj=="others":
                                        if len(features_dict[obj])>0 and isinstance(features_dict[obj],dict):

                                                for i,val in features_dict[obj].items():
                                                        if type=="Train":
                                                                X.ix[each,i]=val
                                                        elif type=="Test":
                                                                if i in features:
                                                                        X.ix[each,i]=val

                                else:
                                        if len(features_dict[obj])>0 and isinstance(features_dict[obj],dict):

                                                for i,val in features_dict[obj].items():
                                                        if type=="Train":
                                                                X.ix[each,i]=1
                                                        elif type=="Test":
                                                                if i in features:
                                                                        X.ix[each,i]=1

                except Exception as e:
                        print (str(e))


        X=X.fillna(0)

        X.to_csv(train_files+type+".csv")

        if type=="Train":
                features_list=list(X.columns.values)
                filename = modelpath+"features"
                pickle.dump(features_list, open(filename, 'wb'))



def gen_model(train,path,alg="DT",modeltype="Multiclass"):

        print("The Algorithm used is" ,alg)
        X_Train = pd.read_csv(train+"Train.csv", error_bad_lines=False).set_index("Unnamed: 0")

        Y_Train=np.asarray(list(X_Train.index))
        X_Train=X_Train.as_matrix()

        if alg=="DT":
                model = DecisionTreeClassifier(random_state=99)

        if alg=="LG":
                model = LogisticRegression(C=1., solver='lbfgs')
        if alg=="SVM":
                print(alg)
                model= svm.SVC(decision_function_shape='ovo')

        model.fit(X_Train,Y_Train)
        if alg=="DT":
                print(alg)
                dotfile = open("dtree2.dot", 'w')
                export_graphviz(model, out_file=dotfile,
                                filled=True, rounded=True,
                                special_characters=True)
                dotfile.close()


        filename = path+'model_'+alg
        pickle.dump(model, open(filename, 'wb'))


if __name__ == "__main__":
        #Initializing the Training and Testing Data Frames
        train_files=configuration.train_dataset
        trainpath=configuration.Train_loc
        modelpath=str(configuration.Model_loc)
        #Set to False to create a new set of traning data and model,Set true to only generate a new model with existing data
        parameters=False
        if not parameters:
                trainfiles=readfiles(trainpath)
                Y=y_values(trainfiles)
                processXY(Y,trainpath,modelpath,train_files)

        gen_model(train_files,modelpath,alg="DT")



