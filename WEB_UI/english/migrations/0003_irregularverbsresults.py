# Generated by Django 2.1.5 on 2019-10-18 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0002_auto_20190927_0850'),
    ]

    operations = [
        migrations.CreateModel(
            name='IrregularVerbsResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('verb_id', models.IntegerField()),
                ('user_answer', models.CharField(max_length=255)),
            ],
        ),
    ]
