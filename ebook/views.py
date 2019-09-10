from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic.base import *
from django.views.generic.list import ListView

from ebook import models

logger = logging.getLogger(__name__)
EBOOK_FILE_TYPES = ['pdf']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


class EbookListView(ListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag = None

    template_name = "ebook/ebook_list.html"
    paginate_by = 4

    def get_queryset(self):
        try:
            tag = self.kwargs["tag"]
            if tag != "all":
                self.tag = get_object_or_404(models.EbookTag, slug=tag)
            if self.tag:
                ebooks = models.Ebook.objects.active().filter(tags=self.tag)
            else:
                ebooks = models.Ebook.objects.active()
        except KeyError:
            ebooks = models.Ebook.objects.active()
        return ebooks.order_by("name")


class EbookAllShowView(LoginRequiredMixin, ListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag = None

    template_name = "ebook/ebook_viewer_list.html"
    paginate_by = 4

    def get_queryset(self):
        try:
            tag = self.kwargs["tag"]
            if tag != "all":
                self.tag = get_object_or_404(models.EbookTag, slug=tag)
            if self.tag:
                ebooks = models.Ebook.objects.active().filter(tags=self.tag)
            else:
                ebooks = models.Ebook.objects.active()
        except KeyError:
            ebooks = models.Ebook.objects.active()
        return ebooks.order_by("name")


class EbookShowView(LoginRequiredMixin, TemplateView):
    template_name = 'ebook/ebook_viewer.html'

    def get_context_data(self, **kwargs):
        slug = self.kwargs["slug"]

        ebook = models.Ebook.objects.all().filter(slug=slug).first()
        context = {'ebook': ebook}
        return context
