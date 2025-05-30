# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 11:00:27 2025

@author: Sri Lakshmi Prasanna
"""
import os
import pandas as pd
os.chdir(r'C:\Users\Sri Lakshmi Prasanna\OneDrive\ai\SPAM classifier')

print("Current Directory:", os.getcwd())
messages = pd.read_csv('smsspamcollection/SMSSpamCollection.csv', sep='\t',
                       names=["label", "message"],)

import re
import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
corpus = []

for i in range(0, len(messages)):
    msg = messages['message'][i]
    # Ensure msg is string type
    if isinstance(msg, bytes):
        msg = msg.decode('utf-8')
    elif not isinstance(msg, str):
        msg = str(msg)
    
    review = re.sub('[^a-zA-Z]', ' ', msg)
    review = review.lower()
    review = review.split()
    
    review = [ps.stem(word) for word in review if not word in stopwords.words('english')]
    review = ' '.join(review)
    corpus.append(review)

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=2500)
X = cv.fit_transform(corpus).toarray()
y = pd.get_dummies(messages['label'])
y = y.iloc[:,1].values

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)

from sklearn.naive_bayes import MultinomialNB
spam_detect_model = MultinomialNB().fit(X_train, y_train)
y_pred = spam_detect_model.predict(X_test)


from sklearn.metrics import confusion_matrix
confusion_m=confusion_matrix(y_test,y_pred)

from sklearn.metrics import accuracy_score
accuracy=accuracy_score(y_test,y_pred)