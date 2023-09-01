"""ruleta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from sorteo.views import ruleta , registro, consultar_ganador,exportar_sorteos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ruleta/<int:pk>', ruleta, name='ruleta'),
    path('', registro, name='registro'),
    path('consultar_ganador/', consultar_ganador, name='consultar_ganador'),
    path('exportar_sorteos/', exportar_sorteos , name='exportar_sorteos')
]
