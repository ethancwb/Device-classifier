import pandas as pd
import configuration
import classifer
import pickle
from sklearn.metrics import accuracy_score,confusion_matrix,f1_score,recall_score,precision_score,classification_report,roc_auc_score,roc_curve
import numpy as np

def predict(testdata,modelpath,alg="SVM"):

    #print("The Algorithm used is" ,alg)
    filename = modelpath+'model_'+alg

    with open(filename, 'rb') as f:
        model = pickle.load(f)
    X_Test = pd.read_csv(testdata+"Test.csv", error_bad_lines=False).set_index("Unnamed: 0")
    print(len(X_Test.columns))
    Y_True=np.asarray(list(X_Test.index))
    X_Test=X_Test.as_matrix()

    Y_Pred=model.predict(X_Test)
    return Y_Pred,Y_True

def metrics(Y_Pred,Y_True):

    print ('Accuracy:', accuracy_score(Y_True, Y_Pred)*100)
    # print ('F1 score:', f1_score(Y_True, Y_Pred,average='micro'))
    # print ('Recall:', recall_score(Y_True, Y_Pred,average='micro'))
    # print ('Precision:', precision_score(Y_True, Y_Pred,average='micro'))
    # print ('\n clasification report:\n', classification_report(Y_True,Y_Pred))
    # print ('\n confussion matrix:\n',confusion_matrix(Y_True, Y_Pred))


if __name__ == "__main__":
    #Initializing the Training and Testing Data Frames
    testpath=configuration.Test_loc
    modelpath=configuration.Model_loc
    test_files=configuration.test_dataset
    parameter=False
    if not parameter:
        filename = modelpath+'features'
        with open(filename, 'rb') as f:
            features = pickle.load(f)

        Testfiles=classifer.readfiles(testpath)

        Y=classifer.y_values(Testfiles)

        classifer.processXY(Y,testpath,modelpath,test_files,type="Test",features=features)

    Y_Pred,Y_True=predict(test_files,modelpath,alg="RBF")
    print(Y_True,Y_Pred)

    metrics(Y_Pred,Y_True)

