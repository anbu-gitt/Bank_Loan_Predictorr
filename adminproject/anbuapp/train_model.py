import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# -----------------------------------------
# 1. Read CSV file
# -----------------------------------------

df = pd.read_csv("loan.csv")


# -----------------------------------------
# 2. Remove spaces from column names
# -----------------------------------------

df.columns = df.columns.str.strip()


# -----------------------------------------
# 3. Remove spaces from text values
# -----------------------------------------

df["education"] = df["education"].astype(str).str.strip()

df["self_employed"] = (
    df["self_employed"]
    .astype(str)
    .str.strip()
)

df["loan_status"] = (
    df["loan_status"]
    .astype(str)
    .str.strip()
)


# -----------------------------------------
# 4. Check loan status values
# -----------------------------------------

print("Loan Status Values:")
print(df["loan_status"].value_counts())


# -----------------------------------------
# 5. Convert categorical values
# -----------------------------------------

df["education"] = df["education"].map({
    "Graduate": 1,
    "Not Graduate": 0
})


df["self_employed"] = df["self_employed"].map({
    "Yes": 1,
    "No": 0
})


df["loan_status"] = df["loan_status"].map({
    "Approved": 1,
    "Rejected": 0
})


# -----------------------------------------
# 6. Fill missing values
# -----------------------------------------

df = df.fillna(0)


# -----------------------------------------
# 7. Input columns
# -----------------------------------------

X = df[
    [
        "no_of_dependents",
        "education",
        "self_employed",
        "income_annum",
        "loan_amount",
        "loan_term",
        "cibil_score",
        "residential_assets_value",
        "commercial_assets_value",
        "luxury_assets_value",
        "bank_asset_value"
    ]
]


# -----------------------------------------
# 8. Target column
# -----------------------------------------

y = df["loan_status"]


# -----------------------------------------
# 9. Check target classes
# -----------------------------------------

print("Target Classes:")
print(y.value_counts())


# -----------------------------------------
# 10. Split data
# -----------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# -----------------------------------------
# 11. Create model
# -----------------------------------------

model = LogisticRegression(
    max_iter=1000
)


# -----------------------------------------
# 12. Train model
# -----------------------------------------

model.fit(
    X_train,
    y_train
)


# -----------------------------------------
# 13. Test model
# -----------------------------------------

prediction = model.predict(X_test)


# -----------------------------------------
# 14. Calculate accuracy
# -----------------------------------------

accuracy = accuracy_score(
    y_test,
    prediction
)

print("Model trained successfully!")

print(
    "Accuracy:",
    accuracy
)


# -----------------------------------------
# 15. Save model
# -----------------------------------------

with open(
    "loan_model.pkl",
    "wb"
) as file:

    pickle.dump(
        model,
        file
    )


print(
    "loan_model.pkl created successfully!"
)