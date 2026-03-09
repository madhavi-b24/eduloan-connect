from django.urls import path
from .views import students, loan_offers,potential_score,loan_bids,best_loan_offer,calculate_emi,accept_loan,download_sanction_letter,eligible_banks

urlpatterns = [
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