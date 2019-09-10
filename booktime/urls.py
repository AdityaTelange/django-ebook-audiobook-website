"""booktime URL Configuration"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('ebooks/', include('ebook.urls'), name='ebook_root'),
    path('audiobooks/', include('audiobook.urls'), name='audiobook_root'),
]
