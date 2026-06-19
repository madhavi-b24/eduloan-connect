from django.contrib import admin
from .models import (
    Student,
    Bank,
    LoanBid,
    LoanCriteria,
    Profile,
    LoanProduct,
    LoanApplication,
    ApplicationStatusEvent,
    EligibilityResult,
    LoanRecommendation,
)

admin.site.register(Student)
admin.site.register(Bank)
admin.site.register(LoanBid)
admin.site.register(LoanCriteria)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'course', 'family_income', 'academic_score', 'legacy_student')
    search_fields = ('user__username', 'user__email', 'phone', 'apaar_id', 'course')
    list_filter = ('role', 'course')


@admin.register(LoanProduct)
class LoanProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_name',
        'bank',
        'interest_rate',
        'min_loan_amount',
        'max_loan_amount',
        'max_tenure_years',
        'collateral_required',
        'active',
    )
    search_fields = ('product_name', 'bank__name', 'description')
    list_filter = ('bank', 'collateral_required', 'active')


@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'applicant',
        'legacy_student',
        'loan_product',
        'requested_amount',
        'requested_tenure_years',
        'status',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'applicant__user__username',
        'applicant__user__email',
        'legacy_student__name',
        'legacy_student__email',
        'loan_product__product_name',
        'remarks',
    )
    list_filter = ('status', 'loan_product__bank', 'created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(ApplicationStatusEvent)
class ApplicationStatusEventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'application',
        'old_status',
        'new_status',
        'changed_by',
        'created_at',
    )
    search_fields = (
        'application__applicant__user__username',
        'application__applicant__user__email',
        'application__loan_product__product_name',
        'changed_by__username',
        'changed_by__email',
        'note',
    )
    list_filter = ('old_status', 'new_status', 'changed_by', 'created_at')
    ordering = ('-created_at',)


@admin.register(EligibilityResult)
class EligibilityResultAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'profile',
        'loan_product',
        'application',
        'eligible',
        'score',
        'created_at',
    )
    search_fields = (
        'profile__user__username',
        'profile__user__email',
        'loan_product__product_name',
        'loan_product__bank__name',
    )
    list_filter = ('eligible', 'loan_product__bank', 'created_at')
    ordering = ('-created_at',)


@admin.register(LoanRecommendation)
class LoanRecommendationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'profile',
        'loan_product',
        'application',
        'rank',
        'score',
        'estimated_emi',
        'total_repayment',
        'created_at',
    )
    search_fields = (
        'profile__user__username',
        'profile__user__email',
        'loan_product__product_name',
        'loan_product__bank__name',
        'reason',
    )
    list_filter = ('loan_product__bank', 'created_at')
    ordering = ('-score',)
