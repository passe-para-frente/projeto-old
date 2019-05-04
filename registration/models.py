from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from .helpers import UserValidator


class UserTypes():
    ADMIN = 'ADMIN'
    PERSON = 'PERSON'
    COMPANY = 'COMPANY'
    SCHOOL = 'SCHOOL'

    types = (
        (PERSON, 'Doador - Pessoa Física'),
        (COMPANY, 'Doador - Pessoa Jurídica'),
        (SCHOOL, 'Escola'),
        (ADMIN, 'Admin')
    )

class UserManager(DefaultUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None

    name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=10, choices=UserTypes.types)
    registration_number = models.CharField(max_length=18, null=True, unique=True)
    company_name = models.CharField(max_length=20, null=True)
    state_registration = models.CharField(max_length=20, null=True)
    phone_number = models.CharField(max_length=14, null=True)
    cell_phone_number = models.CharField(max_length=15, null=True)
    social_id = models.TextField(null=True)
    objects = UserManager()

    def __str__(self):
        return f'{self.name}'

    @property
    def is_social_account(self):
        return self.social_id is not None

    @property
    def registration_completed(self):
        is_company = self.type == UserTypes.COMPANY or UserTypes.SCHOOL
        errors = UserValidator.validate(self, validate_company=is_company)

        return len(errors) == 0

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['type']

class Address(models.Model):
    class Meta:
        verbose_name='Endereço'
        verbose_name_plural='Endereços'

    street = models.CharField(max_length=255)
    number = models.CharField(max_length=10)
    complement = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=9)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.number} {self.street}, {self.district}, {self.city} - {self.state}'
