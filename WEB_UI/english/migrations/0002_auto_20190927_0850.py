# Generated by Django 2.1.5 on 2019-09-27 05:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EnglishIrregularVerbs',
            new_name='IrregularVerbs',
        ),
    ]