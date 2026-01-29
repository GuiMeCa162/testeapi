from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("tipo", "admin")

        return self.create_user(username, password, **extra_fields)

class Usuario(AbstractUser):
    USUARIO_CHOICES = [('admin', 'Admin'), ('staff', 'Staff')]
    tipo = models.CharField(max_length=5, choices=USUARIO_CHOICES, default='staff')

    objects = UsuarioManager()

    def __str__(self):
        return self.username