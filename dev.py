"""
The main idea of this Repo is to generate some fake data and perform predictive analysis using some basic models
#REFERENCE MODEL: "https://365datascience.com/tutorials/python-tutorials/predictive-model-python/"
"""
from os import X_OK
import pandas as pd
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import classification_report

df = pd.read_csv("kerala.csv")
df.describe()
# splitting the dataset to select the features
X= df.iloc[:,1:14]
Y= df.iloc[:,-1]
# selecting the top 3 features
best_features= SelectKBest(score_func=chi2, k=3)
fit= best_features.fit(X,Y)
# Creating dataframes
df_scores = pd.DataFrame(fit.scores_)
df_columns = pd.DataFrame(X.columns)
# replacing a column in the dataframe
df['FLOODS'].replace(['YES', 'NO'], [1,0], inplace=True)
print(df.head())
# Combining the features
features_scores = pd.concat([df_columns,df_scores],axis=1)
features_scores.columns = ['Features','Score']
features_scores = features_scores.sort_values(by='Score',ascending=False)
print(features_scores.head())
# Next Building the model 
X= df[['SEP','JUN', 'JUL']]
Y=df[['FLOODS']]
# Split the dataset into train and test dataset
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 100)
# Building the model
logreg= LogisticRegression()
logreg.fit(X_train, Y_train)
# Predicting the test set results
y_pred = logreg.predict(X_test)
print(y_pred)
print (X_test)
# Model evaluation
print("Accuracy:",metrics.accuracy_score(Y_test, y_pred))
print("Recall: ",metrics.recall_score(Y_test, y_pred, zero_division=1))
print("Precision:",metrics.precision_score(Y_test, y_pred, zero_division=1))
print("CL Report:",metrics.classification_report(Y_test, y_pred, zero_division=1))