

# Create your fields here.
from __future__ import unicode_literals
from db_file_storage.model_utils import delete_file_if_needed
from db_file_storage.model_utils import delete_file
from mongoengine import Document, fields 

class document(Document):
    name = fields.StringField(max_length=255)
    filepath = fields.StringField(max_length=255)
    document = fields.FileField(upload_to='odc.ConsolePicture/bytes/filename/mimetype', , null=True)
    uploaded_at = fields.DateTimeField(auto_now_add=True)
    username = fields.StringField(max_length=255)
    md5sum = fields.StringField(max_length=255,editable=False)

    def save(self, *args, **kwargs):
        delete_file_if_needed(self, 'picture')
        super(Document, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(Document, self).delete(*args, **kwargs)
        delete_file_if_needed(self, 'document')


class ConsolePicture(Document):
    bytes = fields.StringField()
    filename = fields.StringField(max_length=255)
    mimetype = fields.StringField(max_length=50)


class Details(Document):
    username = fields.StringField(max_length=255)
    in_sync = fields.BooleanField(max_length=20, default=False)
    enc_scheme = fields.StringField(max_length=255, default='AES')


class runtimeDetails(Document):
    username = fields.StringField(max_length=255)
    #the name is like <username>_<port_number_assigned> sending this info to client so that user can point specific container allocated
    ownedContainers = fields.DictField()
    totalOwnedContainers = fields.IntField(required=False,default=0)

class wargame_details(Document):
    username = fields.StringField(max_length=255)
    owned_wargame_runtime_port = fields.StringField(max_length=10)
