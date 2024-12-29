from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
import os

def validate_file_size(value):
    filesize = value.size
    if filesize < 102400:  # 100KB
        raise ValidationError("File size must be at least 100KB")
    elif filesize > 10485760:  # 10MB
        raise ValidationError("File size cannot exceed 10MB")

class UploadedFile(models.Model):
    CATEGORY_CHOICES = [
        ('AUDIO', 'Audio'),
        ('VIDEO', 'Video'),
        ('IMAGE', 'Image')
    ]
    
    file = models.FileField(
        upload_to='uploads/',
        validators=[
            FileExtensionValidator(allowed_extensions=['mp3', 'mp4', 'jpeg', 'png', 'gif']),
            validate_file_size
        ]
    )
    filename = models.CharField(max_length=255, default="Default_Value.png")  
    name = models.CharField(max_length=255, default="Default_Value")  
    size = models.BigIntegerField(default=10000)  #in bytes
    file_type = models.CharField(max_length=10, default="jpeg")  
    upload_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES, default="IMAGE")

    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            self.filename = self.file.name
            self.size = self.file.size
            self.file_type = self.get_file_type()
            self.category = self.determine_category()
        super().save(*args, **kwargs)

    def get_file_type(self):
        return os.path.splitext(self.file.name)[1][1:].lower()

    def determine_category(self):
        file_type = self.get_file_type()
        if file_type == 'mp3':
            return 'AUDIO'
        elif file_type == 'mp4':
            return 'VIDEO'
        return 'IMAGE'

    def get_formatted_size(self):
        return filesizeformat(self.size)

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.filename
    
    
    
