from django.urls import path

from . import views


urlpatterns = [

    # ========================================================
    # LOGIN
    # ========================================================

    path(
        "",
        views.login_page,
        name="login"
    ),


    # ========================================================
    # REGISTER
    # ========================================================

    path(
        "register/",
        views.register_page,
        name="register"
    ),


    # ========================================================
    # HOME
    # ========================================================

    path(
        "home/",
        views.home_page,
        name="home"
    ),


    # ========================================================
    # LOAN ELIGIBILITY
    # ========================================================

    path(
        "eligibility/",
        views.eligibility_step1,
        name="eligibility_step1"
    ),


    # ========================================================
    # FINANCIAL DETAILS
    # ========================================================

    path(
        "eligibility/financial/",
        views.eligibility_step2,
        name="eligibility_step2"
    ),


    # ========================================================
    # REVIEW
    # ========================================================

    path(
        "eligibility/review/",
        views.eligibility_review,
        name="eligibility_review"
    ),


    # ========================================================
    # ML PREDICTION
    # ========================================================

    path(
        "eligibility/check/",
        views.check_eligibility,
        name="check_eligibility"
    ),


    # ========================================================
    # PREDICTION HISTORY
    # ========================================================

    path(
        "predictions/",
        views.prediction_list,
        name="prediction_list"
    ),


    # ========================================================
    # EDIT
    # ========================================================

    path(
        "predictions/edit/<int:id>/",
        views.edit_prediction,
        name="edit_prediction"
    ),


    # ========================================================
    # DELETE
    # ========================================================

    path(
        "predictions/delete/<int:id>/",
        views.delete_prediction,
        name="delete_prediction"
    ),


    # ========================================================
    # LOGOUT
    # ========================================================

    path(
        "logout/",
        views.logout_page,
        name="logout"
    ),

]