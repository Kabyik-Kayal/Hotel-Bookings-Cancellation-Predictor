from scipy.stats import randint, uniform

LIGHTGBM_PARAMS = {
    "n_estimators": randint(100, 1000),
    "max_depth": randint(5, 100),
    "learning_rate": uniform(0.01, 0.2),
    "num_leaves": randint(20, 100),
    "boosting_type": ["gbdt","dart"]
}

RANDOM_SEARCH_PARAMS = {
    "n_iter": 20,
    "cv": 3,
    "n_jobs": 1,
    "verbose": 2,
    "random_state": 42,
    "scoring": "accuracy"
}