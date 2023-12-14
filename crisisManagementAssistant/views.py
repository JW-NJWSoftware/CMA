from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404

from crisisManagementAssistant.models import CMDoc, Chat
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
    owner = False
    
    if group:
        users = CustomUser.objects.filter(group=group)

        if request.user.role == 'Owner':
            owner = True

    return render(request, 'cma/manage.html', {'group': users, 'owner': owner})

@login_required
def add_to_group(request):
    userEmail = request.GET.get('user_email') or None

    if userEmail:
        user = get_object_or_404(CustomUser, email=userEmail)
        
        if user.group is None:
            user.group = request.user.group
            user.save()
            user.role = 'Member'
            user.save()
            messages.success(request, 'User added to group')

        else:
            messages.error(request, 'User is already in a group')
    else:
        messages.error(request, 'User not found')

    return redirect('manage')

@login_required
def remove_from_group(request):
    userEmail = request.GET.get('user_email') or None
    print(userEmail)
    if userEmail:
        user = get_object_or_404(CustomUser, email=userEmail)
  
        if user.group == request.user.group:
        
            if request.user.role == 'Owner':

                user.group = None
                user.save()

                user.role = None
                user.save()
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied

    return redirect('manage')

@login_required
def new_group(request):
    group_name = request.GET.get('group_name') or None

    if group_name:
        user = request.user
        
        if user.group is None:
            existingGroup = CustomUser.objects.filter(group=group_name)
            #print(existingGroup)
            if not existingGroup:
                user.group = group_name
                user.save()

                user.role = 'Owner'
                user.save()
            else:
                messages.error(request, 'Group already exists')
        else:
            messages.error(request, 'User already in group')
    else:
        messages.error(request, 'Please enter a group name')

    return redirect('manage')

@login_required
def view_all_files(request):
    files = []

    if request.user.group:
        users = CustomUser.objects.filter(group=request.user.group)
        for user in users:
            user_files = CMDoc.objects.filter(user=user)
            files.extend(user_files)
    else:
        files = CMDoc.objects.filter(user=request.user)

    file_names_list = [CMDoc.file.name.split('/')[-1] for CMDoc in files]

    return render(request, 'cma/files.html', {'files': files, 'names': file_names_list})

@login_required
def upload_file(request):

    if request.method == 'POST':
        local = request.POST.get('switch_value') == 'on'
        form = CMDocForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            obj = form.save(commit = False)
            obj.user=request.user   
            obj.save()
            
            extracted = extract_info_via_api(obj.file, local)
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

        if file_obj.user != request.user and file_obj.user.group != request.user.group:
            raise PermissionDenied

        data = file_obj.extractData
        summary = data.get('summary')
        names = data.get('names')

        if names:
            names_list = names.split(', ')
        else:
            names_list = None

    return render(request, 'cma/view_CMDoc.html', {'CMDoc': file_obj, 'summary': str(summary), 'names_list': names_list})


@login_required

def download_file(request, file_id):

    file_obj = get_object_or_404(CMDoc, pk=file_id)

    if file_obj.user != request.user and file_obj.user.group != request.user.group:
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
        messages.error(request, 'An error has occured. Please try again.')

        return redirect('view_all_files')

    file_obj.delete()

    return redirect('view_all_files')


@login_required
def view_all_chats(request):
    chats = []

    if request.user.group:
        users = CustomUser.objects.filter(group=request.user.group)
        for user in users:
            user_chats = Chat.objects.filter(user=user)
            chats.extend(user_chats)
    else:
        chats = Chat.objects.filter(user=request.user)

    return render(request, 'cma/chats.html', {'chats': chats})

@login_required
def view_chat(request, slug=None):
    chat_obj = None
    if slug is not None:
        chat_obj = get_object_or_404(Chat, slug=slug)

        if chat_obj.user != request.user and chat_obj.user.group != request.user.group:
            raise PermissionDenied

        data = chat_obj.chatData

    return render(request, 'cma/view_chat.html', {'chat': chat_obj})

@login_required
def delete_chat(request, slug=None):

    chat_obj = get_object_or_404(Chat, slug=slug)

    if chat_obj.user != request.user:
        raise PermissionDenied

    chat_obj.delete()

    return redirect('view_all_chats')

@login_required
def new_chat(request):
    chat_name = request.GET.get('chat_name') or None

    if chat_name:
        new_chat = Chat.objects.create(
            user=request.user,
            chatName=chat_name
        )
    
        new_chat.save()

        return redirect('view_chat', slug=new_chat.slug)

    else:
        messages.ERROR(request, 'No chat name provided')
        return redirect('view_all_chats')
