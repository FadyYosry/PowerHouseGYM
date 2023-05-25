from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.core.validators import MaxValueValidator, DecimalValidator
from django.core.exceptions import ObjectDoesNotExist

class Admin(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, blank=False, null=False)

    def __str__(self):
        return f"{self.username}"
    
    def connected_gym(self):
        try:
            return self.gym.name
        except Gym.DoesNotExist:
            return None

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

class AdminGym(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)

class Member(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    USERNAME_FIELD = 'username'
    age = models.PositiveIntegerField(blank=True, null=True)
    height = models.DecimalField(max_digits=6, decimal_places=2, default='0.00', validators=[MaxValueValidator(999.99), DecimalValidator(max_digits=5, decimal_places=2)])
    weight = models.DecimalField(max_digits=5, decimal_places=2, default='0.00', validators=[MaxValueValidator(999.99), DecimalValidator(max_digits=5, decimal_places=2)])
    target = models.DecimalField(max_digits=5, decimal_places=2, default='0.00', validators=[MaxValueValidator(999.99), DecimalValidator(max_digits=5, decimal_places=2)])
    gender = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, blank=False, null=False)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gym_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    def save(self, *args, **kwargs):
        # Hash the password before saving the user object
        self.password = make_password(self.password)
        try:
            # Search for the gym in the Gym table
            gym = Gym.objects.get(name=self.gym_name)
        except ObjectDoesNotExist:
            # If the gym doesn't exist, create a new gym entry
            gym = Gym(name=self.gym_name)
            gym.save()
        # Set the gym foreign key to the found or created gym
        self.gym = gym
        # Call the parent class's save method
        super(Member, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class AdminMember(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    Member = models.ForeignKey(Member, on_delete=models.CASCADE)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def TokenCreate(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)