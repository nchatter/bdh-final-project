import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import KFold, ShuffleSplit
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression, SGDClassifier, LinearRegression, PassiveAggressiveRegressor, TheilSenRegressor, SGDRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor
from sklearn.metrics import *
from sklearn.svm import SVR
import matplotlib.pyplot as plt



RANDOM_STATE = 545510477

'''
irp_data = pd.read_csv("combined_irp_data.csv", header=0, sep=',')
oscar_data = pd.read_csv("combined_oscar_data.csv", header=0, sep=',')

combined_data = pd.merge(oscar_data, irp_data, how='inner', on=['term', 'course_num', 'section'])
dataframe = pd.DataFrame(combined_data)

dataframe = dataframe[~dataframe.time.str.contains("ABBR")]

dataframe['start'] = dataframe.apply(lambda row: row.time.split('-')[0].strip().split(':')[0] + row.time.split('-')[0].strip().split(':')[1][0:2], axis=1)


dataframe.to_csv('merged_test.csv', sep=',')
'''
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



def f(x):
    try:
        if np.float(x) >= 0.05 and np.float(x) <= 4.00: return np.float(x)
        else: return np.nan
    except:
        return np.nan

def convert_military(x):
    if 'pm' in x.split('-')[0]:
        hour = x.split('-')[0].strip().split(':')[0].strip()
        minute = x.split('-')[0].strip().split(':')[1][0:2].strip()
        if hour == '12': return int(str(int(hour)) + minute)
        return int(str(int(hour) + 12) + minute)
    else:
        hour = x.split('-')[0].strip().split(':')[0].strip()
        minute = x.split('-')[0].strip().split(':')[1][0:2].strip()
        return int(str(int(hour)) + minute)

def round_gpa(x):
    return round(x, 1)

def compute_acc(y_true, y_pred):
    running_sum = 0
    for f,b in zip(y_true, y_pred):
        running_sum += (f - b) * (f - b)
    return running_sum / float(len(y_pred))

irp_data = pd.read_csv("combined_irp_data.csv", header=0, sep=',')
oscar_data = pd.read_csv("combined_oscar_data.csv", header=0, sep=',')

combined_data = pd.merge(oscar_data, irp_data, how='inner', on=['term', 'course_num', 'section'])
dataframe = pd.DataFrame(combined_data)

dataframe = dataframe[~dataframe.time.str.contains("ABBR")]


dataframe['gpa'] = dataframe['gpa'].apply(f)
dataframe = dataframe[pd.notnull(dataframe['gpa'])]
dataframe['gpa'] = dataframe['gpa'].astype('float')

dataframe['start'] = dataframe.apply(lambda row: row.time.split('-')[0].strip().split(':')[0] + row.time.split('-')[0].strip().split(':')[1][0:2], axis=1)
dataframe['start_military'] = dataframe['time'].apply(convert_military).astype('float')
dataframe['gpa_rounded'] = dataframe['gpa'].apply(round_gpa)

means = dataframe.groupby('start_military')['gpa'].mean()


#x_values = np.array(dataframe['start']).reshape((len(dataframe['start']), 1))
y_values = dataframe['gpa'].astype('float')
#x_values = pd.concat([dataframe['start_military'],dataframe['department']],axis=1)
x_values = np.array(dataframe['start_military']).reshape((len(dataframe['start']), 1))
y_values = dataframe['gpa'].astype('float')

'''
colors = (0,0,0)
area = np.pi*3
plt.scatter(np.array(dataframe['start_military']), dataframe['gpa'], s=area, c=colors, alpha=0.5)
plt.xlabel('Course Time')
plt.ylabel('GPA')
plt.show()
'''

x_train, x_test, y_train, y_test = train_test_split(x_values,y_values, test_size=0.30, random_state=RANDOM_STATE)
clf = RandomForestRegressor(n_estimators=1000) #SVR(gamma='scale', C=1.0, epsilon=0.2)
clf.fit(x_train,y_train)
predictions = clf.predict(x_test)


print(clf.score(x_test,y_test))
print(compute_acc(y_test, predictions))
