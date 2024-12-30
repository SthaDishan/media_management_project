import os  
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UploadedFile
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_POST



def upload_file(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        
        if len(files) > 10:
            messages.error(request, 'You can only upload up to 10 files at once.')
            return redirect('upload_file')
            
        for file in files:
            try:
                # Extract file details
                filename = file.name
                size = file.size
                file_extension = os.path.splitext(filename)[1][1:].lower()  # File extension without the dot
                name = os.path.splitext(filename)[0]
                
                # Determine category based on extension
                CATEGORY_CHOICES = {
                    'IMAGE': ['jpeg', 'png', 'gif'],
                    'VIDEO': ['mp4'],
                    'AUDIO': ['mp3'],
                    # Add more categories if needed
                }
                category = next((key for key, exts in CATEGORY_CHOICES.items() if file_extension in exts), 'IMAGE')
                
                # Create and save the UploadedFile instance
                uploaded_file = UploadedFile(
                    file=file,
                    name=name,
                    filename=filename,
                    size=size,
                    file_type=file_extension,
                    category=category
                )
                uploaded_file.full_clean()
                uploaded_file.save()
                messages.success(request, f'Successfully uploaded {filename}')
            except ValidationError as e:
                messages.error(request, f'Error uploading {filename}: {e}')
                
    files = UploadedFile.objects.all().order_by('-upload_date')
    return redirect('/')


@require_POST
def delete_file(request, file_id):
    try:
        file = get_object_or_404(UploadedFile, id=file_id)
        filename = file.filename
        file.delete()
        messages.success(request, f'Successfully deleted {filename}')
        return redirect('upload_file')
    except Exception as e:
        messages.error(request, f'Error deleting file: {str(e)}')
        return redirect('upload_file')
    
def delete_all_file(request):
    try:
        all_objects= UploadedFile.objects.all()
        for ao in all_objects:
            if os.path.isfile(ao.file.path):
                os.remove(ao.file.path)
        all_objects.delete()
        messages.success(request, f'Successfully deleted all files')
        return redirect('upload_file')
    except Exception as e:
        messages.error(request, f'Error deleting file: {str(e)}')
        return redirect('upload_file')
    

def get_view(request):
    files = UploadedFile.objects.all().order_by('-upload_date')
    return render(request, 'file_upload/upload.html', {'files': files})
