from sklearn import tree
import configuration
import pickle

modelpath = configuration.Model_loc
alg = "RBF"

filename = modelpath + 'model_' + alg
with open(filename, 'rb') as f:
    model = pickle.load(f)

i_tree = 0
for tree_in_forest in model.estimators_:
   with open('tree_' + str(i_tree) + '.dot', 'w') as my_file:
       my_file = tree.export_graphviz(tree_in_forest, out_file = my_file)
   i_tree = i_tree + 1