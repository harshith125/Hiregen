from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import JobPosting, ReferralRequest
from .serializers import JobPostingSerializer, ReferralRequestSerializer

class IsProfessionalOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow professionals to create standard jobs.
    Anyone can read.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'WORKING_PROFESSIONAL'

class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.all().order_by('-created_at')
    serializer_class = JobPostingSerializer
    permission_classes = [IsProfessionalOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

class ReferralRequestViewSet(viewsets.ModelViewSet):
    serializer_class = ReferralRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'STUDENT':
            # Students can see their own requests
            return ReferralRequest.objects.filter(student=user).order_by('-created_at')
        elif user.role == 'WORKING_PROFESSIONAL':
            # Professionals can see requests for their job postings
            return ReferralRequest.objects.filter(job_posting__posted_by=user).order_by('-created_at')
        return ReferralRequest.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'STUDENT':
            raise PermissionDenied("Only students can create referral requests.")
        
        # We can pass status='PENDING' here manually if we want to enforce it,
        # but the default model value is already PENDING.
        serializer.save(student=user)

    def partial_update(self, request, *args, **kwargs):
        """
        Professionals can accept or reject the referral
        """
        if request.user.role != 'WORKING_PROFESSIONAL':
            raise PermissionDenied("Only professionals can update the referral status.")
        
        # Only allow changing 'status'
        allowed_keys = ['status']
        data = {k: v for k, v in request.data.items() if k in allowed_keys}
        
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
