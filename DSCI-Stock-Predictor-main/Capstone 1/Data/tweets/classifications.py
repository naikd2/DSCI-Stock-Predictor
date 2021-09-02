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

def normalize(df):
    for feature_name in ['tweet_count', 'likes', 'retweets', 'open', 'close', 'volume']:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        df[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return df

def tfidf_features(df):
    others = {'ticker', 'date', 'tweet_count', 'likes', 'retweets', 'open', 'close', 'volume', 'direction'
              'direction_1',
              'direction_3',
              'direction_5',
              'direction_7',
              'direction_14',
              'direction_21',
              'direction_28',
              'index'}
    tfidf = set(df.columns)
    return list(tfidf - others)

def sentiment_features(df):
    return ['sentiment_negative', 'sentiment_neutral', 'sentiment_postive']

def split(data, train, test, type, direction):
    train = data.iloc[train]
    test = data.iloc[test]
    if type == 'tfidf':
        features = tfidf_features(train)
    else:
        features = sentiment_features(train)

    features = features + ['tweet_count', 'likes', 'retweets', 'open', 'close', 'volume']
    x_train = train[features]
    x_test = test[features]
    y_train = train[direction]
    y_test = test[direction]
    return x_train, x_test, y_train, y_test

def train(x_train, y_train, model_type):
    model = None
    if model_type == BOOSTED_TREE:
        model = GradientBoostingClassifier(
        )
    elif model_type == REGRESSION:
        model = LogisticRegression(max_iter=100000)
    else:
        raise ValueError
    model.fit(x_train, y_train)
    return model

def test(x_test, y_test, direction, model):
    y_pred = model.predict(x_test)
    y_pred = pd.DataFrame(y_pred, columns=['Prediction'])
    scores = pd.DataFrame(y_test).reset_index().join(y_pred)
    scores = scores.rename(columns={direction: 'Actual'})[['Actual', 'Prediction']]
    return scores

def build_scores(scores):
    tn, fp, fn, tp  = confusion_matrix(scores['Actual'], scores['Prediction']).ravel()
    print(f'True Negative:{tn}  False Positive:{fp}\n'
          f'False Negative:{fn}  True Positive:{tp}')
    accuracy = ((tn+tp) / (tn+fp+fn+tp))
    precision = 0 if tp == 0 and fp == 0 else (tp / (tp+fp))
    recall = 0 if tp == 0 and fn == 0 else (tp / (tp+fn))
    return accuracy*100, precision*100, recall*100

if __name__ == '__main__':
    datasets = {'final_dataset_sentiment.csv': 'sentiment'
                , 'final_dataset_tfidf.csv': 'tfidf'}
    records = []
    for d, type in datasets.items():
        df = pd.read_csv(d)
        df = normalize(df)
        data = df[~pd.isna(df.direction)].reset_index(drop=True)

        kfold = KFold(n_splits=5, shuffle=True, random_state=0)
        for direction in ['direction_1', 'direction_3', 'direction_5', 'direction_7',
                       'direction_14', 'direction_21', 'direction_28']:
            data = data[data[direction] != 0]
            for model_type in [REGRESSION, BOOSTED_TREE]:
                kfold_counter = 0
                for train_split, test_split in kfold.split(data):
                    kfold_counter = kfold_counter + 1
                    print(f"--------MODEL: {model_type} | KFOLD: {kfold_counter} | direction: {direction} --------")
                    x_train, x_test, y_train, y_test = split(data, train_split, test_split, type, direction)
                    model = train(x_train, y_train, model_type)
                    scores = test(x_test, y_test, direction, model)
                    accuracy, precision, recall = build_scores(scores)
                    r = {
                        'dataset': d,
                        'model_type': model_type,
                        'direction_window': direction,
                        'kfold': kfold_counter,
                        'accuracy': accuracy,
                        'precision': precision,
                        'recall': recall
                    }
                    records.append(r)
                    print("\n")

    pd.DataFrame.from_records(records).to_csv("results.csv")
