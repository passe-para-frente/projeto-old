# Generated by Django 2.1.1 on 2018-10-30 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20181014_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='social_id',
            field=models.TextField(null=True),
        ),
    ]
