import dns_data_processor
import  pandas as pd
from sklearn.tree import DecisionTreeClassifier ,export_graphviz
from sklearn.linear_model import LogisticRegression
import  subprocess
import  sys

Y_train=['24-fd-5b-2-1d-3a','fc-65-de-5f-15-a','40-4e-36-86-d0-28','18-b4-30-c8-d8-28','0-e-f3-3b-85-e5']
X_train=pd.DataFrame(columns=["Device Mac"])
X_train.set_index("Device Mac")

for each in Y_train:
        path = 'E:\\MonIOTr\\'+each+'-dns.csv'
        path__http = 'E:\\MonIOTr\\'+each+'-http.csv'


        try:
                df = pd.read_csv(path,error_bad_lines=False,sep='\t')
                df_http = pd.read_csv(path__http,error_bad_lines=False,sep='\t')
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

path = 'E:\\MonIOTr\\test-dns.csv'
path__http = 'E:\\MonIOTr\\test-http.csv'


try:
        df = pd.read_csv(path,error_bad_lines=False,sep='\t')
        df_http = pd.read_csv(path__http,error_bad_lines=False,sep='\t')

        fe_obj = dns_data_processor.data_feature_extractor(df,df_http)
        features_dict=fe_obj.formatted_output()

        for obj in features_dict:

                if len(features_dict[obj])>0 and isinstance(features_dict[obj],dict):

                        for i,val in features_dict[obj].items():

                                if i in features_list:
                                        X_Test.ix['0',i]=1

except:

        pass







X_Test=X_Test.fillna(0)

X_Test=X_Test.as_matrix()
dt = DecisionTreeClassifier(random_state=99)
dt.fit(X_train, Y_train)
#visualize_tree(dt,features_list )
print(dt.predict(X_Test))

#X_train.to_csv("Training.csv")

import graphviz
dot_data = export_graphviz(dt, out_file="sample.png")
graph=graphviz.Source(dot_data)
graph.render()





