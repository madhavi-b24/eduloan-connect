from rest_framework import serializers
from .models import Student, Bank, LoanBid

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'


class LoanBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanBid
        fields = '__all__'