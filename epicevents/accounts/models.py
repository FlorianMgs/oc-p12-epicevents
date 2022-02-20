from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from datetime import datetime


class UserManager(BaseUserManager):
    """Define a model manager for User model without username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):

    SALES = 'sales_member'
    MANAGEMENT = 'management_member'
    SUPPORT = 'support_member'
    ROLE_CHOICES = (
        (SALES, 'sales_member'),
        (MANAGEMENT, 'management_member'),
        (SUPPORT, 'support_member')
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    objects = UserManager()

    def __str__(self):
        return f'{self.email}'


class Client(models.Model):

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    company_name = models.CharField(max_length=250)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    sales_contact = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='sales_contact')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def update_date(self):
        self.date_updated = datetime.now()

    def save(self, *args, **kwargs):
        self.update_date()
        return super(Client, self).save()
