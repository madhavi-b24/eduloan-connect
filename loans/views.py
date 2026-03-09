from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student, Bank, LoanBid,LoanCriteria
from .serializers import StudentSerializer, BankSerializer, LoanBidSerializer
from django.http import HttpResponse
import math
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404


@api_view(['GET', 'POST'])
def students(request):
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(['GET'])
def loan_offers(request, student_id):
    bids = LoanBid.objects.filter(student_id=student_id)
    serializer = LoanBidSerializer(bids, many=True)
    return Response(serializer.data)
def home(request):
    return HttpResponse("Eduloan Backend Running")
@api_view(['GET'])
def potential_score(request, student_id):

    student = Student.objects.get(id=student_id)

    score = (
        0.4 * 80 +
        0.3 * (student.family_income / 100000) +
        0.2 * 70 +
        0.1 * 60
    )

    return Response({
        "student": student.name,
        "potential_score": round(score, 2)
    })
@api_view(['GET','POST'])
def loan_bids(request):

    if request.method == 'GET':
        bids = LoanBid.objects.all()
        serializer = LoanBidSerializer(bids, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = LoanBidSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
@api_view(['GET'])
def best_loan_offer(request, student_id):

    bids = LoanBid.objects.filter(student_id=student_id).order_by('interest_rate').first()

    if not bids:
        return Response({"message": "No loan offers found"})

    data = {
        "student_id": student_id,
        "best_bank": bids.bank.name,
        "interest_rate": bids.interest_rate,
        "loan_amount": bids.loan_amount,
        "tenure_years": bids.tenure_years
    }

    return Response(data)
@api_view(['GET'])
def calculate_emi(request, loan_id):

    from .models import LoanBid

    bid = LoanBid.objects.get(id=loan_id)

    P = bid.loan_amount
    annual_rate = bid.interest_rate
    tenure_years = bid.tenure_years

    r = (annual_rate / 100) / 12
    n = tenure_years * 12

    emi = (P * r * (1+r)**n) / ((1+r)**n - 1)

    data = {
        "bank": bid.bank.name,
        "loan_amount": P,
        "interest_rate": annual_rate,
        "tenure_years": tenure_years,
        "monthly_emi": round(emi, 2)
    }

    return Response(data)
@api_view(['GET','POST'])
def accept_loan(request, loan_id):

    bid = LoanBid.objects.get(id=loan_id)

    # approve selected loan
    bid.status = "approved"
    bid.save()

    # reject other bank bids for the same student
    LoanBid.objects.filter(
        student=bid.student
    ).exclude(id=loan_id).update(status="rejected")

    data = {
        "message": "Loan accepted successfully",
        "approved_bank": bid.bank.name,
        "student": bid.student.name,
        "loan_amount": bid.loan_amount,
        "interest_rate": bid.interest_rate,
        "status": bid.status
    }

    return Response(data)
def download_sanction_letter(request, loan_id):

    bid = get_object_or_404(LoanBid, id=loan_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="loan_sanction_letter.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica", 14)
    p.drawString(200, 800, "Loan Sanction Letter")

    p.setFont("Helvetica", 12)
    p.drawString(100, 740, f"Student: {bid.student.name}")
    p.drawString(100, 710, f"Bank: {bid.bank.name}")
    p.drawString(100, 680, f"Loan Amount: ₹{bid.loan_amount}")
    p.drawString(100, 650, f"Interest Rate: {bid.interest_rate}%")
    p.drawString(100, 620, f"Tenure: {bid.tenure_years} Years")

    p.drawString(100, 560, "Congratulations! Your loan has been approved.")

    p.save()

    return response
@api_view(['GET'])
def eligible_banks(request, student_id):

    student = Student.objects.get(id=student_id)

    banks = LoanCriteria.objects.filter(
        min_score__lte=student.potential_score,
        min_family_income__lte=student.family_income
    )

    data = []

    for b in banks:
        data.append({
            "bank": b.bank.name,
            "max_loan": b.max_loan_amount,
            "interest_limit": b.max_interest_rate
        })

    return Response(data)

