from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    course = models.CharField(max_length=100)
    family_income = models.IntegerField()
    apaar_id=models.CharField(max_length=20)
    potential_score=models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Bank(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class LoanBid(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    bank = models.ForeignKey('Bank', on_delete=models.CASCADE)
    interest_rate = models.FloatField()
    loan_amount = models.IntegerField()
    tenure_years = models.IntegerField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    collateral_document=models.FileField(upload_to="collateral/",null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def _str_(self):
        return f"{self.bank.name} bid for {self.student.name}"
class LoanCriteria(models.Model):
    bank = models.ForeignKey('Bank', on_delete=models.CASCADE)

    min_score = models.IntegerField()
    min_family_income = models.IntegerField()
    max_loan_amount = models.IntegerField()
    max_interest_rate = models.FloatField()

    def __str__(self):
        return self.bank.name