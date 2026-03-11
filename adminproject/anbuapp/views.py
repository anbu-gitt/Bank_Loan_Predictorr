
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import get_user_model,authenticate,login
from django.contrib.auth.decorators import login_required
users=get_user_model()




def login_page(request):
    error_message=None
    if request.method == 'POST':
        username=request.POST.get('username','').strip()
        password=request.POST.get('password','').strip()
        user= authenticate(request,username=username,password=password)
        if user is not None:
           login(request,user) 
           return redirect('home')
        else:
             error_message='invalid username or password'
    return render(request,'login.html',{
        "error_message":error_message
        }) 

def register_page(request):
    
    if request.method == 'POST':
        username=request.POST.get('username')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        password=request.POST.get('password')
        address=request.POST.get('address')
        user=users(username=username,phone=phone,email=email,password=password,address=address)
        user.set_password(password)
        user.save()
        return redirect('login')
    else:
     return render(request,'register.html')


from django.shortcuts import render, get_object_or_404, redirect
from .models import LoanPrediction
@login_required(login_url='login')
def prediction_list(request):
    loans = LoanPrediction.objects.all()
    return render(request, "prediction_list.html", {"loans": loans})  
 
@login_required(login_url='login')
def edit_prediction(request, id):
    loan = get_object_or_404(LoanPrediction,id=id)

    if request.method == "POST":
        loan.loan_id = request.POST.get("loan_id")
        loan.no_of_dependents = request.POST.get("no_of_dependents")
        loan.education = request.POST.get("education")
        loan.self_employed = request.POST.get("self_employed")
        loan.income_annum = request.POST.get("income_annum")
        loan.loan_amount = request.POST.get("loan_amount")
        loan.loan_term = request.POST.get("loan_term")
        loan.cibil_score = request.POST.get("cibil_score")
        loan.residential_assets_value = request.POST.get("residential_assets_value")
        loan.commercial_assets_value = request.POST.get("commercial_assets_value")
        loan.luxury_assets_value = request.POST.get("luxury_assets_value")
        loan.bank_asset_value = request.POST.get("bank_asset_value")

        loan.save()
        return redirect("prediction_list")

    return render(request, "edit_prediction.html", {"loan": loan}) 
@login_required(login_url='login')
def delete_prediction(request, id):
    loan = get_object_or_404(LoanPrediction, id=id)
    loan.delete()
    return redirect("prediction_list")
 
 
#loan model

from django.shortcuts import render
import pandas as ai
import joblib
import os
from django.conf import settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
from .models import LoanPrediction

encoder = joblib.load(os.path.join(BASE_DIR, "encoder.joblib")) 

BASE_DIR = settings.BASE_DIR

model_path = os.path.join(BASE_DIR, "anbuapp", "loan_model_joblib")
encoder_path = os.path.join(BASE_DIR, "anbuapp", "encoder.joblib")

model = joblib.load(model_path)
encoder = joblib.load(encoder_path)

catogarical_col = ['education','loan_status','self_employed']

@login_required(login_url='login') 
def home_page(request):
    prediction = None
    
    if request.method == 'POST':
        education = request.POST.get("education")
        self_employed = request.POST.get("self_employed")

        data={
            "loan_id":int(request.POST.get("loan_id")),
            "no_of_dependents":int(request.POST.get("no_of_dependents")),
             "education": request.POST.get("education").strip(),
            "self_employed":request.POST.get("self_employed").strip(),
            "income_annum":int(request.POST.get("income_annum")),
            "loan_amount":int(request.POST.get("loan_amount")),
            "cibil_score":int(request.POST.get("cibil_score")),
            "residential_assets_value":int(request.POST.get("residential_assets_value")),
            "commercial_assets_value":int(request.POST.get("commercial_assets_value")),
            "luxury_assets_value":int(request.POST.get("luxury_assets_value")),
            "bank_asset_value":int(request.POST.get("bank_asset_value")),
            "loan_term": int(request.POST.get("loan_term"))
        }

        loan=ai.DataFrame([data])
        
        loan["education"] = encoder["education"].transform(loan["education"])
        loan["self_employed"] = encoder["self_employed"].transform(loan["self_employed"])
    
        loan = loan[model.feature_names_in_]
       
    
         # Predict
        pred = model.predict(loan)
        prediction = encoder["loan_status"].inverse_transform(pred)[0]
        LoanPrediction.objects.create(
    loan_id=data["loan_id"],
    no_of_dependents=data["no_of_dependents"],
    education=data["education"],
    self_employed=data["self_employed"],
    income_annum=data["income_annum"],
    loan_amount=data["loan_amount"],
    loan_term=data["loan_term"],
    cibil_score=data["cibil_score"],
    residential_assets_value=data["residential_assets_value"],
    commercial_assets_value=data["commercial_assets_value"],
    luxury_assets_value=data["luxury_assets_value"],
    bank_asset_value=data["bank_asset_value"],
    loan_status=prediction
)
    return render(request,'home.html',{"prediction": prediction})
    
    
