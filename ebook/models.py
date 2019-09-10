from __future__ import unicode_literals

import logging

from django.db import models
from welut.models import EbookConverter

logger = logging.getLogger(__name__)


class ActiveManager(models.Manager):
    def active(self):
        return self.filter(active=True)


class EbookTagManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class EbookTag(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=48)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    objects = EbookTagManager()

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.slug,)


class Ebook(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    slug = models.SlugField(max_length=48)
    tags = models.ManyToManyField(EbookTag, blank=True)
    active = models.BooleanField(default=True)
    date_updated = models.DateTimeField(auto_now=True)
    ebook_file = models.ForeignKey(EbookConverter, related_name='ebook_file', on_delete=models.CASCADE, )

    objects = ActiveManager()

    def __str__(self):
        return self.name

    def get_files(self):
        """ return list images of ebook per-page """
        return self.ebook_file.get_files()

    class Meta:
        ordering = ['-name']


class EbookImage(models.Model):
    product = models.ForeignKey(Ebook, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product-images")

    thumbnail = models.ImageField(upload_to="product-thumbnails", null=True)
