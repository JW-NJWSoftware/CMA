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
            obj = form.save(commit = False)
            obj.user=request.user
            obj.save()
            return redirect('home_page')
    else:
        form = CMDocForm()
    files = CMDoc.objects.all()
    return render(request, 'cma/home.html', {'form': form, 'files': files})

@login_required
def view_file(request, slug=None):
    cmdoc_obj = None
    if slug is not None:
        cmdoc_obj = CMDoc.objects.get(slug=slug)
    return render(request, 'cma/view_CMDoc.html', {'CMDoc': cmdoc_obj})

@login_required
def download_file(request, file_id):
    uploaded_file = CMDoc.objects.get(pk=file_id)
    response = HttpResponse(uploaded_file.file.name, uploaded_file.file)
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file.name}"'
    return response
