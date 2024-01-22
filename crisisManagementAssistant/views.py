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
from ResilienceAI.services import extract_info_via_api, ask_chat_via_api

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

    return render(request, 'cma/manage.html', {'group': users, 'owner': owner, 'mainUser':request.user})

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
def leave_group(request):
    user = request.user

    if user.group:
        if user.role != 'Owner':
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
def delete_group(request):
    user = request.user
  
    if user.group:
        if request.user.role == 'Owner':
            groupUsers = CustomUser.objects.filter(group=user.group)

            for groupUser in groupUsers:
                groupUser.group = None
                groupUser.save()

                groupUser.role = None
                groupUser.save()

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

            user_settings = request.user.settings
            chunk_size = user_settings.get('chunk_size', 1000) if user_settings else 1000
            sentence_cut_percentage = user_settings.get('sentence_cut_percentage', 25.0) if user_settings else 25.0
            
            extracted = extract_info_via_api(obj.file, local, chunk_size, sentence_cut_percentage)
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

        file_extension = file_obj.file.name.split('.')[-1].lower()

        # Check if the file type is one that can be shown in an HTML iframe
        allowed_view_file_types = ['pdf', 'html', 'txt', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'mp4'] #allowed file types
        allowed_extracted_file_types = ['pdf', 'txt', 'doc', 'docx'] #allowed file types

        allow_view = file_extension in allowed_view_file_types
        allow_extracted_data = file_extension in allowed_extracted_file_types

    return render(request, 'cma/view_CMDoc.html', {'CMDoc': file_obj, 'summary': str(summary), 'names_list': names_list, 'allow_view': allow_view, 'allow_extracted_data': allow_extracted_data})


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
    all_file_data = None
    chat_obj = None
    chat_history = None
    file_ids = None
    allowed_file_extensions = ['pdf', 'txt', 'doc', 'docx']
    all_files = []

    if slug is not None:
        chat_obj = get_object_or_404(Chat, slug=slug)

        if chat_obj.user != request.user and chat_obj.user.group != request.user.group:
            raise PermissionDenied

        if request.user.group:
            users = CustomUser.objects.filter(group=request.user.group)
            for user in users:
                user_files = CMDoc.objects.filter(user=user)
                for file_obj in user_files:
                    if any(file_obj.file.name.split('.')[-1].lower() for ext in allowed_file_extensions):
                        all_files.append(file_obj)
        else:
            user_files = CMDoc.objects.filter(user=request.user)
            for file_obj in user_files:
                if any(file_obj.file.name.lower().endswith(ext) for ext in allowed_file_extensions):
                    all_files.append(file_obj)

        all_file_data = [{'id': file_obj.id, 'name': file_obj.fileName} for file_obj in all_files]
            
        if request.method == 'POST':
            question = request.POST.get('question_value') or None
            if question is not None:
                local = request.POST.get('switch_value') == 'on'
                user_settings = request.user.settings
                modelChoice = user_settings.get('modelChoice', "roberta-base-squad2") if user_settings else "roberta-base-squad2"
                result = ask_chat_via_api(question, chat_obj.chatData, local, modelChoice)
                answer = str(result.get('answer')).replace('\n', '')
                answerContext = str(result.get('answerContext'))
                question_answer_pair = f"Question: {question}\n Answer: {answer}\n Context: {answerContext}\n"
            
                history = ''.join([str(chat_obj.chatData.get('history')), question_answer_pair])

                file_ids = chat_obj.chatData.get('file_ids')

                data = {
                    "history": history,
                    "context": chat_obj.chatData.get('context'),
                    "file_ids": file_ids,
                }

                chat_obj.chatData = data
                chat_obj.save()
            else:
                history = chat_obj.chatData.get('history')
                file_ids = chat_obj.chatData.get('file_ids')
        else:
            history = chat_obj.chatData.get('history')
            file_ids = chat_obj.chatData.get('file_ids')
        
        if history:
            chat_history = history.split("\n")

    return render(request, 'cma/view_chat.html', {'chat': chat_obj, 'chat_history': chat_history, 'file_ids': file_ids, 'all_file_data': all_file_data})

@login_required
def delete_chat(request, slug=None):

    chat_obj = get_object_or_404(Chat, slug=slug)

    if chat_obj.user != request.user:
        raise PermissionDenied

    chat_obj.delete()

    return redirect('view_all_chats')

@login_required
def regen_context_chat(request, slug=None):

    chat_obj = get_object_or_404(Chat, slug=slug)

    if chat_obj.user != request.user:
        raise PermissionDenied
        
    if request.method == 'POST':
        selected_files_ids = request.POST.getlist('selected_files')
        selected_files = CMDoc.objects.filter(id__in=selected_files_ids)
        
        file_ids = []
        context = ""
        
        for file_obj in selected_files:
            data = file_obj.extractData
            text = data.get('text')
            if text:
                context += f"{text} "
                file_ids.append(file_obj.id)

        chatData = {
            "history": chat_obj.chatData.get('history'),
            "context": context.strip(),
            "file_ids": file_ids,
        }

        chat_obj.chatData = chatData
        chat_obj.save()

    return redirect('view_chat', slug=slug)

@login_required
def new_chat(request):
    chat_name = request.GET.get('chat_name') or None

    if chat_name:
        new_chat = Chat.objects.create(
            user=request.user,
            chatName=chat_name
        )
    
        new_chat.save()

        files = []
        file_ids = []
        context = None

        if request.user.group:
            users = CustomUser.objects.filter(group=request.user.group)
            for user in users:
                user_files = CMDoc.objects.filter(user=user)
                files.extend(user_files)
        else:
            files = CMDoc.objects.filter(user=request.user)

        for file_obj in files:
            data = file_obj.extractData
            text = data.get('text')
            if text:
                if context is None:
                    context = text
                else:
                    context += " " + text
                file_ids.append(file_obj.id)
        
        chatData = {
            "history": "",
            "context": context,
            "file_ids": file_ids,
        }

        new_chat.chatData = chatData
        new_chat.save()

        return redirect('view_chat', slug=new_chat.slug)

    else:
        messages.ERROR(request, 'No chat name provided')
        return redirect('view_all_chats')