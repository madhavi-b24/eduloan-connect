from django.contrib import admin
from .models import Student, Bank, LoanBid,LoanCriteria

admin.site.register(Student)
admin.site.register(Bank)
admin.site.register(LoanBid)
admin.site.register(LoanCriteria)