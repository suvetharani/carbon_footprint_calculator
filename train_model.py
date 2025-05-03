import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

df = pd.read_csv("model/7d69f80f-571c-4cef-bc77-e3608f3d3741.csv")

features = [
    "Heating Energy Source", "Transport", "Vehicle Type", "Monthly Grocery Bill",
    "Vehicle Monthly Distance Km", "Waste Bag Weekly Count", "How Long TV PC Daily Hour",
    "How Many New Clothes Monthly", "How Long Internet Daily Hour"
]

df = df[features + ["CarbonEmission"]].dropna()

label_encoders = {}
for col in df.select_dtypes(include="object"):
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

X = df[features]
y = df["CarbonEmission"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor()
model.fit(X_train, y_train)

os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/carbon_model.pkl")
joblib.dump(label_encoders, "model/label_encoders.pkl")
print("✅ Model trained and saved!")
