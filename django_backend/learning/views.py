from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Roadmap
from .serializers import RoadmapSerializer
from .services import generate_dynamic_roadmap

class RoadmapViewSet(viewsets.ModelViewSet):
    """
    ViewSet for students to manage and generate their AI roadmaps.
    """
    serializer_class = RoadmapSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users should only see their own roadmaps
        return Roadmap.objects.filter(student=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        # We override standard POST just in case, though the @action below is preferred.
        if self.request.user.role != 'STUDENT':
            raise PermissionDenied("Only students can create learning roadmaps.")
        serializer.save(student=self.request.user)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def generate(self, request):
        """
        Custom POST endpoint to automatically generate via Groq AI.
        Requires `target_role` in request payload.
        """
        user = request.user
        if user.role != 'STUDENT':
            return Response(
                {"detail": "Only students can generate learning roadmaps."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        target_role = request.data.get('target_role')
        if not target_role:
            return Response(
                {"detail": "target_role is required in the request body."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 1. Call Groq service
        roadmap_content = generate_dynamic_roadmap(user, target_role)

        # 2. Save structured DB Record
        new_roadmap = Roadmap.objects.create(
            student=user,
            target_role=target_role,
            content=roadmap_content
        )

        # 3. Return serialized data
        serializer = self.get_serializer(new_roadmap)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
