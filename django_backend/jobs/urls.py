from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobPostingViewSet, ReferralRequestViewSet

router = DefaultRouter()
router.register(r'postings', JobPostingViewSet, basename='job-postings')
router.register(r'requests', ReferralRequestViewSet, basename='referral-requests')

urlpatterns = [
    path('', include(router.urls)),
]
