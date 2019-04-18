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

def getFName(x):
    x = ' '.join(x.split())
    return x.split(' ')[0]

def getLName(x):
    x = ' '.join(x.split())
    return x.split(' ')[-1]

def getDiff(x):
    return x.split(' ')[1][0]

def getDept(x):
    return x.split(' ')[0]


def compute_acc(y_true, y_pred):
    running_sum = 0
    for f,b in zip(y_true, y_pred):
        running_sum += (f - b) * (f - b)
    return running_sum / float(len(y_pred))

irp_data = pd.read_csv("../data/combined_irp_data.csv", header=0, sep=',')
oscar_data = pd.read_csv("../data/combined_oscar_data.csv", header=0, sep=',')
prof_data = pd.read_csv("../data/prof_data/prof_comments_score.csv",header=None,sep=',',usecols=[0,1,2,3,4,5],names=['tid','overall_rating','fName','lName','num_ratings','pos_score'])

dataframe = pd.merge(oscar_data, irp_data, how='inner', on=['term', 'course_num', 'section'])

dataframe = dataframe[~dataframe.time.str.contains("ABBR")]

dataframe['gpa'] = dataframe['gpa'].apply(f)
dataframe = dataframe[pd.notnull(dataframe['gpa'])]
dataframe['gpa'] = dataframe['gpa'].astype('float')

dataframe['start'] = dataframe.apply(lambda row: row.time.split('-')[0].strip().split(':')[0] + row.time.split('-')[0].strip().split(':')[1][0:2], axis=1)
dataframe['start_military'] = dataframe['time'].apply(convert_military).astype('float')
dataframe['gpa_rounded'] = dataframe['gpa'].apply(round_gpa)
dataframe['difficulty'] = dataframe['course_num'].apply(getDiff)
dataframe['department'] = dataframe['course_num'].apply(getDept)
unique_departments = dataframe.department.unique()
department_mapping = {k: v for v, k in enumerate(unique_departments)}
dataframe['department'] = dataframe['department'].apply(lambda x: department_mapping[x])
dataframe['fName'] = dataframe['prof'].apply(getFName)
dataframe['lName'] = dataframe['prof'].apply(getLName)

dataframe = pd.merge(dataframe,prof_data,how='inner',on=['fName','lName'])

#x_values = np.array(dataframe['start']).reshape((len(dataframe['start']), 1))

x_values = np.array(dataframe['start_military']).reshape(-1,1)
x_values = pd.concat([dataframe['start_military'],dataframe['difficulty'],dataframe['pos_score'],dataframe['enrollment'],dataframe['department'],dataframe['credits']],axis=1)
y_values = dataframe['gpa'].astype('float')

'''
colors = (0,0,0)
area = np.pi*3
plt.scatter(np.array(dataframe['credits']), dataframe['enrollment'], s=area, c=colors, alpha=0.5)
plt.xlabel('Credits')
plt.ylabel('Enrollment')
plt.savefig('foo.png')
'''

x_train, x_test, y_train, y_test = train_test_split(x_values,y_values, test_size=0.20, random_state=RANDOM_STATE)
clf = RandomForestRegressor(n_estimators=1000)
clf.fit(x_train,y_train)
predictions = clf.predict(x_test)


print(clf.score(x_test,y_test))
print(compute_acc(y_test, predictions))


importances = clf.feature_importances_
std = np.std([tree.feature_importances_ for tree in clf.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")

for f in range(x_values.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

# Plot the feature importances of the forest
plt.figure()
plt.bar(range(x_values.shape[1]), importances[indices],
       color="b", yerr=std[indices], align="center")
plt.xticks(range(x_values.shape[1]), indices)
plt.xlim([-1, x_values.shape[1]])
plt.show()
