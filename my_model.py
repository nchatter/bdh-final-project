import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import KFold, ShuffleSplit


RANDOM_STATE = 545510477

irp_data = pd.read_csv("combined_irp_data.csv", header=0, sep=',')
oscar_data = pd.read_csv("combined_oscar_data.csv", header=0, sep=',')

combined_data = pd.merge(oscar_data, irp_data, how='inner', on=['term', 'course_num', 'section'])
dataframe = pd.DataFrame(combined_data)

dataframe = dataframe[~dataframe.time.str.contains("ABBR")]

dataframe['start'] = dataframe.apply(lambda row: row.time.split('-')[0].strip().split(':')[0] + row.time.split('-')[0].strip().split(':')[1][0:2], axis=1)


dataframe.to_csv('merged_test.csv', sep=',')

def my_classifier(X_train,Y_train,X_test):
	#TODO: complete this
    print(np.shape(X_train))
    print(np.shape(Y_train))
    print(np.shape(X_test))
    clf = SGDClassifier(loss="hinge", penalty="l2", max_iter=5)
    clf.fit(X_train, Y_train)
    pred = clf.predict(X_test)
    return pred

def classification_metrics(Y_pred, Y_true):
    accuracy = accuracy_score(Y_true, Y_pred)
    auc = roc_auc_score(Y_true, Y_pred)
    precision = precision_score(Y_true, Y_pred)
    recall = recall_score(Y_true, Y_pred)
    f1score = f1_score(Y_true, Y_pred)
    return accuracy,auc,precision,recall,f1score

def get_acc_auc_kfold(X,Y,k=5):
    accuracies = []
    aucs = []
    for train, test in KFold(n_splits = k, random_state = RANDOM_STATE).split(X):
        Y_pred = my_classifier(X[train], Y[train], X[test])
        results = classification_metrics(Y_pred, Y[test])
        accuracies.append(results[0])
        aucs.append(results[1])
    return mean(accuracies),mean(aucs)

# acc_k,auc_k = get_acc_auc_kfold(df_start, dataframe['gpa'])

X_train, X_t, y_train, y_t = train_test_split(dataframe['start'], dataframe['gpa'], test_size=0.33, random_state=42)
X_test, X_validation, y_test, y_validation = train_test_split(X_t, y_t, test_size=0.66, random_state=42)
clf = SGDClassifier(loss="hinge", penalty="l2", max_iter=5)
clf.fit(X_train, y_train)
pred = clf.predict(X_test)
print(pred)