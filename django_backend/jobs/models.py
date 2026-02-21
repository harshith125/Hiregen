from django.db import models
from django.conf import settings

class JobPosting(models.Model):
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_postings')
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    description = models.TextField()
    required_skills = models.JSONField(blank=True, null=True, default=list, help_text="e.g., ['Python', 'Django']")
    is_referral_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

class ReferralRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    )

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='referral_requests')
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='referral_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    message = models.TextField(blank=True, null=True, help_text="Optional pitch message from the student")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} -> {self.job_posting.job_title} ({self.status})"
