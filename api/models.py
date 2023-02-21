from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.core.validators import MaxValueValidator, DecimalValidator

class Gym(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Member(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    USERNAME_FIELD = 'username'
    age = models.PositiveIntegerField(blank=True, null=True)
    height = models.DecimalField(max_digits=6, decimal_places=2, default='0.00', validators=[MaxValueValidator(999.99), DecimalValidator(max_digits=5, decimal_places=2)])
    weight = models.DecimalField(max_digits=5, decimal_places=2, default='0.00', validators=[MaxValueValidator(999.99), DecimalValidator(max_digits=5, decimal_places=2)])
    target = models.DecimalField(max_digits=5, decimal_places=2, default='0.00', validators=[MaxValueValidator(999.99), DecimalValidator(max_digits=5, decimal_places=2)])
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, blank=False, null=False)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gym = models.ForeignKey(Gym, on_delete=models.SET('Unknown'))
    membership_start_date = models.DateField()
    membership_end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    def save(self, *args, **kwargs):
        # Hash the password before saving the user object
        self.password = make_password(self.password)
        super(Member, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def TokenCreate(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)