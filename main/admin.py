from django.contrib import admin
from .models import Tutorial
from django.db import models
from tinymce import TinyMCE


# Register your models here.

class TutorialAdmin(admin.ModelAdmin):
    # fields = ["tutorial_title",
    #           "tutorial_published",
    #           "tutorial_content"
    #           ]
    # I want to show them in fieldsets with my category

    fieldsets = [
        ("Title and Date", {"fields": ["tutorial_title", "tutorial_published"]}),
        ("Content", {"fields": ["tutorial_content"]}),

    ]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }


admin.site.register(Tutorial, TutorialAdmin)
