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

def compute_acc(y_true, y_pred):
    running_sum = 0
    for f,b in zip(y_true, y_pred):
        running_sum += (f - b) * (f - b)
    return running_sum / float(len(y_pred))

def convert_military(x):
    #test = 01:30 PM - 02:50 PM
    #print(x)
    if 'PM' in x.split('-')[0]:
        hour = x.split('-')[0].strip().split(':')[0].strip()
        minute = x.split('-')[0].strip().split(':')[1][0:2].strip()
        if hour == '12': return int(str(int(hour)) + minute)
        return int(str(int(hour) + 12) + minute)
    else:
        hour = x.split('-')[0].strip().split(':')[0].strip()
        minute = x.split('-')[0].strip().split(':')[1][0:2].strip()
        return int(str(int(hour)) + minute)

def getFName(x):
    fName_MI = x.split(',')[1].strip()
    items = fName_MI.split(' ')
    return items[0]

def getLName(x):
    return x.split(',')[0]

course_data = pd.read_csv("../data/course_data/uiuc_combined_data.csv", header=0, sep=',')
course_data = course_data.sort_values(['year','term','subject','number','section'],ascending=[False,True,True,True,True])
prof_data = pd.read_csv("../data/prof_data/prof_comments_score.csv",header=None,sep=',',usecols=[0,1,2,3,4,5],names=['tid','overall_rating','fName','lName','num_ratings','pos_score'])


course_data = course_data[~course_data.time.str.contains("ARRANGED")]
course_data['start_military'] = course_data['time'].apply(convert_military).astype('float')
unique_departments = course_data.subject.unique()
department_mapping = {k: v for v, k in enumerate(unique_departments)}
course_data['department'] = course_data['subject'].apply(lambda x: department_mapping[x])
course_data['level'] = course_data['number'].apply(lambda x: str(x)[0])
course_data['key'] = course_data.apply(lambda x: str(x.year)+str(x.term)+str(x.subject)+str(x.number), axis=1)
course_counts = course_data.groupby('key').count().to_dict()


gpa_data = pd.read_csv("../data/gpa/uiuc-gpa-dataset.csv",header=0,sep=',')
gpa_data['enrollment'] = gpa_data.apply(lambda row: row.A_plus + row.A + row.A_minus + row.B_plus + row.B + row.B_minus + row.C_plus + row.C + row.C_minus + row.D_plus + row.D + row.D_minus + row.F ,axis=1)
gpa_data['gpa'] = gpa_data.apply(lambda row: (row.A_plus*4 + row.A*4 + row.A_minus*3.67 + row.B_plus*3.33 + row.B*3 + row.B_minus*2.67 + row.C_plus*2.33 + row.C*2 + row.C_minus*1.67 + row.D_plus*1.33 + row.D + row.D_minus*0.67 + row.F*0)/float(row.enrollment),axis =1 )
gpa_data['term'] = gpa_data['term'].str.lower()
gpa_data = gpa_data[pd.notnull(gpa_data['prof'])]
gpa_data['fName'] = gpa_data['prof'].apply(getFName)
gpa_data['lName'] = gpa_data['prof'].apply(getLName)
gpa_data['key'] = gpa_data.apply(lambda x: str(x.year)+str(x.term)+str(x.subject)+str(x.number), axis=1)
gpa_counts = gpa_data.groupby('key').count().to_dict()

delete_keys = set()
for key in course_counts:
    if key in gpa_counts:
        if course_counts[key] != gpa_counts[key]: delete_keys.add(key)
    else: delete_keys.add(key)

course_data = course_data[~course_data['key'].isin(delete_keys)]
gpa_data = gpa_data[~gpa_data['key'].isin(delete_keys)]

course_data['rank'] = course_data.groupby(['key']).cumcount()+1
gpa_data['rank'] = gpa_data.groupby(['key']).cumcount()+1

course_gpa_data = pd.merge(course_data, gpa_data, how='inner', on=['key', 'rank'])
course_gpa_data = pd.merge(course_gpa_data, prof_data, how='inner', on=['fName', 'lName'])
course_gpa_data.to_csv('course_gpa_data_test.csv',sep=',')

x_values = pd.concat([course_gpa_data['start_military'],course_gpa_data['level'],course_gpa_data['enrollment'],course_gpa_data['department'],course_gpa_data['credits'], course_gpa_data['pos_score']],axis=1)
y_values = course_gpa_data['gpa'].astype('float')

'''
colors = (0,0,0)
area = np.pi*3
plt.scatter(np.array(course_gpa_data['level']), course_gpa_data['gpa'], s=area, c=colors, alpha=0.5)
plt.xlabel('Level')
plt.ylabel('GPA')
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

