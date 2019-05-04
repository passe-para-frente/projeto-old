from django.db import models
from django.contrib import admin
from django.core.exceptions import ValidationError
from registration.models import User, UserTypes

class MaterialCondition():
    EMPTY = ''
    AVERAGE = 'REGULAR'
    GOOD = 'BOM'
    VERY_GOOD = 'MUITO_BOM'

    CHOICES = (
        (EMPTY, 'Selecione a condição do material'),
        (AVERAGE, 'Regular'),
        (GOOD, 'Bom'),
        (VERY_GOOD, 'Muito Bom'),
    )

class Category():
    NONE = ''
    SPORTING_GOODS = 'MATERIAIS_ESPORTIVOS'
    BOOKS = 'LIVROS'
    COMPUTER_EQUIPMENT = 'EQUIPAMENTOS_INFORMATICA'

    CHOICES = (
        (NONE, 'Selecione a categoria'),
        (SPORTING_GOODS, 'Materiais Esportivos'),
        (BOOKS, 'Livros'),
        (COMPUTER_EQUIPMENT, 'Equipamentos de Informática')
    )

    '''
    Essas categorias não possuem materiais vinculados
    '''
    EMPTY_CATEGORIES = (BOOKS)

    @classmethod
    def is_empty(cls, category):
        return category in cls.EMPTY_CATEGORIES

    @classmethod
    def get_verbose_name(cls, category):
        for item in cls.CHOICES:
            if item[0] == category:
                return item[1]

        return None

class Delivery():
    NONE = ''
    DONOR = 'DONOR'
    SCHOOL = 'SCHOOL'

    CHOICES = (
        (NONE, 'Forma de entrega'),
        (DONOR, 'Levar pessoalmente'),
        (SCHOOL, 'Quero que retirem'),
    )

class Sport(models.Model):
    class Meta:
        verbose_name = 'Esporte'
        verbose_name_plural = 'Esportes'

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Material(models.Model):
    class Meta:
        verbose_name_plural = 'Materiais'

    name = models.CharField(verbose_name='Nome', max_length=255)
    category = models.CharField(verbose_name='Categoria', max_length=255, choices=Category.CHOICES)
    sport = models.ForeignKey(Sport, on_delete=None, related_name="sport", null=True, blank=True, verbose_name="Esporte")

    def __str__(self):
        return self.name

class Donation(models.Model):
    class Meta:
        verbose_name = 'Doação'
        verbose_name_plural = 'Doações'

    created_at = models.DateTimeField(verbose_name='Data de criação', auto_now_add=True)
    confirmed = models.BooleanField(verbose_name='Confirmado', default=False)
    delivery = models.CharField(verbose_name='Forma de entrega', max_length=255, choices=Delivery.CHOICES)

    donor = models.ForeignKey(User, verbose_name='Doador', related_name='donor', on_delete=models.PROTECT)
    school = models.ForeignKey(User, verbose_name='Escola', related_name='school', on_delete=models.PROTECT, null=True)

    def __str__(self):
        school_name = self.school.name if self.school else '(em aberto)'
        return f'#{self.id} {self.donor.name} -> {school_name}'

    @property
    def items(self):
        return self.donationitem_set.all()

    @property
    def item_quantity(self):
        response = self.donationitem_set.aggregate(models.Sum('quantity'))
        return response['quantity__sum']

    def clean(self):
        if self.donor.type not in (UserTypes.PERSON, UserTypes.COMPANY):
            raise ValidationError('Doador deve ser uma pessoa física ou jurídica')

        if self.school and self.school.type != UserTypes.SCHOOL:
            raise ValidationError('Recebedor deve ser uma escola')

class DonationItem(models.Model):
    class Meta:
        verbose_name = 'Item para Doação'
        verbose_name_plural = 'Itens para Doação'

    condition = models.CharField(max_length=255, verbose_name='condição', choices=MaterialCondition.CHOICES, null=True, blank=True)
    quantity = models.IntegerField(verbose_name='Quantidade')
    description = models.TextField(null=True, blank=True, verbose_name='Descrição')

    donation = models.ForeignKey(Donation, on_delete=models.PROTECT, verbose_name='Doador')
    sport = models.ForeignKey(Sport, verbose_name='Esporte', on_delete=models.PROTECT, null=True, blank=True)
    material = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True)
    category = models.CharField(verbose_name='Categoria', max_length=255, choices=Category.CHOICES, null=True)

    def __str__(self):
        if not self.material:
            return Category.get_verbose_name(self.category)

        if self.sport:
            return self.material.name + ' de ' + self.sport.name

        return self.material.name
