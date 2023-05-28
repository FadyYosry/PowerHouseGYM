from django.contrib import admin
from .models import Gym,Member,AdminGym, Admin
# Register your models here.

admin.site.register(Gym)
admin.site.register(Member)
admin.site.register(AdminGym)
admin.site.register(Admin)