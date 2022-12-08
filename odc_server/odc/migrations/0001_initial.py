# Generated by Django 4.1.2 on 2022-12-06 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConsolePicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bytes', models.TextField()),
                ('filename', models.CharField(max_length=255)),
                ('mimetype', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=255)),
                ('in_sync', models.BooleanField(default=False, max_length=20)),
                ('enc_scheme', models.CharField(default='AES', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('filepath', models.CharField(blank=True, max_length=255)),
                ('document', models.FileField(blank=True, null=True, upload_to='odc.ConsolePicture/bytes/filename/mimetype')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(blank=True, max_length=255)),
                ('md5sum', models.CharField(blank=True, editable=False, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='runtimeDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=255)),
                ('ownedContainers', models.CharField(blank=True, max_length=65535)),
                ('totalOwnedContainers', models.IntegerField(default=0)),
            ],
        ),
    ]
