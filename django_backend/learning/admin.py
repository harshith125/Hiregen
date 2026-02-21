from django.contrib import admin
from .models import Roadmap
import json
from django.utils.html import format_html

@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ('student', 'target_role', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('student__username', 'target_role')
    readonly_fields = ('created_at', 'formatted_content')
    
    def formatted_content(self, obj):
        try:
            # Pretty-print the JSON content payload so admins can read the roadmap
            formatted_json = json.dumps(obj.content, indent=2)
            return format_html('<pre>{}</pre>', formatted_json)
        except Exception:
            return obj.content
    formatted_content.short_description = 'AI Roadmap Content'
