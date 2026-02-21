from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'groups', 'user_permissions')


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'password', 'role', 'phone_number',
            'college', 'interested_job_roles', 'skills', 'certifications',
            'personal_website', 'linkedin_url', 'github_url', 'leetcode_url',
            'codeforces_url', 'codechef_url', 'hackerrank_url',
            'current_company', 'current_job_title'
        )

    def create(self, validated_data):
        # Extract password to set it properly (hashing it)
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user
