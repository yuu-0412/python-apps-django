from django.contrib import admin
from .models import ClockPhoto

@admin.register(ClockPhoto)
class ClockPhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "uploaded_at")