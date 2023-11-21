from django.shortcuts import render, redirect

from django.http import HttpResponse

from crisisManagementAssistant.models import CMDoc

from crisisManagementAssistant.forms import CMDocForm

from django.contrib.auth.decorators import login_required



@login_required
def view_all_files(request):

    files = CMDoc.objects.filter(user=request.user)

    file_names_list = [CMDoc.file.name.split('/')[-1] for CMDoc in files]

    return render(request, 'cma/files.html', {'files': files, 'names': file_names_list})

@login_required
def upload_file(request):

    if request.method == 'POST':

        form = CMDocForm(request.POST, request.FILES)

        if form.is_valid():

            obj = form.save(commit = False)

            obj.user=request.user

            obj.save()

            return redirect('view_all_files')

    else:

        form = CMDocForm()

    return render(request, 'cma/new_file.html', {'form': form})


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


@login_required

def delete_file(request, file_id):
    uploaded_file = CMDoc.objects.get(pk=file_id)
    uploaded_file.delete()
    return redirect('view_all_files')

