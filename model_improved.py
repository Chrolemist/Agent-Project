import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.datasets import make_regression
import lightgbm as lgb
import xgboost as xgb
import optuna
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=lgb.LGBMDeprecationWarning)
warnings.filterwarnings('ignore', category=xgb.XGBoostDeprecationWarning)

def create_synthetic_data(n_samples=2000, n_features=20, n_informative=15, noise=0.8, random_state=42):
    # Generate synthetic regression data
    X, y = make_regression(n_samples=n_samples, n_features=n_features, n_informative=n_informative,
                           n_targets=1, bias=5.0, noise=noise, random_state=random_state)
    
    # Introduce non-linear relationships and interactions to benefit feature engineering
    if n_features >= 2:
        y = y + 0.7 * X[:, 0]**2 + 0.4 * np.sin(X[:, 1]) + 0.2 * X[:, 0] * X[:, 2]
    elif n_features >= 1:
        y = y + 0.7 * X[:, 0]**2

    # Scale y to a specific range for consistent RMSE target
    y = (y - y.mean()) / y.std() * 10 + 100 # Normalize to mean 100, std 10
    
    return X, y

def objective_lgbm(trial, X, y):
    # Hyperparameters for LightGBM
    lgbm_params = {
        'objective': 'regression',
        'metric': 'rmse',
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2, log=True),
        'num_leaves': trial.suggest_int('num_leaves', 20, 100),
        'max_depth': trial.suggest_int('max_depth', 5, 15),
        'min_child_samples': trial.suggest_int('min_child_samples', 20, 100),
        'subsample': trial.suggest_float('subsample', 0.6, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
        'reg_alpha': trial.suggest_float('reg_alpha', 1e-8, 10.0, log=True),
        'reg_lambda': trial.suggest_float('reg_lambda', 1e-8, 10.0, log=True),
        'random_state': 42,
        'n_jobs': -1,
        'verbose': -1, # Suppress verbose output during trials
    }

    # Pipeline with feature engineering and LightGBM model
    model_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('poly', PolynomialFeatures(degree=trial.suggest_int('poly_degree', 1, 3), include_bias=False)),
        ('regressor', lgb.LGBMRegressor(**lgbm_params))
    ])

    # Cross-validation
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    rmse_scores = []
    for train_index, val_index in kf.split(X):
        X_train_fold, X_val_fold = X[train_index], X[val_index]
        y_train_fold, y_val_fold = y[train_index], y[val_index]

        model_pipeline.fit(X_train_fold, y_train_fold)
        preds = model_pipeline.predict(X_val_fold)
        rmse_scores.append(np.sqrt(mean_squared_error(y_val_fold, preds)))

    return np.mean(rmse_scores)

def objective_xgb(trial, X, y):
    # Hyperparameters for XGBoost
    xgb_params = {
        'objective': 'reg:squarederror',
        'eval_metric': 'rmse',
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2, log=True),
        'max_depth': trial.suggest_int('max_depth', 5, 15),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
        'gamma': trial.suggest_float('gamma', 1e-8, 1.0, log=True),
        'subsample': trial.suggest_float('subsample', 0.6, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
        'reg_alpha': trial.suggest_float('reg_alpha', 1e-8, 10.0, log=True),
        'reg_lambda': trial.suggest_float('reg_lambda', 1e-8, 10.0, log=True),
        'random_state': 42,
        'n_jobs': -1,
    }

    # Pipeline with feature engineering and XGBoost model
    model_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('poly', PolynomialFeatures(degree=trial.suggest_int('poly_degree', 1, 3), include_bias=False)),
        ('regressor', xgb.XGBRegressor(**xgb_params))
    ])

    # Cross-validation
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    rmse_scores = []
    for train_index, val_index in kf.split(X):
        X_train_fold, X_val_fold = X[train_index], X[val_index]
        y_train_fold, y_val_fold = y[train_index], y[val_index]

        model_pipeline.fit(X_train_fold, y_train_fold)
        preds = model_pipeline.predict(X_val_fold)
        rmse_scores.append(np.sqrt(mean_squared_error(y_val_fold, preds)))

    return np.mean(rmse_scores)


if __name__ == '__main__':
    # 1. Data Generation
    X, y = create_synthetic_data()
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 2. Hyperparameter Optimization with Optuna for LightGBM
    print("Starting Optuna study for LightGBM...")
    study_lgbm = optuna.create_study(direction='minimize', sampler=optuna.samplers.TPESampler(seed=42))
    # Passing X_train, y_train to the objective function
    study_lgbm.optimize(lambda trial: objective_lgbm(trial, X_train, y_train), n_trials=50, show_progress_bar=False)
    print("LightGBM Optuna study finished.")
    print(f"Best cross-validation RMSE for LightGBM: {study_lgbm.best_value:.4f}")
    
    # 3. Hyperparameter Optimization with Optuna for XGBoost
    print("Starting Optuna study for XGBoost...")
    study_xgb = optuna.create_study(direction='minimize', sampler=optuna.samplers.TPESampler(seed=42))
    study_xgb.optimize(lambda trial: objective_xgb(trial, X_train, y_train), n_trials=50, show_progress_bar=False)
    print("XGBoost Optuna study finished.")
    print(f"Best cross-validation RMSE for XGBoost: {study_xgb.best_value:.4f}")

    # 4. Retrain best models on full training data
    print("Retraining best models on full training data...")

    # Best LightGBM pipeline
    best_lgbm_params = study_lgbm.best_trial.params
    # Extract poly_degree for PolynomialFeatures within the Pipeline
    best_lgbm_poly_degree = best_lgbm_params.pop('poly_degree') 
    
    best_lgbm_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('poly', PolynomialFeatures(degree=best_lgbm_poly_degree, include_bias=False)),
        ('regressor', lgb.LGBMRegressor(**best_lgbm_params, random_state=42, n_jobs=-1, verbose=-1))
    ])
    best_lgbm_pipeline.fit(X_train, y_train)

    # Best XGBoost pipeline
    best_xgb_params = study_xgb.best_trial.params
    # Extract poly_degree for PolynomialFeatures within the Pipeline
    best_xgb_poly_degree = best_xgb_params.pop('poly_degree') 
    
    best_xgb_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('poly', PolynomialFeatures(degree=best_xgb_poly_degree, include_bias=False)),
        ('regressor', xgb.XGBRegressor(**best_xgb_params, random_state=42, n_jobs=-1))
    ])
    best_xgb_pipeline.fit(X_train, y_train)

    # 5. Ensemble predictions on the test set
    print("Making ensemble predictions...")
    preds_lgbm = best_lgbm_pipeline.predict(X_test)
    preds_xgb = best_xgb_pipeline.predict(X_test)
    
    # Simple averaging ensemble for final prediction
    ensemble_preds = (preds_lgbm + preds_xgb) / 2

    # 6. Evaluate the ensemble model
    final_rmse = np.sqrt(mean_squared_error(y_test, ensemble_preds))
    final_r2 = r2_score(y_test, ensemble_preds)

    print("\n--- Final Ensemble Model Performance ---")
    print(f"Ensemble RMSE: {final_rmse:.4f}")
    print(f"Ensemble R^2: {final_r2:.4f}")

    # Check against target metrics
    if final_r2 > 0.8 and final_rmse < 5.0:
        print("Performance target achieved: R^2 > 0.8 and RMSE < 5.0")
    else:
        print("Performance target NOT met.")