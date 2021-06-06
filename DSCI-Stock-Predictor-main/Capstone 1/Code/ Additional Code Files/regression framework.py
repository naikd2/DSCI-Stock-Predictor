import json
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

df = pd.read_csv('final_nvda.csv')


model = LogisticRegression()

# Map string to float
mapper = {
    'neu': 0.0,
    'pos': 1.0,
    'neg': -1.0
}
df['comments'] = df['comments'].map(mapper).fillna(0)
df['posts'] = df['posts'].map(mapper).fillna(0)

X = df[['comments', 'posts']]
y = df['direction']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
logreg = LogisticRegression()
logreg.fit(X_train, y_train)
y_pred = logreg.predict(X_test)
print('% Accuracy of Regression Classifier: {:.2f}%'.format(logreg.score(X_test, y_test) * 100))

