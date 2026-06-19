from django.contrib import admin
from .models import Student, Bank, LoanBid, LoanCriteria, Profile, LoanProduct

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
