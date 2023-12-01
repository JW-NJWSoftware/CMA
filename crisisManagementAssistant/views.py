from django.shortcuts import render, redirect

from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404

from crisisManagementAssistant.models import CMDoc
from authentication.models import CustomUser

from django.core.exceptions import PermissionDenied

from crisisManagementAssistant.forms import CMDocForm

from django.contrib.auth.decorators import login_required

from ResilienceAI.cdn.conf import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_LOCATION, AWS_STORAGE_BUCKET_NAME, AWS_S3_ENDPOINT_URL, AWS_REGION_NAME
from ResilienceAI.services import extract_info_via_api

from botocore.exceptions import ClientError

import boto3, requests


@login_required
def manage(request):
    group = request.user.group
    users = {}

    if group:
        users = CustomUser.objects.filter(group=group)

    return render(request, 'cma/manage.html', {'group': users})

@login_required
def add_to_group(request):
    userEmail = request.GET.get('user_email') or None

    if userEmail:
        user = CustomUser.objects.get(email=userEmail)
        
        if user.group is None:
            user.group = request.user.group
            user.save()

    return redirect('manage')

@login_required
def new_group(request):
    group_name = request.GET.get('group_name') or None

    if group_name:
        user = request.user
        
        if user.group is None:
            user.group = group_name
            user.save()

    return redirect('manage')

@login_required
def view_all_files(request):

    files = CMDoc.objects.filter(user=request.user)

    file_names_list = [CMDoc.file.name.split('/')[-1] for CMDoc in files]

    return render(request, 'cma/files.html', {'files': files, 'names': file_names_list})

@login_required
def upload_file(request):

    if request.method == 'POST':

        form = CMDocForm(request.POST or None, request.FILES or None)

        if form.is_valid():

            obj = form.save(commit = False)
            obj.user=request.user   
            obj.save()
            
            extracted = extract_info_via_api(obj.file)
            obj.extractData = extracted

            obj.save()

            return redirect('view_all_files')

    else:

        form = CMDocForm()

    return render(request, 'cma/new_file.html', {'form': form})


@login_required

def view_file(request, slug=None):

    file_obj = None

    if slug is not None:

        file_obj = get_object_or_404(CMDoc, slug=slug)

        if file_obj.user != request.user:
            raise PermissionDenied

        data = file_obj.extractData

        summary = data.get('summary')

    return render(request, 'cma/view_CMDoc.html', {'CMDoc': file_obj, 'summary': str(summary)})


@login_required

def download_file(request, file_id):

    file_obj = get_object_or_404(CMDoc, pk=file_id)

    if file_obj.user != request.user:
        raise PermissionDenied

    fileName = file_obj.file.name.split('/')[-1]

    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME,
        endpoint_url=AWS_S3_ENDPOINT_URL
    )

    try:
        # Get a pre-signed URL for the file stored in S3
        presigned_url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': AWS_STORAGE_BUCKET_NAME,
                'Key': "media/" + str(file_obj.file)
            },
            ExpiresIn=3600  # URL expiration time in seconds (adjust as needed)
        )

        response = FileResponse(requests.get(presigned_url), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{fileName}"'

        return response
    
    except ClientError as e:
        # Handle any exceptions or errors
        return HttpResponse(f'Error: {e}')


@login_required

def delete_file(request, file_id):

    file_obj = get_object_or_404(CMDoc, pk=file_id)

    if file_obj.user != request.user:
        raise PermissionDenied

    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME,
        endpoint_url=AWS_S3_ENDPOINT_URL
    )

    try:
        # Delete the file from the S3 bucket
        s3_client.delete_object(
            Bucket=AWS_STORAGE_BUCKET_NAME,
            Key="media/" + str(file_obj.file)
        )

    except ClientError as e:
        # Handle any exceptions or errors
        messages.ERROR(request, 'An error has occured. Please try again.')

        return redirect('view_all_files')

    file_obj.delete()

    return redirect('view_all_files')

