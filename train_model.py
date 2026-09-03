import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

data = {

    "temperature": [22,25,28,30,18,15,32,29],

    "humidity": [60,70,85,90,50,40,95,88],

    "rainfall": [0,5,20,50,0,0,80,60],

    "elevation": [200,300,500,700,100,50,800,600],

    "risk": [0,0,1,1,0,0,1,1]
}

df = pd.DataFrame(data)

X = df[
    [
        "temperature",
        "humidity",
        "rainfall",
        "elevation"
    ]
]

y = df["risk"]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

joblib.dump(
    model,
    "models/landslide_model.pkl"
)

print("Model Saved")