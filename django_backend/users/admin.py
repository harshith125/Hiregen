from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    
    # Define how standard fields show up
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    
    # Custom grouping in the admin page's edit/creation form
    fieldsets = UserAdmin.fieldsets + (
        ('Advanced Profile Info', {
            'fields': (
                'role', 'phone_number'
            )
        }),
        ('Student Specific', {
            'fields': (
                'college', 'interested_job_roles', 'skills', 'certifications',
                'personal_website', 'linkedin_url', 'github_url', 'leetcode_url',
                'codeforces_url', 'codechef_url', 'hackerrank_url'
            ),
            'classes': ('collapse',), # Collapsed by default to save space
        }),
        ('Professional Specific', {
            'fields': (
                'current_company', 'current_job_title'
            ),
            'classes': ('collapse',),
        }),
    )

admin.site.register(User, CustomUserAdmin)
