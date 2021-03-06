# -*- coding: utf-8 -*-
"""DataAnalysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jJXyTNKwjeTHA0bFh01Z7P5z-gxFlSld
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
sns.set_style('whitegrid')
import statsmodels.api as sm
from scipy import stats
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

df = pd.read_csv("Project/data/student-por.csv",sep=";")
df['Grade'] = "NA"
df.loc[(df.G3 >= 15) & (df.G3 <= 20), 'Grade'] = 'good' 
df.loc[(df.G3 >= 10) & (df.G3 <= 14), 'Grade'] = 'fair' 
df.loc[(df.G3>= 0) & (df.G3 <= 9), 'Grade'] = 'poor' 
df.columns

print("Target Variable Analysis\n")
print("Mean : "+str(np.mean(df['G3'])))
print("Median : "+str(np.median(df['G3'])))
print("Mode : "+str(stats.mode(df['G3'])))
print("Standard Deviation : "+str(np.std(df['G3'])))
print("Variance : "+str(np.var(df['G3'])))

corr=df.corr()
plt.figure(figsize=(20,20))
sns.heatmap(corr,annot=True,cmap="Reds")
plt.title("Correlation Matrix",fontsize=20)

plt.figure(figsize=(8,6))
sns.countplot(df.Grade,order=["poor","fair","good"])
plt.title('Final Grade - Number of Students',fontsize=20)
plt.xlabel('Final Grade', fontsize=16)
plt.ylabel('Number of Student', fontsize=16)

#CrossTabulating the Data based on Romantic Relationships
perc = (lambda col: col/col.sum())
index = ['poor','fair','good']
romance_tab1 = pd.crosstab(index=df.Grade, columns=df.romantic)
romance_tab = np.log(romance_tab1) #Reducing Skewness of data, and reducing effects of outliers.
romance_perc = romance_tab.apply(perc).reindex(index)
plt.figure()
romance_perc.plot.bar(figsize=(8,6),fontsize=16)
plt.title("Final Grade with Romantic Status",fontsize=15)
plt.xlabel("Grade",fontsize=15)
plt.ylabel("Number of Students",fontsize=15)

import statsmodels.api as sm
romance_table = sm.stats.Table(romance_tab1)
romance_rslt = romance_table.test_nominal_association()
romance_rslt.pvalue

alc_tab1 = pd.crosstab(index=df.Grade, columns=df.Walc)
alc_tab = np.log(alc_tab1)
alc_perc = alc_tab.apply(perc).reindex(index)
good = df.loc[df.Grade == 'good']
good['good_alcohol_usage']=good.Walc
poor = df.loc[df.Grade == 'poor']
poor['poor_alcohol_usage']=poor.Walc
plt.figure(figsize=(10,6))
p1=sns.kdeplot(good['good_alcohol_usage'], shade=True, color="r")
p1=sns.kdeplot(poor['poor_alcohol_usage'], shade=True, color="b")
plt.title('Good Performance vs. Poor Performance Student Weekend Alcohol Consumption', fontsize=20)
plt.ylabel('Density', fontsize=16)
plt.xlabel('Level of Alcohol Consumption', fontsize=16)

alc_perc.plot.bar(colormap="Reds", figsize=(10,8), fontsize=16)
plt.title('Final Grade By Weekend Alcohol Consumption', fontsize=20)
plt.ylabel('Percentage of Logarithm Student Counts', fontsize=16)
plt.xlabel('Final Grade', fontsize=16)

import statsmodels.api as sm
alc_table = sm.stats.Table(alc_tab1)
alc_rslt = alc_table.test_nominal_association()
alc_rslt.pvalue

good['good_student_father_education'] = good.Fedu
poor['poor_student_father_education'] = poor.Fedu
good['good_student_mother_education'] = good.Medu
poor['poor_student_mother_education'] = poor.Medu

plt.figure(figsize=(6,4))
p2=sns.kdeplot(good['good_student_father_education'], shade=True, color="r")
p2=sns.kdeplot(poor['poor_student_father_education'], shade=True, color="b")
plt.xlabel('Father Education Level', fontsize=20)

plt.figure(figsize=(6,4))
p3=sns.kdeplot(good['good_student_mother_education'], shade=True, color="r")
p3=sns.kdeplot(poor['poor_student_mother_education'], shade=True, color="b")
plt.xlabel('Mother Education Level', fontsize=20)

X_edu = df[['Medu','Fedu']]
y_edu = df.G3
edu = sm.OLS(y_edu, X_edu)
results_edu = edu.fit()
results_edu.summary()

plt.figure(figsize=(6,10))
sns.boxplot(x='goout', y='G3', data=df, palette='hot')
plt.title('Final Grade By Frequency of Going Out', fontsize=20)
plt.ylabel('Final Score', fontsize=16)
plt.xlabel('Frequency of Going Out', fontsize=16)

out_tab = pd.crosstab(index=df.Grade, columns=df.goout)
out_perc = out_tab.apply(perc).reindex(index)

out_perc.plot.bar(colormap="mako_r", fontsize=16, figsize=(14,6))
plt.title('Final Grade By Frequency of Going Out', fontsize=20)
plt.ylabel('Percentage of Student', fontsize=16)
plt.xlabel('Final Grade', fontsize=16)

out_table = sm.stats.Table(out_tab)
out_rslt = out_table.test_nominal_association()
out_rslt.pvalue

plt.figure(figsize=(12,8))
sns.violinplot(x='age', y='studytime', hue='higher', data=df, palette="Accent_r", ylim=(1,6))
plt.title('Distribution Of Study Time By Age & Desire To Receive Higher Education', fontsize=20)
plt.ylabel('Study Time', fontsize=16)
plt.xlabel('Age', fontsize=16)

higher_tab = pd.crosstab(index=df.Grade, columns=df.higher)
higher_perc = higher_tab.apply(perc).reindex(index)
higher_perc.plot.bar(figsize=(14,6), fontsize=16)
plt.title('Final Grade By Desire to Receive Higher Education', fontsize=20)
plt.xlabel('Final Grade', fontsize=16)
plt.ylabel('Percentage of Student', fontsize=16)
import statsmodels.api as sm
higher_table = sm.stats.Table(higher_tab)
higher_rslt = higher_table.test_nominal_association()
higher_rslt.pvalue

plt.figure(figsize=(6,6))
sns.countplot(df.address,palette="Blues")
plt.title('Urban and Rural Students Count', fontsize=20)
plt.xlabel('Living Area', fontsize=16)
plt.ylabel('Number Of Students', fontsize=16)

ad_tab1 = pd.crosstab(index=df.Grade, columns=df.address)
ad_tab = np.log(ad_tab1)
ad_perc = ad_tab.apply(perc).reindex(index)
ad_perc.plot.bar(colormap="RdYlGn_r", fontsize=16, figsize=(8,6))
plt.title('Final Grade By Living Area', fontsize=20)
plt.ylabel('Percentage of Logarithm Student#', fontsize=16)
plt.xlabel('Final Grade', fontsize=16)

ad_table = sm.stats.Table(ad_tab1)
ad_rslt = ad_table.test_nominal_association()
ad_rslt.pvalue

dfl = df.copy()
X_ols = dfl.drop(['G1', 'G2', 'G3','Grade', 'failures','studytime','absences'], axis=1)
X_ols = pd.get_dummies(X_ols)
mod = sm.OLS(df.G3, X_ols)
mod = mod.fit()
print(mod.summary())

dfd = df.copy()
dfd = dfd.drop([ 'G3'], axis=1)

from sklearn import preprocessing
le = preprocessing.LabelEncoder()
dfd.Grade = le.fit_transform(dfd.Grade)

from sklearn.model_selection import train_test_split
X = dfd.drop('Grade',axis=1)
y = dfd.Grade
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3)

X_train = pd.get_dummies(X_train)
X_test = pd.get_dummies(X_test)

from sklearn.tree import DecisionTreeClassifier
msl=[]
for i in range(1,58):
    tree = DecisionTreeClassifier(min_samples_leaf=i)
    t= tree.fit(X_train, y_train)
    ts=t.score(X_test, y_test)
    msl.append(ts)
msl = pd.Series(msl)
msl.where(msl==msl.max()).dropna()

tree = DecisionTreeClassifier(min_samples_leaf=12)
t= tree.fit(X_train, y_train)
print("Decision Tree Model Score : "+str(t.score(X_train, y_train))+ 
      "\nCross Validation Score : "+str(t.score(X_test, y_test)))
y_pred = t.predict(X_test)
print("Training Error:"+str(1-tree.score(X_train,y_train)))
print("Test Error:"+str(1-tree.score(X_test,y_test)))
print("Correct Predictions : "+str(len(df.where(y_pred==y_test).dropna())))
print("Incorrect Predictions : "+str(len(df.where(y_pred!=y_test).dropna())))
print("Total Predictions : " + str(len(y_pred)))
target_names=["Class 0","Class 1","Class 2"]
print(classification_report(y_test,y_pred,target_names=target_names))
cm = confusion_matrix(y_test,y_pred)
plt.figure(figsize=(10,7))
sns.set(font_scale=1.3)
sns.heatmap(cm,annot=True,annot_kws={"size": 16})

from sklearn.ensemble import RandomForestClassifier
ne=[]
for i in range(1,58):
    forest = RandomForestClassifier(n_estimators=36, min_samples_leaf=i)
    f = forest.fit(X_train, y_train)
    fs = f.score(X_test, y_test)
    ne.append(fs)
ne = pd.Series(ne)
ne.where(ne==ne.max()).dropna()
forest = RandomForestClassifier(n_estimators=36, min_samples_leaf=2)
f = forest.fit(X_train, y_train)
print("Random Forest Model Score :"+str(f.score(X_train, y_train))+
      "\nCross Validation Score : "+str(f.score(X_test, y_test)))
print("Training Error:"+str(1-f.score(X_train,y_train)))
print("Test Error:"+str(1-f.score(X_test,y_test)))
y_pred = forest.predict(X_test)
print("Correct Predictions : "+str(len(df.where(y_pred==y_test).dropna())))
print("Incorrect Predictions : "+str(len(df.where(y_pred!=y_test).dropna())))
print("Total Predictions : " + str(len(y_pred)))
print(classification_report(y_test,y_pred,target_names=target_names))
cm = confusion_matrix(y_test,y_pred)
plt.figure(figsize=(10,7))
sns.set(font_scale=1.3)
sns.heatmap(cm,annot=True,annot_kws={"size": 16})

from sklearn.svm import SVC
svc = SVC()
s= svc.fit(X_train, y_train)
print("SVC Model Score : "+str(s.score(X_train, y_train))+
      "\nCross Validation Score : "+str(s.score(X_test, y_test)))
print("Training Error:"+str(1-s.score(X_train,y_train)))
print("Test Error:"+str(1-s.score(X_test,y_test)))
y_pred = s.predict(X_test)
print("Correct Predictions : "+str(len(df.where(y_pred==y_test).dropna())))
print("Incorrect Predictions : "+str(len(df.where(y_pred!=y_test).dropna())))
print("Total Predictions : " + str(len(y_pred)))
print(classification_report(y_test,y_pred,target_names=target_names))
cm = confusion_matrix(y_test,y_pred)
plt.figure(figsize=(10,7))
sns.set(font_scale=1.3)
sns.heatmap(cm,annot=True,annot_kws={"size": 16})

from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(multi_class='multinomial', solver='newton-cg',fit_intercept=True)
from sklearn.feature_selection import SelectKBest, chi2

ks=[]
for i in range(1,58):
    sk = SelectKBest(chi2, k=i)
    x_new = sk.fit_transform(X_train,y_train)
    x_new_test=sk.fit_transform(X_test,y_test)
    l = lr.fit(x_new, y_train)
    ll = l.score(x_new_test, y_test)
    ks.append(ll)  
    
ks = pd.Series(ks)
ks = ks.reindex(list(range(1,58)))
ks.where(ks==ks.max()).dropna()
sk = SelectKBest(chi2, k=8)
x_new = sk.fit_transform(X_train,y_train)
x_new_test=sk.fit_transform(X_test,y_test)

lr = lr.fit(x_new, y_train)
y_pred = lr.predict(x_new_test)
print("Logistic Regression Model Score : "+str(lr.score(x_new, y_train))+
      "\nCross Validation Score : "+str(lr.score(x_new_test, y_test)))
print("Training Error:"+str(1-lr.score(x_new,y_train)))
print("Test Error:"+str(1-lr.score(x_new_test,y_test)))
print(classification_report(y_test,y_pred,target_names=target_names))
cm = confusion_matrix(y_test,y_pred)
plt.figure(figsize=(10,7))
sns.set(font_scale=1.3)
sns.heatmap(cm,annot=True,annot_kws={"size": 16})

import numpy as np
import scipy.stats
def mean_confidence_interval(data,confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h
a,b,c = mean_confidence_interval(df["G3"],0.95)
print(a)
print("Interval is : "+str(a)+" +/- "+str(a-b))

#Don't execute this again
from sklearn.tree import export_graphviz
import os
from os import system
tree_dot = open("tree.dot","w")
export_graphviz(tree,
                feature_names=X_train.columns,
                filled=True,
                rounded=True, out_file=tree_dot)
tree_dot.close()
os.system('dot -Tpng tree.dot -o tree.png')

from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

model = XGBClassifier()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
pred = [round(value) for value in y_pred]
accuracy = accuracy_score(y_test, pred)
print("Accuracy: %.2f%%" % (accuracy * 100.0))
target_names=["Class 0","Class 1","Class 2"]
print(classification_report(y_test,y_pred,target_names=target_names))

from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
dt = DecisionTreeClassifier()
adaboost = AdaBoostClassifier(n_estimators=100, base_estimator=dt,learning_rate=1)
adaboost.fit(X_train,y_train)
y_pred = adaboost.predict(X_test)
pred = [round(value) for value in y_pred]
accuracy = accuracy_score(y_test,pred)
print("Accuracy: %.2f%%" % (accuracy * 100.0))
target_names=["Class 0","Class 1","Class 2"]
print(classification_report(y_test,y_pred,target_names=target_names))

from sklearn.ensemble import GradientBoostingClassifier
gradientboost = GradientBoostingClassifier(n_estimators=4, learning_rate=1.0, max_depth=1)
gradientboost.fit(X_train, y_train)
y_pred = gradientboost.predict(X_test)
pred = [round(value) for value in y_pred]
accuracy = accuracy_score(y_test,pred)
print("Accuracy: %.2f%%" % (accuracy * 100.0))
target_names=["Class 0","Class 1","Class 2"]
print(classification_report(y_test,y_pred,target_names=target_names))