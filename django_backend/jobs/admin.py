from django.contrib import admin
from .models import JobPosting, ReferralRequest

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company_name', 'posted_by', 'is_referral_available', 'created_at')
    list_filter = ('company_name', 'is_referral_available', 'created_at')
    search_fields = ('job_title', 'company_name', 'posted_by__username')
    ordering = ('-created_at',)

@admin.register(ReferralRequest)
class ReferralRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'get_job_title', 'get_company_name', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('student__username', 'job_posting__job_title', 'job_posting__company_name')
    ordering = ('-created_at',)

    def get_job_title(self, obj):
        return obj.job_posting.job_title
    get_job_title.short_description = 'Job Title'
    get_job_title.admin_order_field = 'job_posting__job_title'
    
    def get_company_name(self, obj):
        return obj.job_posting.company_name
    get_company_name.short_description = 'Company Name'
    get_company_name.admin_order_field = 'job_posting__company_name'
