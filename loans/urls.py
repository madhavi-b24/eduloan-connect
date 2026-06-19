from django.urls import path
from .views import students, loan_offers,potential_score,loan_bids,best_loan_offer,calculate_emi,accept_loan,download_sanction_letter,eligible_banks,student_register,student_login,student_logout
from .rbac_views import (
    AdminStudentListView,
    EligibilityResultDetailView,
    EligibilityResultListView,
    LoanApplicationDetailView,
    LoanApplicationListView,
    LoanRecommendationDetailView,
    LoanRecommendationListView,
    ProfileDetailView,
    ProfileListView,
)

urlpatterns = [
    path('auth/register/', student_register),
    path('auth/login/', student_login),
    path('auth/logout/', student_logout),
    path('rbac/students/', AdminStudentListView.as_view()),
    path('rbac/profiles/', ProfileListView.as_view()),
    path('rbac/profiles/<int:pk>/', ProfileDetailView.as_view()),
    path('rbac/applications/', LoanApplicationListView.as_view()),
    path('rbac/applications/<int:pk>/', LoanApplicationDetailView.as_view()),
    path('rbac/eligibility-results/', EligibilityResultListView.as_view()),
    path('rbac/eligibility-results/<int:pk>/', EligibilityResultDetailView.as_view()),
    path('rbac/recommendations/', LoanRecommendationListView.as_view()),
    path('rbac/recommendations/<int:pk>/', LoanRecommendationDetailView.as_view()),
    path('students/', students),
    path('loan-offers/<int:student_id>/', loan_offers),
    path('score/<int:student_id>/',potential_score),
    path('loan-bids/',loan_bids),
    path('best-offer/<int:student_id>/',best_loan_offer),
    path('emi/<int:loan_id>/',calculate_emi),
    path('accept-loan/<int:loan_id>/',accept_loan),
    path('sanction-letter/<int:loan_id>/',download_sanction_letter),
    path('eligible-banks/<int:student_id>/', eligible_banks),
]
