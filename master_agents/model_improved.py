import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import KFold
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.metrics import mean_squared_error
import optuna
import random
import sys

# Set a random seed for reproducibility
np.random.seed(42)
random.seed(42)

# --- 1. Synthetic Data Generation ---
# Create a synthetic dataset that allows for near-exact predictions
# Target values will be somewhat large to make 1-2 integer error significant
n_samples = 2000
X = np.random.rand(n_samples, 3) * 100 # Features ranging from 0 to 100

# Define a complex non-linear relationship for the target
# y = 5*x1 + 0.05*x2^2 - 0.0005*x3^3 + 10*sin(x1/5) + 5*log(x2+1) + small noise
# Scale factors chosen to make target values reasonably large integers
# Add very small noise to simulate real-world data but keep it highly predictable
y_true = (
    5 * X[:, 0]
    + 0.05 * X[:, 1]**2
    - 0.0005 * X[:, 2]**3
    + 10 * np.sin(X[:, 0] / 5)
    + 5 * np.log(X[:, 1] + 1)
    + np.random.normal(0, 0.5, n_samples) # Small noise standard deviation
)

# Introduce a slight bias or shift to target values for realism, and ensure positive values
y_true = np.maximum(50, y_true + 100) # Shift values up and ensure they are at least 50

# --- 2. Realistic RMSE Target ---
# Based on the "within 1-2 integers" requirement, an RMSE of 1.0-1.5 is ambitious and realistic
REALISTIC_RMSE_TARGET = 1.5

# --- 3. Feature Engineering ---
# Combine original features and polynomial features
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_poly)

# Split data into training and testing sets (manual split for simplicity here, KFold later for CV)
# For final training, we'll use all data with CV
split_idx = int(0.8 * n_samples)
X_train_scaled, X_test_scaled = X_scaled[:split_idx], X_scaled[split_idx:]
y_train, y_test = y_true[:split_idx], y_true[split_idx:]

# --- 4. Hyperparameter Optimization with Optuna ---
def objective(trial):
    params = {
        'objective': 'regression_l1', # MAE objective for robustness to outliers, can also be 'regression' (L2)
        'metric': 'rmse',
        'n_estimators': trial.suggest_int('n_estimators', 100, 2000),
        'learning_rate': trial.suggest_loguniform('learning_rate', 0.005, 0.2),
        'num_leaves': trial.suggest_int('num_leaves', 20, 256),
        'max_depth': trial.suggest_int('max_depth', 5, 15),
        'min_child_samples': trial.suggest_int('min_child_samples', 20, 100),
        'subsample': trial.suggest_loguniform('subsample', 0.6, 1.0),
        'colsample_bytree': trial.suggest_loguniform('colsample_bytree', 0.6, 1.0),
        'reg_alpha': trial.suggest_loguniform('reg_alpha', 1e-8, 10.0),
        'reg_lambda': trial.suggest_loguniform('reg_lambda', 1e-8, 10.0),
        'random_state': 42,
        'n_jobs': -1,
        'verbose': -1, # Suppress verbose output during trials
        'boosting_type': 'gbdt',
        'early_stopping_round': 100 # Using early stopping to prevent overfitting
    }

    # Cross-validation setup
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    rmse_scores = []

    for fold, (train_index, val_index) in enumerate(kf.split(X_train_scaled, y_train)):
        X_train_fold, X_val_fold = X_train_scaled[train_index], X_train_scaled[val_index]
        y_train_fold, y_val_fold = y_train[train_index], y_train[val_index]

        model = lgb.LGBMRegressor(**params)
        model.fit(X_train_fold, y_train_fold,
                  eval_set=[(X_val_fold, y_val_fold)],
                  eval_metric='rmse',
                  callbacks=[lgb.early_stopping(params['early_stopping_round'], verbose=False)])

        predictions = model.predict(X_val_fold)
        rmse = np.sqrt(mean_squared_error(y_val_fold, predictions))
        rmse_scores.append(rmse)

    return np.mean(rmse_scores)

# Run Optuna study
optuna_n_trials = 100 # Number of optimization trials
study = optuna.create_study(direction='minimize', sampler=optuna.samplers.TPESampler(seed=42))
# Disable Optuna warnings if running in a non-interactive environment, for cleaner output
optuna.logging.set_verbosity(optuna.logging.WARNING)
study.optimize(objective, n_trials=optuna_n_trials, show_progress_bar=False)

best_params = study.best_params
# Remove early_stopping_round from best_params before passing to final model
# It's a callback parameter, not a direct model parameter
if 'early_stopping_round' in best_params:
    del best_params['early_stopping_round']

# --- 5. Training the Final Model with Best Hyperparameters ---
final_model = lgb.LGBMRegressor(**best_params, random_state=42, n_jobs=-1, verbose=-1)

# Train on the entire training dataset
final_model.fit(X_train_scaled, y_train)

# --- 6. Prediction and Evaluation ---
predictions_test = final_model.predict(X_test_scaled)
final_rmse = np.sqrt(mean_squared_error(y_test, predictions_test))

print("Model Training and Evaluation Report:")
print(f"Optimal hyperparameters found by Optuna: {study.best_value:.4f} RMSE (Cross-Validation)")
print(f"Final model RMSE on test set: {final_rmse:.4f}")

if final_rmse <= REALISTIC_RMSE_TARGET:
    print(f"Realistic RMSE Target ({REALISTIC_RMSE_TARGET}) ACHIEVED!")
else:
    print(f"Realistic RMSE Target ({REALISTIC_RMSE_TARGET}) NOT achieved.")

# Show some example predictions vs. actuals
print("\nSample Predictions vs. Actuals (Test Set):")
sample_indices = random.sample(range(len(y_test)), min(10, len(y_test)))
for i in sample_indices:
    actual = y_test[i]
    predicted = predictions_test[i]
    difference = abs(actual - predicted)
    print(f"Actual: {actual:.2f}, Predicted: {predicted:.2f}, Difference: {difference:.2f} (Within 1-2 integers: {difference <= 2.0})")