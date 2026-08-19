from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import LoanPrediction

import pandas as pd
import pickle
import os


# ============================================================
# USER MODEL
# ============================================================

User = get_user_model()


# ============================================================
# LOGIN
# ============================================================

def login_page(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("home")

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(
        request,
        "login.html"
    )


# ============================================================
# REGISTER
# ============================================================

def register_page(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check username

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect("register")

        # Create user

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            "Account created successfully. Please login."
        )

        return redirect("login")

    return render(
        request,
        "register.html"
    )


# ============================================================
# HOME
# ============================================================

@login_required(login_url="login")
def home_page(request):

    return render(
        request,
        "home.html"
    )


# ============================================================
# ELIGIBILITY - STEP 1
# ============================================================

@login_required(login_url="login")
def eligibility_step1(request):

    if request.method == "POST":

        loan_id = request.POST.get(
            "loan_id"
        )

        no_of_dependents = request.POST.get(
            "no_of_dependents"
        )

        education = request.POST.get(
            "education"
        )

        self_employed = request.POST.get(
            "self_employed"
        )

        # Store data in session

        request.session["loan_id"] = loan_id

        request.session[
            "no_of_dependents"
        ] = no_of_dependents

        request.session[
            "education"
        ] = education

        request.session[
            "self_employed"
        ] = self_employed

        # Go to financial page

        return redirect(
            "eligibility_step2"
        )

    return render(
        request,
        "eligibility.html"
    )


# ============================================================
# ELIGIBILITY - STEP 2
# FINANCIAL DETAILS
# ============================================================

@login_required(login_url="login")
def eligibility_step2(request):

    if request.method == "POST":

        income_annum = request.POST.get(
            "income_annum"
        )

        loan_amount = request.POST.get(
            "loan_amount"
        )

        loan_term = request.POST.get(
            "loan_term"
        )

        cibil_score = request.POST.get(
            "cibil_score"
        )

        # Optional asset fields

        residential_assets = (
            request.POST.get(
                "residential_assets_value"
            ) or 0
        )

        commercial_assets = (
            request.POST.get(
                "commercial_assets_value"
            ) or 0
        )

        luxury_assets = (
            request.POST.get(
                "luxury_assets_value"
            ) or 0
        )

        bank_assets = (
            request.POST.get(
                "bank_asset_value"
            ) or 0
        )

        # Store financial data in session

        request.session[
            "income_annum"
        ] = income_annum

        request.session[
            "loan_amount"
        ] = loan_amount

        request.session[
            "loan_term"
        ] = loan_term

        request.session[
            "cibil_score"
        ] = cibil_score

        request.session[
            "residential_assets_value"
        ] = residential_assets

        request.session[
            "commercial_assets_value"
        ] = commercial_assets

        request.session[
            "luxury_assets_value"
        ] = luxury_assets

        request.session[
            "bank_asset_value"
        ] = bank_assets

        return redirect(
            "eligibility_review"
        )

    return render(
        request,
        "financial.html"
    )


# ============================================================
# REVIEW PAGE
# ============================================================

@login_required(login_url="login")
def eligibility_review(request):

    # Step 1 data

    loan_id = request.session.get(
        "loan_id"
    )

    no_of_dependents = request.session.get(
        "no_of_dependents"
    )

    education = request.session.get(
        "education"
    )

    self_employed = request.session.get(
        "self_employed"
    )

    # Step 2 data

    income_annum = request.session.get(
        "income_annum"
    )

    loan_amount = request.session.get(
        "loan_amount"
    )

    loan_term = request.session.get(
        "loan_term"
    )

    cibil_score = request.session.get(
        "cibil_score"
    )

    residential_assets = request.session.get(
        "residential_assets_value",
        0
    )

    commercial_assets = request.session.get(
        "commercial_assets_value",
        0
    )

    luxury_assets = request.session.get(
        "luxury_assets_value",
        0
    )

    bank_assets = request.session.get(
        "bank_asset_value",
        0
    )

    # Create dictionary

    loan = {

        "loan_id": loan_id,

        "no_of_dependents":
            no_of_dependents,

        "education":
            education,

        "self_employed":
            self_employed,

        "income_annum":
            income_annum,

        "loan_amount":
            loan_amount,

        "loan_term":
            loan_term,

        "cibil_score":
            cibil_score,

        "residential_assets_value":
            residential_assets,

        "commercial_assets_value":
            commercial_assets,

        "luxury_assets_value":
            luxury_assets,

        "bank_asset_value":
            bank_assets,
    }

    return render(
        request,
        "review.html",
        {
            "loan": loan
        }
    )


# ============================================================
# CHECK ELIGIBILITY
# MACHINE LEARNING PREDICTION
# ============================================================

@login_required(login_url="login")
def check_eligibility(request):

    # Only POST request allowed

    if request.method != "POST":

        return redirect(
            "eligibility_step1"
        )

    try:

        # ====================================================
        # 1. GET DATA FROM SESSION
        # ====================================================

        loan_id = request.session.get(
            "loan_id"
        )

        no_of_dependents = request.session.get(
            "no_of_dependents"
        )

        education = request.session.get(
            "education"
        )

        self_employed = request.session.get(
            "self_employed"
        )

        income_annum = request.session.get(
            "income_annum"
        )

        loan_amount = request.session.get(
            "loan_amount"
        )

        loan_term = request.session.get(
            "loan_term"
        )

        cibil_score = request.session.get(
            "cibil_score"
        )

        residential_assets = request.session.get(
            "residential_assets_value",
            0
        )

        commercial_assets = request.session.get(
            "commercial_assets_value",
            0
        )

        luxury_assets = request.session.get(
            "luxury_assets_value",
            0
        )

        bank_assets = request.session.get(
            "bank_asset_value",
            0
        )

        # ====================================================
        # 2. CHECK REQUIRED DATA
        # ====================================================

        if not no_of_dependents:
            raise ValueError(
                "Number of dependents is missing."
            )

        if not income_annum:
            raise ValueError(
                "Annual income is missing."
            )

        if not loan_amount:
            raise ValueError(
                "Loan amount is missing."
            )

        if not loan_term:
            raise ValueError(
                "Loan term is missing."
            )

        if not cibil_score:
            raise ValueError(
                "CIBIL score is missing."
            )

        # ====================================================
        # 3. CONVERT VALUES TO NUMBERS
        # ====================================================

        no_of_dependents = int(
            no_of_dependents
        )

        income_annum = float(
            income_annum
        )

        loan_amount = float(
            loan_amount
        )

        loan_term = float(
            loan_term
        )

        cibil_score = float(
            cibil_score
        )

        residential_assets = float(
            residential_assets or 0
        )

        commercial_assets = float(
            commercial_assets or 0
        )

        luxury_assets = float(
            luxury_assets or 0
        )

        bank_assets = float(
            bank_assets or 0
        )

        # ====================================================
        # 4. CONVERT TEXT TO NUMBERS
        # ====================================================

        if education == "Graduate":

            education_value = 1

        else:

            education_value = 0

        if self_employed == "Yes":

            self_employed_value = 1

        else:

            self_employed_value = 0

        # ====================================================
        # 5. LOAD ML MODEL
        # ====================================================

        model_path = os.path.join(
            os.path.dirname(__file__),
            "loan_model.pkl"
        )

        if not os.path.exists(
            model_path
        ):

            raise FileNotFoundError(
                "loan_model.pkl not found."
            )

        with open(
            model_path,
            "rb"
        ) as file:

            model = pickle.load(
                file
            )

        # ====================================================
        # 6. PREPARE INPUT DATA
        # ====================================================

        input_data = pd.DataFrame([{

            "no_of_dependents":
                no_of_dependents,

            "education":
                education_value,

            "self_employed":
                self_employed_value,

            "income_annum":
                income_annum,

            "loan_amount":
                loan_amount,

            "loan_term":
                loan_term,

            "cibil_score":
                cibil_score,

            "residential_assets_value":
                residential_assets,

            "commercial_assets_value":
                commercial_assets,

            "luxury_assets_value":
                luxury_assets,

            "bank_asset_value":
                bank_assets

        }])

        # ====================================================
        # 7. MACHINE LEARNING PREDICTION
        # ====================================================

        prediction = model.predict(
            input_data
        )

        result = prediction[0]

        # ====================================================
        # 8. CONVERT RESULT
        # ====================================================

        if int(result) == 1:

            eligibility_result = "Eligible"

        else:

            eligibility_result = "Not Eligible"

        # ====================================================
        # 9. SAVE RESULT TO DATABASE
        # ====================================================

        loan = LoanPrediction.objects.create(

            loan_id=loan_id,

            no_of_dependents=
                no_of_dependents,

            education=
                education,

            self_employed=
                self_employed,

            income_annum=
                income_annum,

            loan_amount=
                loan_amount,

            loan_term=
                loan_term,

            cibil_score=
                cibil_score,

            residential_assets_value=
                residential_assets,

            commercial_assets_value=
                commercial_assets,

            luxury_assets_value=
                luxury_assets,

            bank_asset_value=
                bank_assets,

            loan_status=
                eligibility_result
        )

        # ====================================================
        # 10. SHOW RESULT
        # ====================================================

        return render(
            request,
            "result.html",
            {
                "loan": loan,
                "result": eligibility_result
            }
        )

    except Exception as e:

        # Print actual error in terminal

        print(
            "Prediction Error:",
            str(e)
        )

        messages.error(
            request,
            f"Unable to process result: {str(e)}"
        )

        return redirect(
            "eligibility_review"
        )


# ============================================================
# PREDICTION LIST
# ============================================================

@login_required(login_url="login")
def prediction_list(request):

    loans = LoanPrediction.objects.all().order_by(
        "-id"
    )

    return render(
        request,
        "prediction_list.html",
        {
            "loans": loans
        }
    )


# ============================================================
# EDIT PREDICTION
# ============================================================

@login_required(login_url="login")
def edit_prediction(request, id):

    loan = get_object_or_404(
        LoanPrediction,
        id=id
    )

    if request.method == "POST":

        loan.no_of_dependents = request.POST.get(
            "no_of_dependents"
        )

        loan.education = request.POST.get(
            "education"
        )

        loan.self_employed = request.POST.get(
            "self_employed"
        )

        loan.income_annum = request.POST.get(
            "income_annum"
        )

        loan.loan_amount = request.POST.get(
            "loan_amount"
        )

        loan.loan_term = request.POST.get(
            "loan_term"
        )

        loan.cibil_score = request.POST.get(
            "cibil_score"
        )

        loan.residential_assets_value = (
            request.POST.get(
                "residential_assets_value"
            ) or 0
        )

        loan.commercial_assets_value = (
            request.POST.get(
                "commercial_assets_value"
            ) or 0
        )

        loan.luxury_assets_value = (
            request.POST.get(
                "luxury_assets_value"
            ) or 0
        )

        loan.bank_asset_value = (
            request.POST.get(
                "bank_asset_value"
            ) or 0
        )

        loan.save()

        messages.success(
            request,
            "Prediction updated successfully."
        )

        return redirect(
            "prediction_list"
        )

    return render(
        request,
        "edit_prediction.html",
        {
            "loan": loan
        }
    )


# ============================================================
# DELETE PREDICTION
# ============================================================

@login_required(login_url="login")
def delete_prediction(request, id):

    loan = get_object_or_404(
        LoanPrediction,
        id=id
    )

    loan.delete()

    messages.success(
        request,
        "Prediction deleted successfully."
    )

    return redirect(
        "prediction_list"
    )


# ============================================================
# LOGOUT
# ============================================================

@login_required(login_url="login")
def logout_page(request):

    logout(request)

    return redirect(
        "login"
    )