import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


from model import clf

import time
timestr= time.strftime("%Y%m%d-%H%M%S")

# prep
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.datasets import make_classification
from sklearn.preprocessing import binarize, LabelEncoder, MinMaxScaler


# Validation libraries
from sklearn import metrics
from sklearn.metrics import accuracy_score, mean_squared_error, precision_recall_curve
from sklearn.model_selection import cross_val_score

#Bagging
from sklearn.ensemble import AdaBoostClassifier


def input_test(path):

    train_df = pd.read_csv(path)
    print(train_df)
    
    #missing data
    total = train_df.isnull().sum().sort_values(ascending=False)
    percent = (train_df.isnull().sum()/train_df.isnull().count()).sort_values(ascending=False)
    missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])

    #dealing with missing data
    train_df.drop(['comments'], axis= 1, inplace=True)
    train_df.drop(['state'], axis= 1, inplace=True)
    train_df.drop(['Timestamp'], axis= 1, inplace=True)

    train_df.isnull().sum().max() #just checking that there's no missing data missing...

    # Assign default values for each data type
    defaultInt = 0
    defaultString = 'NaN'
    defaultFloat = 0.0

    # Create lists by data tpe
    intFeatures = ['Age']
    stringFeatures = ['Gender', 'Country', 'self_employed', 'family_history', 'treatment', 'work_interfere',
                'no_employees', 'remote_work', 'tech_company', 'anonymity', 'leave', 'mental_health_consequence',
                'phys_health_consequence', 'coworkers', 'supervisor', 'mental_health_interview', 'phys_health_interview',
                'mental_vs_physical', 'obs_consequence', 'benefits', 'care_options', 'wellness_program',
                'seek_help']
    floatFeatures = []

    # Clean the NaN's
    for feature in train_df:
        if feature in intFeatures:
            train_df[feature] = train_df[feature].fillna(defaultInt)
        elif feature in stringFeatures:
            train_df[feature] = train_df[feature].fillna(defaultString)
        elif feature in floatFeatures:
            train_df[feature] = train_df[feature].fillna(defaultFloat)
        else:
            print('Error: Feature %s not recognized.' % feature)

    #Clean 'Gender'
    gender = train_df['Gender'].unique()

    #Made gender groups
    male_str = ["male", "m", "male-ish", "maile", "mal", "male (cis)", "make", "male ", "man","msle", "mail", "malr","cis man", "Cis Male", "cis male"]
    trans_str = ["trans-female", "something kinda male?", "queer/she/they", "non-binary","nah", "all", "enby", "fluid", "genderqueer", "androgyne", "agender", "male leaning androgynous", "guy (-ish) ^_^", "trans woman", "neuter", "female (trans)", "queer", "ostensibly male, unsure what that really means"]           
    female_str = ["cis female", "f", "female", "woman",  "femake", "female ","cis-female/femme", "female (cis)", "femail"]

    for (row, col) in train_df.iterrows():

        if str.lower(col.Gender) in male_str:
            train_df['Gender'].replace(to_replace=col.Gender, value='male', inplace=True)

        if str.lower(col.Gender) in female_str:
            train_df['Gender'].replace(to_replace=col.Gender, value='female', inplace=True)

        if str.lower(col.Gender) in trans_str:
            train_df['Gender'].replace(to_replace=col.Gender, value='trans', inplace=True)

    #Get rid of bullshit
    stk_list = ['A little about you', 'p']
    train_df = train_df[~train_df['Gender'].isin(stk_list)]

    #complete missing age with mean
    train_df['Age'].fillna(train_df['Age'].median(), inplace = True)

    # Fill with media() values < 18 and > 120
    s = pd.Series(train_df['Age'])
    s[s<18] = train_df['Age'].median()
    train_df['Age'] = s
    s = pd.Series(train_df['Age'])
    s[s>120] = train_df['Age'].median()
    train_df['Age'] = s

    #Ranges of Age
    train_df['age_range'] = pd.cut(train_df['Age'], [0,20,30,65,100], labels=["0-20", "21-30", "31-65", "66-100"], include_lowest=True)

    #There are only 0.014% of self employed so let's change NaN to NOT self_employed
    #Replace "NaN" string from defaultString
    train_df['self_employed'] = train_df['self_employed'].replace([defaultString], 'No')

    #There are only 0.20% of self work_interfere so let's change NaN to "Don't know
    #Replace "NaN" string from defaultString

    train_df['work_interfere'] = train_df['work_interfere'].replace([defaultString], 'Don\'t know' )

    #Encoding data
    labelDict = {}
    for feature in train_df:
        le = preprocessing.LabelEncoder()
        le.fit(train_df[feature])
        le_name_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
        train_df[feature] = le.transform(train_df[feature])
        # Get labels
        labelKey = 'label_' + feature
        labelValue = [*le_name_mapping]
        labelDict[labelKey] =labelValue

    #Get rid of 'Country'
    train_df = train_df.drop(['Country'], axis= 1)

    #Features Scaling: We're going to scale age, because it is extremely different from the other ones.
    #Scaling and Fitting
    # Scaling Age
    scaler = MinMaxScaler()
    train_df['Age'] = scaler.fit_transform(train_df[['Age']])

    #Spilitting Dataset
    # define X and y
    feature_cols = ['Age', 'Gender', 'family_history', 'benefits', 'care_options', 'anonymity', 'leave', 'work_interfere']
    X = train_df[feature_cols]
    y = train_df.treatment


    dfTestPredictions = clf.predict(X)

    # Write predictions to csv file
    # We don't have any significative field so we save the index
    results = pd.DataFrame({'Index': X.index, 'Treatment': dfTestPredictions})

    f = results[results['Treatment'] == 1]

    # Save to file
    # This file will be visible after publishing in the output section
    f.to_csv('results'+timestr+'.csv')
    
    return f

