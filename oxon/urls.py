"""oxon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/', include('product.urls', namespace='product')),
    path('', views.home, name='home'),
    path('account/', include('account.urls', namespace='account')),
    path('404/', views.error, name='error'),
    path('reset_password/', auth_view.PasswordResetView.as_view(
        template_name='password_reset_form/passwordresetview.html'
    ), name='reset_password'),
    path('reset/<uidb64>/<token>', auth_view.PasswordResetConfirmView.as_view(
        template_name='password_reset_form/PasswordResetConfirmView.html'
    ), name="password_reset_confirm"),
    path('reset_sent/', auth_view.PasswordResetDoneView.as_view(
        template_name= 'password_reset_form/PasswordResetDoneView.html'
    ), name='password_reset_done'),
    path('reset_complete/', auth_view.PasswordResetCompleteView.as_view(
        template_name='password_reset_form/PasswordResetCompleteView.html'
    ), name='password_reset_complete'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)