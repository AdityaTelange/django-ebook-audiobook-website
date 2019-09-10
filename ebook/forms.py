# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from welut.models import EbookConverter

from .models import Ebook


class EbookConverterForm(forms.ModelForm):
    class Meta:
        model = EbookConverter
        fields = ['path', ]

    def __init__(self, *args, **kwargs):
        super(EbookConverterForm, self).__init__(*args, **kwargs)
        self.fields['path'].widget.attrs = {'class': 'form-control'}


class EBookForm(forms.ModelForm):
    class Meta:
        model = Ebook
        fields = ['name', ]

    def __init__(self, *args, **kwargs):
        super(EBookForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'class': 'form-control'}
