import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ActiveManager(models.Manager):
    def active(self):
        return self.filter(active=True)


class AudioBookTagManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class AudiobookTag(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=48)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    objects = AudioBookTagManager()

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.slug,)


def ext_validators(value):
    ext = '%s' % os.path.splitext(value.name)[-1]
    if ext.lower() not in settings.AUDIO_EXTENTIONS:
        message = _('Invalid format, please choose: %(ext)s') % {'ext': settings.AUDIO_EXTENTIONS}
        raise ValidationError(message)


class Audiobook(models.Model):
    name = models.CharField(max_length=500)
    written_by = models.CharField(max_length=250)
    narrated_by = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    slug = models.SlugField(max_length=48)
    tags = models.ManyToManyField(AudiobookTag, blank=True)
    active = models.BooleanField(default=True)
    date_updated = models.DateTimeField(auto_now=True)
    album_logo = models.FileField()
    # book_part = models.ForeignKey(AudioPart, on_delete=models.CASCADE, related_name='book_part')
    objects = ActiveManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']


class AudioPart(models.Model):
    # contains audio in a audiobook mostly chapters
    audio_book = models.ForeignKey(Audiobook, on_delete=models.CASCADE, related_name='book_part')
    audio_name = models.CharField(max_length=250)
    audio_file = models.FileField(default='', validators=[ext_validators])

    def __str__(self):
        return self.audio_name


class AudiobookImage(models.Model):
    product = models.ForeignKey(Audiobook, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product-images")

    thumbnail = models.ImageField(upload_to="product-thumbnails", null=True)
