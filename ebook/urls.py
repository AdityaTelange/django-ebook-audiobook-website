from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic.detail import DetailView

import ebook.models
import ebook.views

urlpatterns = [
                  path("ebook/<slug:slug>/",
                       DetailView.as_view(model=ebook.models.Ebook),
                       name="ebook", ),
                  path("<slug:tag>",
                       ebook.views.EbookListView.as_view(),
                       name="ebooks", ),
                  path("",
                       ebook.views.EbookListView.as_view(),
                       name="ebooks", ),
                  path("ebook_viewer/", ebook.views.EbookAllShowView.as_view(), name='all_ebook_viewer'),
                  path("ebook_viewer/<slug:slug>/", ebook.views.EbookShowView.as_view(), name='ebook_viewer'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
