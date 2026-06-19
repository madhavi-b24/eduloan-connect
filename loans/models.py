from django.contrib.auth.models import User
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


class Profile(models.Model):
    ROLE_STUDENT = 'student'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = [
        (ROLE_STUDENT, 'Student'),
        (ROLE_ADMIN, 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_STUDENT)
    phone = models.CharField(max_length=10, blank=True)
    apaar_id = models.CharField(max_length=20, blank=True)
    course = models.CharField(max_length=100, blank=True)
    family_income = models.IntegerField(null=True, blank=True)
    academic_score = models.IntegerField(null=True, blank=True)
    legacy_student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class LoanProduct(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    min_loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    max_loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    max_tenure_years = models.PositiveIntegerField()
    min_family_income = models.DecimalField(max_digits=12, decimal_places=2)
    min_academic_score = models.PositiveIntegerField()
    processing_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    collateral_required = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bank.name} - {self.product_name}"


class LoanApplication(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_SUBMITTED = 'submitted'
    STATUS_UNDER_REVIEW = 'under_review'
    STATUS_ELIGIBLE = 'eligible'
    STATUS_OFFER_GENERATED = 'offer_generated'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_ACCEPTED = 'accepted'

    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_SUBMITTED, 'Submitted'),
        (STATUS_UNDER_REVIEW, 'Under Review'),
        (STATUS_ELIGIBLE, 'Eligible'),
        (STATUS_OFFER_GENERATED, 'Offer Generated'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_ACCEPTED, 'Accepted'),
    ]

    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    legacy_student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    loan_product = models.ForeignKey(LoanProduct, on_delete=models.PROTECT)
    requested_amount = models.DecimalField(max_digits=12, decimal_places=2)
    requested_tenure_years = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.applicant.user.username} - {self.loan_product.product_name}"


class ApplicationStatusEvent(models.Model):
    application = models.ForeignKey(LoanApplication, on_delete=models.CASCADE)
    old_status = models.CharField(max_length=20, choices=LoanApplication.STATUS_CHOICES)
    new_status = models.CharField(max_length=20, choices=LoanApplication.STATUS_CHOICES)
    note = models.TextField(blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.application_id}: {self.old_status} -> {self.new_status}"


class EligibilityResult(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    loan_product = models.ForeignKey(LoanProduct, on_delete=models.CASCADE)
    application = models.ForeignKey(
        LoanApplication,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    eligible = models.BooleanField()
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    reasons = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        status = "Eligible" if self.eligible else "Not eligible"
        return f"{self.profile.user.username} - {self.loan_product.product_name}: {status}"


class LoanRecommendation(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    loan_product = models.ForeignKey(LoanProduct, on_delete=models.CASCADE)
    application = models.ForeignKey(
        LoanApplication,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    rank = models.PositiveIntegerField(default=1)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    estimated_emi = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_repayment = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score']

    def __str__(self):
        return f"{self.profile.user.username} - {self.loan_product.product_name} (Rank {self.rank})"
