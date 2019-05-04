# Generated by Django 2.1.1 on 2019-01-31 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0006_auto_20181207_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donationitem',
            name='category',
            field=models.CharField(choices=[('', 'Selecione a categoria'), ('MATERIAIS_ESPORTIVOS', 'Materiais Esportivos'), ('LIVROS', 'Livros'), ('EQUIPAMENTOS_INFORMATICA', 'Equipamentos de Informática')], max_length=255, null=True, verbose_name='Categoria'),
        ),
        migrations.AlterField(
            model_name='donationitem',
            name='condition',
            field=models.CharField(blank=True, choices=[('', 'Selecione a condição do material'), ('REGULAR', 'Regular'), ('BOM', 'Bom'), ('MUITO_BOM', 'Muito Bom')], max_length=255, null=True, verbose_name='condição'),
        ),
        migrations.AlterField(
            model_name='donationitem',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='condição'),
        ),
        migrations.AlterField(
            model_name='donationitem',
            name='donation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='donation.Donation', verbose_name='Doador'),
        ),
        migrations.AlterField(
            model_name='donationitem',
            name='quantity',
            field=models.IntegerField(verbose_name='Quantidade'),
        ),
        migrations.AlterField(
            model_name='material',
            name='category',
            field=models.CharField(choices=[('', 'Selecione a categoria'), ('MATERIAIS_ESPORTIVOS', 'Materiais Esportivos'), ('LIVROS', 'Livros'), ('EQUIPAMENTOS_INFORMATICA', 'Equipamentos de Informática')], max_length=255, verbose_name='Categoria'),
        ),
    ]
