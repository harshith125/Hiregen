from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('STUDENT', 'Student'),
        ('WORKING_PROFESSIONAL', 'Working Professional'),
    )

    role = models.CharField(max_length=25, choices=ROLE_CHOICES, default='STUDENT')
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # ===============
    # STUDENT FIELDS
    # ===============
    college = models.CharField(max_length=255, blank=True, null=True)
    interested_job_roles = models.JSONField(blank=True, null=True, default=list, help_text="e.g., ['Software Engineer', 'Data Scientist']")
    skills = models.JSONField(blank=True, null=True, default=list, help_text="e.g., ['Python', 'Django', 'React']")
    certifications = models.TextField(blank=True, null=True, help_text="List of certifications")
    
    # Links/Portfolios
    personal_website = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    leetcode_url = models.URLField(blank=True, null=True)
    codeforces_url = models.URLField(blank=True, null=True)
    codechef_url = models.URLField(blank=True, null=True)
    hackerrank_url = models.URLField(blank=True, null=True)

    # ==========================
    # WORKING PROFESSIONAL FIELDS
    # ==========================
    current_company = models.CharField(max_length=255, blank=True, null=True)
    current_job_title = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
