from django.contrib import admin
from .models import FaceImage
# Register your models here.

class FaceImageAdmin(admin.ModelAdmin):
    pass 


admin.site.register(FaceImage)

