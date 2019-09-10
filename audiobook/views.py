from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from . import models


class AudioBookListView(ListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag = None

    template_name = "audiobook/audiobook_list.html"
    paginate_by = 4

    def get_queryset(self):
        try:
            tag = self.kwargs["tag"]
            if tag != "all":
                self.tag = get_object_or_404(models.AudiobookTag, slug=tag)
            if self.tag:
                audiobooks = models.Audiobook.objects.active().filter(tags=self.tag)
            else:
                audiobooks = models.Audiobook.objects.active()
        except KeyError:
            audiobooks = models.Audiobook.objects.active()
        return audiobooks.order_by("name")


class AudiobookAllShowView(LoginRequiredMixin, ListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag = None

    template_name = "audiobook/audiobook_viewer_list.html"
    paginate_by = 4

    def get_queryset(self):
        try:
            tag = self.kwargs["tag"]
            if tag != "all":
                self.tag = get_object_or_404(models.AudiobookTag, slug=tag)
            if self.tag:
                ebooks = models.Audiobook.objects.active().filter(tags=self.tag)
            else:
                ebooks = models.Audiobook.objects.active()
        except KeyError:
            ebooks = models.Audiobook.objects.active()
        return ebooks.order_by("name")


class AudiobookShowView(LoginRequiredMixin, TemplateView):
    template_name = 'audiobook/audiobook_viewer.html'

    def get_context_data(self, **kwargs):
        slug = self.kwargs["slug"]

        audiobook = models.Audiobook.objects.get(slug=slug)
        print(audiobook.book_part.all())
        return {'audiobook': audiobook}
