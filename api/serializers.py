from rest_framework import serializers
from .models import Member, Gym

class GYMSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['gym_name'] = instance.gym_name
        return data

