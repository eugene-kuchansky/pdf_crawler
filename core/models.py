# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class PDFFile(models.Model):
    name = models.CharField(max_length=300)
    
    def __str__(self):
        return 'id: {}, name: {}'.format(self.id, self.name)


class Link(models.Model):
    url = models.CharField(max_length=200, unique=True)
    pdf_file = models.ManyToManyField(PDFFile)
    is_alive = models.BooleanField(default=True)
    
    def __str__(self):
        return 'id: {}, url: {}'.format(self.id, self.url)
