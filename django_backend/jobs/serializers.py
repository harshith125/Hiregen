from rest_framework import serializers
from .models import JobPosting, ReferralRequest

class JobPostingSerializer(serializers.ModelSerializer):
    posted_by_username = serializers.ReadOnlyField(source='posted_by.username')

    class Meta:
        model = JobPosting
        fields = '__all__'
        read_only_fields = ('posted_by',)

class ReferralRequestSerializer(serializers.ModelSerializer):
    student_username = serializers.ReadOnlyField(source='student.username')
    job_title = serializers.ReadOnlyField(source='job_posting.job_title')
    company_name = serializers.ReadOnlyField(source='job_posting.company_name')

    class Meta:
        model = ReferralRequest
        fields = '__all__'
        read_only_fields = ('student', 'status', 'created_at')
