import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import KFold

REGRESSION = 'REGRESSION'
BOOSTED_TREE = 'BOOSTED TREE'

sentiment_mapping = {
    0: "negative",
    1: "neutral",
    2: "positive"
}

def split(data, train, test):
    train = data.iloc[train]
    test = data.iloc[test]
    x_train = train[['tweet_count', 'likes', 'retweets', 'open', 'close', 'volume', 'sentiment']]
    x_test = test[['tweet_count', 'likes', 'retweets', 'open', 'close', 'volume', 'sentiment']]
    y_train = train['direction']
    y_test = test['direction']
    return x_train, x_test, y_train, y_test

def train(x_train, y_train, model_type):
    model = None
    if model_type == BOOSTED_TREE:
        model = GradientBoostingClassifier(
        )
    elif model_type == REGRESSION:
        model = LogisticRegression()
    else:
        raise ValueError
    model.fit(x_train, y_train)
    return model

def test(x_test, y_test, model):
    y_pred = model.predict(x_test)
    y_pred = pd.DataFrame(y_pred, columns=['Prediction'])
    scores = pd.DataFrame(y_test).reset_index().join(y_pred)
    scores = scores.rename(columns={'direction': 'Actual'})[['Actual', 'Prediction']]
    return scores

def build_scores(scores):
    tn, fp, fn, tp  = confusion_matrix(scores['Actual'], scores['Prediction']).ravel()
    print(f'True Negative:{tn}  False Positive:{fp}\n'
          f'False Negative:{fn}  True Positive:{tp}')
    accuracy = ((tn+tp) / (tn+fp+fn+tp))
    precision = 0 if tp == 0 and fp == 0 else (tp / (tp+fp))
    recall = 0 if tp == 0 and fn == 0 else (tp / (tp+fn))
    print(f"Accuracy: {accuracy*100:.2f} %")
    print(f"Precision: {precision*100:.2f} %")
    print(f"Recall: {recall*100:.2f} %")


if __name__ == '__main__':
    # TODO: data std for numerical
    df = pd.read_csv('final_dataset.csv')
    kfold = KFold(n_splits=5, shuffle=True, random_state=0)
    for model_type in [REGRESSION, BOOSTED_TREE]:
        for ticker, data in df.groupby('ticker'):
            data = data[~pd.isna(data.direction)].reset_index(drop=True)
            kfold_counter = 0
            for train_split, test_split in kfold.split(data):
                kfold_counter = kfold_counter + 1
                print(f"--------MODEL: {model_type} | KFOLD: {kfold_counter} | TICKER {ticker}--------")
                x_train, x_test, y_train, y_test = split(data, train_split, test_split)
                model = train(x_train, y_train, model_type)
                scores = test(x_test, y_test, model)
                build_scores(scores)
                print("\n")
