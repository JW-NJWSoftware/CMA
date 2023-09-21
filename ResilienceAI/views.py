from django.http import HttpResponse
from django.template.loader import render_to_string

def home(request):
  


    HTML_string = render_to_string("home.html")

    return HttpResponse(HTML_string)
