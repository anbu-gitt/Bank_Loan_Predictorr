
import os

import joblib
import pandas as ai
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "loan.csv")

loan = ai.read_csv(csv_path)
for col in loan.select_dtypes(include="object").columns:
    loan[col] = loan[col].str.strip()
# loan data 
loan.columns = loan.columns.str.strip()
print(loan) 

loan.replace("",float("nan"),inplace=True)

print(loan)

print(loan.columns)

# print([repr(c) for c in loan.columns])

catogarical_col = ['education','loan_status','self_employed']
encoder={}

for col in catogarical_col:
    le = LabelEncoder()
    loan[col]=le.fit_transform(loan[col])
    encoder[col]=le

print(loan)

# print(loan.dtypes) 

loan.fillna(loan.mean(),inplace=True)
print(loan)

x=loan.drop('loan_status',axis=1)

print(x)

y=loan['loan_status']
print(y)



x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)


model=DecisionTreeClassifier(random_state=42)  
model.fit(x_train,y_train)   

y_pred=model.predict(x_test)
accuracy=accuracy_score(y_test,y_pred)
print("accuracy:",accuracy)

model_path = os.path.join(BASE_DIR, "loan_model_joblib")
encoder_path = os.path.join(BASE_DIR, "encoder.joblib")

joblib.dump(model, model_path)
joblib.dump(encoder, encoder_path)

# print("Model saved at:", model_path)
# print("Encoder saved at:", encoder_path)

# print("Education Classes:", encoder["education"].classes_)
# print("Unique Education Values:", loan["education"].unique())