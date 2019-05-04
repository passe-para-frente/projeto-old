from django.db import models

class Contact(models.Model):
    class Meta:
        verbose_name='Contato'
        verbose_name_plural='Contatos'

    email = models.EmailField(max_length=255, verbose_name='e-mail')
    name = models.CharField(max_length=50, verbose_name='nome')
    message = models.TextField(verbose_name='mensagem')

    def __str__(self):
        return f'{self.name}'