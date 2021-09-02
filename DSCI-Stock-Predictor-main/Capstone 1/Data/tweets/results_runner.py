import pandas as pd

df = pd.read_csv('results.csv', index_col=0)

groups = df.groupby(['dataset','model_type', 'direction_window'])
groups.mean().to_csv('avg_results.csv')
