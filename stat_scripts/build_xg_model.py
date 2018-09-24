import pickle
import time
import pandas as pd
import numpy as np
import xg_prepare as xg
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split, RandomizedSearchCV
from sklearn.metrics import roc_auc_score, log_loss
from sklearn.linear_model import LogisticRegression

SEED = 5
folder = '../scraped_files/'
file_names = ['nhl_pbp20102011.csv', 'nhl_pbp20112012.csv',
              'nhl_pbp20122013.csv', 'nhl_pbp20132014.csv',
              'nhl_pbp20142015.csv', 'nhl_pbp20152016.csv',
              'nhl_pbp20162017.csv', 'nhl_pbp20172018.csv']

train_file_names = file_names[:-1]
test_file_names = file_names[-1]

feature_columns = ['seconds_elapsed', 'xc', 'yc', 'time_diff', 'score_diff',
                   'prior_x_coords', 'prior_y_coords', 'dist_to_prior',
                   'distance', 'angle', 'is_rebound', 'rebound_angle', 'is_rush',
                   'shooter_strength', 'type_BACKHAND', 'type_DEFLECTED',
                   'type_SLAP SHOT', 'type_SNAP SHOT', 'type_TIP-IN',
                   'type_WRIST SHOT']

test_df = pd.read_csv(f'{folder}{test_file_names}')
test_df.columns = list(map(str.lower, test_df.columns))
test_df = xg.fixed_seconds_elapsed(test_df)
test_df = xg.create_stat_features(test_df)
test_df = pd.get_dummies(test_df[test_df.event.isin(['SHOT', 'GOAL', 'MISS'])],
                         columns=['type'])
test_df = test_df[~test_df[feature_columns].isnull().any(axis=1)]

print(test_df.head())

train_dfs = []


target = ['is_goal']

for name in train_file_names:
    pbp_df = pd.read_csv(f'{folder}{name}')
    pbp_df.columns = list(map(str.lower, pbp_df.columns))
    pbp_df = xg.fixed_seconds_elapsed(pbp_df)
    pbp_df = xg.create_stat_features(pbp_df)
    pbp_df = pd.get_dummies(pbp_df[pbp_df.event.isin(['SHOT', 'GOAL', 'MISS'])],
                            columns=['type'])
    pbp_df = pbp_df[~pbp_df[feature_columns].isnull().any(axis=1)]
    train_dfs.append(pbp_df)

train_dfs = pd.concat(train_dfs)

random_forest = RandomForestClassifier(random_state=SEED, bootstrap=True, class_weight='balanced',
                              n_jobs=-1)
gbm = GradientBoostingClassifier(random_state=SEED, learning_rate=.01)

log = LogisticRegression(max_iter=100000, random_state=SEED)

log_params = {'C':[.001, .01, .1, 1, 10, 100, 1000, 10000],
              'solver':['sag']}

forest_params = {'n_estimators': [200], 'min_samples_leaf': [50, 100, 250, 500]}

gbm_params = {'min_samples_split': [100, 250, 500],
              'max_depth': [3, 4, 5]}

gradient_boost = GridSearchCV(gbm, gbm_params, scoring='neg_log_loss', cv=5)
random_forest = GridSearchCV(random_forest, forest_params, scoring='neg_log_loss', cv=5)
logreg = GridSearchCV(log, log_params, scoring='neg_log_loss', cv=5)

print('Training GBM model')
start_time = time.time()
gradient_boost.fit(train_dfs[feature_columns], train_dfs.loc[:, target[0]])
end_time = time.time()
print('It took this model {} minutes to train.'.format((end_time-start_time)/60))

print('Training Random Forestmodel')
start_time = time.time()
random_forest.fit(train_dfs[feature_columns], train_dfs.loc[:, target[0]])
end_time = time.time()
print('It took this model {} minutes to train.'.format((end_time-start_time)/60))

print('Training Logistic Regression')
start_time = time.time()
log.fit(train_dfs[feature_columns], train_dfs.loc[:, target[0]])
end_time = time.time()
print('It took this model {} minutes to train.'.format((end_time-start_time)/60))
with open('gbm_model', 'wb') as f:
    pickle.dump(gradient_boost, f)
with open('random_forest_model', 'wb') as f:
    pickle.dump(random_forest, f)

test_df['xg_gbm'] = gradient_boost.predict_proba(test_df[feature_columns])[:, 1]

auc_gbm=roc_auc_score(test_df[target], test_df['xg_gbm'])
ll_gbm = log_loss(test_df[target], test_df['xg_gbm'])

print(f'gbm AUC score: {auc_gbm}')
print(f'gbm log loss score: {ll_gbm}')
test_df['xg_rf'] = random_forest.predict_proba(test_df[feature_columns])[:, 1]

auc_rf=roc_auc_score(test_df[target], test_df['xg_rf'])
ll_rf = log_loss(test_df[target], test_df['xg_rf'])

print(f'random forest AUC score: {auc_rf}')
print(f'random log loss score: {ll_rf}')

test_df['xg'] = log.predict_proba(test_df[feature_columns])[:, 1]

auc=roc_auc_score(test_df[target], test_df['xg'])
ll = log_loss(test_df[target], test_df['xg'])

print(f'logreg AUC score: {auc}')
print(f'logreg log loss score: {ll}')

test_df.to_csv('test_xg.csv', index=False)
with open('logreg_model', 'wb') as f:
    pickle.dump(log, f)
