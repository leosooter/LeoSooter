from __future__ import unicode_literals
from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.ForeignKey('Description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Description(models.Model):
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
j
