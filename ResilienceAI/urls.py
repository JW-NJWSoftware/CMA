"""
URL configuration for ResilienceAI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from ResilienceAI.views import home, guides

from ResilienceAI.views import handler400, handler401, handler403, handler404, handler500

handler400 = 'ResilienceAI.views.handler400'
handler401 = 'ResilienceAI.views.handler401'
handler403 = 'ResilienceAI.views.handler403'
handler404 = 'ResilienceAI.views.handler404'
handler500 = 'ResilienceAI.views.handler500'

urlpatterns = [
    path('', home),
    path('guides/', guides),
    path('admin/', admin.site.urls),
    path('auth/', include("authentication.urls")),
    path('CMA/', include("crisisManagementAssistant.urls")),
    path('cma/', include("crisisManagementAssistant.urls")),
]
