import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor


# =========================
# Load dataset
# =========================
data = pd.read_csv("dataset/dataset_bloods.csv")

print("Dataset Preview:")
print(data.head())


# =========================
# Preprocessing
# =========================
le = LabelEncoder()
data['Blood_Group'] = le.fit_transform(data['Blood_Group'])


# =========================
# Features and Target
# =========================
X = data[['Month', 'Blood_Group', 'Units_Collected', 'Units_Supplied']]
y = data['Units_Requested']


# =========================
# Train Test Split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# =========================
# Linear Regression Model
# =========================
lr = LinearRegression()
lr.fit(X_train, y_train)

lr_pred = lr.predict(X_test)

lr_mae = mean_absolute_error(y_test, lr_pred)


# =========================
# Random Forest Model
# =========================
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

rf_pred = rf.predict(X_test)

rf_mae = mean_absolute_error(y_test, rf_pred)


# =========================
# Compare Models
# =========================
print("\nModel Comparison:")
print("Linear Regression MAE :", lr_mae)
print("Random Forest MAE    :", rf_mae)


if lr_mae < rf_mae:
    best_model = lr
    best_name = "Linear Regression"
    best_pred = lr_pred
else:
    best_model = rf
    best_name = "Random Forest"
    best_pred = rf_pred


# =========================
# Best Model Evaluation
# =========================
mae = mean_absolute_error(y_test, best_pred)
mse = mean_squared_error(y_test, best_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, best_pred)

print("\n===== Best Model =====")
print("Model :", best_name)

print("\n===== Evaluation Metrics =====")
print("MAE  :", mae)
print("MSE  :", mse)
print("RMSE :", rmse)
print("R2 Score :", r2)


# =========================
# Save Model
# =========================
with open("ml_model/blood_model.pkl", "wb") as f:
    pickle.dump(best_model, f)

print("\nModel saved as blood_model.pkl")


# =========================
# Save Label Encoder (IMPORTANT)
# =========================
with open("ml_model/label_encoder.pkl", "wb") as f:
    pickle.dump(le, f)

print("Label Encoder saved as label_encoder.pkl")