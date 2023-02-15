from rest_framework import serializers
from .models import Member, Gym

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class GYMSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = '__all__'