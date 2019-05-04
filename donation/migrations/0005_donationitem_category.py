# Generated by Django 2.1.1 on 2018-11-22 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0004_auto_20181031_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationitem',
            name='category',
            field=models.CharField(choices=[('', 'selecionar a categoria'), ('SPORTING_GOODS', 'Materiais Esportivos'), ('BOOKS', 'Livros'), ('COMPUTER_EQUIPMENT', 'Equipamentos de informática')], max_length=255, null=True, verbose_name='Categoria'),
        ),
    ]