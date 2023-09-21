from django.shortcuts import render, redirect
from django.http import HttpResponse
from crisisManagementAssistant.models import CMDoc
from crisisManagementAssistant.forms import CMDocForm
from django.contrib.auth.decorators import login_required


@login_required
def home_page(request):
    if request.method == 'POST':
        form = CMDocForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home_page')
    else:
        form = CMDocForm()
    files = CMDoc.objects.all()
    return render(request, 'CMA/home.html', {'form': form, 'files': files})


def download_file(request, file_id):
    uploaded_file = CMDoc.objects.get(pk=file_id)
    response = HttpResponse(uploaded_file.fileName, uploaded_file.file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.fileName}"'
    return response
