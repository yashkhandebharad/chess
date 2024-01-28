
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadFileForm
from .models import UploadedFile
from wsgiref.util import FileWrapper
from django.shortcuts import get_object_or_404
import mimetypes
import os

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload')
    else:
        form = UploadFileForm()
    return render(request, 'filehandler/upload.html', {'form': form})

def download_file(request):
    latest_file = UploadedFile.objects.order_by('-id').first()
    
    return render(request, 'filehandler/download.html', {'latest_file': latest_file})

    #files = UploadedFile.objects.all()

    #response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename=downloaded_files.pdf'

    # Create a PDF file by concatenating all uploaded files
   # with open(response['Content-Disposition'], 'wb') as pdf_file:
    #    for file in files:
     #       file_path = file.file.path
      #      with open(file_path, 'rb') as file_content:
       #         pdf_file.write(file_content.read())

    #return render(request, 'filehandler/download.html', {'files': files})

# Create your views here.

def download_pdf(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)

    with open(uploaded_file.file.path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file.name}"'
        return response

def upload_success(request):
    return render(request, 'filehandler/upload_success.html')