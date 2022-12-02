

# Create your models here.
from __future__ import unicode_literals
from django.db import models
from db_file_storage.model_utils import delete_file_if_needed
from db_file_storage.model_utils import delete_file


class Document(models.Model):
    name = models.CharField(max_length=255, blank=True)
    filepath = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='odc.ConsolePicture/bytes/filename/mimetype', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=255, blank=True)
    md5sum = models.CharField(max_length=255, blank=True, editable=False)

    def save(self, *args, **kwargs):
        delete_file_if_needed(self, 'picture')
        super(Document, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(Document, self).delete(*args, **kwargs)
        delete_file_if_needed(self, 'document')


class ConsolePicture(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)


class Details(models.Model):
    username = models.CharField(max_length=255, blank=True)
    in_sync = models.BooleanField(max_length=20, default=False)
    enc_scheme = models.CharField(max_length=255, default='AES')


class runtimeDetails(models.Model):
    username = models.CharField(max_length=255, blank=True)
    #the name is like <username>_<port_number_assigned> sending this info to client so that user can point specific container allocated
    ownedContainers = models.CharField(max_length=65535, blank=True)
    totalOwnedContainers = models.IntegerField(blank=False,default=0)
