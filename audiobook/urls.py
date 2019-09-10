from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import DetailView

import audiobook.models
from . import views

urlpatterns = [
                  path("",
                       views.AudioBookListView.as_view(),
                       name="audiobooks", ),
                  path("<slug:tag>",
                       views.AudioBookListView.as_view(),
                       name="audiobooks", ),
                  path("audiobook/<slug:slug>/",
                       DetailView.as_view(model=audiobook.models.Audiobook),
                       name="audiobook", ),
                  path("audiobook_viewer/", audiobook.views.AudiobookAllShowView.as_view(),
                       name='all_audiobook_viewer'),
                  path("audiobook_viewer/<slug:slug>/", audiobook.views.AudiobookShowView.as_view(), name='audiobook_viewer'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
