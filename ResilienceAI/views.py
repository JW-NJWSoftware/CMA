from django.shortcuts import render, redirect
from django.contrib import messages
from crisisManagementAssistant.models import CMDoc, Chat
from authentication.models import CustomUser
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "home.html")

@login_required
def search(request):
    search_value = request.GET.get('search_value') or None
    files = []
    chats = []
    file_names_list = []
    search = False

    if search_value:
        search = True
        if request.user.group:
            users = CustomUser.objects.filter(group=request.user.group)
            for user in users:
                user_files = CMDoc.objects.filter(user=user, fileName__icontains=search_value)
                files.extend(user_files)
                user_chats = Chat.objects.filter(user=user, chatName__icontains=search_value)
                chats.extend(user_chats)
        else:
            files = CMDoc.objects.filter(user=request.user, fileName__icontains=search_value)
            chats = Chat.objects.filter(user=request.user, chatName__icontains=search_value)

        file_names_list = [CMDoc.file.name.split('/')[-1] for CMDoc in files]
    
    else:
        messages.error(request, 'No search value provided.')

    return render(request, "search.html", {'files': files, 'chats': chats, 'names': file_names_list, 'search': search})

@login_required
def guides(request):
    return render(request, "guides.html")

def handler400(request, exception):
    context = {"errorCode":"400", "errorType":"Bad Request", "description":"This error indicates that the server cannot process the request due to a malformed or incorrect syntax. The request you made contains incorrect or incomplete information that the server cannot understand. Please ensure the request parameters or data are properly formatted and try again. If you believe this is a mistake, review the request details or contact support for further assistance."}
    return render(request, 'errorPage.html', context, status=400)

def handler401(request, exception):
    context = {"errorCode":"401", "errorType":"Unauthorized", "description":"This error indicates that the provided authentication credentials are invalid or missing. Access to this page requires valid authentication. Please check your credentials and try again. If you believe this is a mistake, please ensure you have the correct authentication details."}
    return render(request, 'errorPage.html', context, status=401)

def handler403(request, exception):
    context = {"errorCode":"403", "errorType":"Forbidden", "description":"This error indicates that although your authentication credentials are valid, access to this specific resource is denied due to insufficient permissions. The server refuses to authorize your request to access this page. If you believe this is a mistake or require additional permissions, please try again, contact the administrator or try another resource."}
    return render(request, 'errorPage.html', context, status=403)

def handler404(request, exception):
    context = {"errorCode":"404", "errorType":"Not Found", "description":"This error indicates that the requested page or resource does not exist on the server. The server couldn't find the specific page you're looking for. Please verify the URL or check if the resource has been moved or deleted. If you believe this is a mistake, please verify the URL or navigate to another page."}
    return render(request, 'errorPage.html', context, status=404)

def handler500(request):
    context = {"errorCode":"500", "errorType":"Internal Server Error", "description":"This error indicates that there is an unexpected issue on the server while processing your request. The server encountered an error it cannot handle. This could be due to an internal configuration problem or a temporary overload. Please try again later. If the problem persists, contact the website administrator for assistance."}
    return render(request, 'errorPage.html', context, status=500)
