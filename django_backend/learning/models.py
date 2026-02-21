from django.db import models
from django.conf import settings

class Roadmap(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='roadmaps'
    )
    target_role = models.CharField(max_length=255)
    content = models.JSONField(help_text="Stores the structured JSON AI response")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Roadmap for {self.student.username} -> {self.target_role}"
