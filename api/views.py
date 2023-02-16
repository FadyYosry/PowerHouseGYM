from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Member, Gym
from .serializers import MemberSerializer, GYMSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password


@api_view(['POST'])
def create_gym_member(request):
    serializer = MemberSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_gym_member(request, pk):
    try:
        member = Member.objects.get(pk=pk)
    except Member.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = MemberSerializer(member, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_gym_member(request, pk):
    try:
        member = Member.objects.get(pk=pk)
    except Member.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    member.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def list_gym_members(request):
    members = Member.objects.all()
    serializer = MemberSerializer(members, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_gym_member(request, pk):
    try:
        member = Member.objects.get(pk=pk)
    except Member.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = MemberSerializer(member)
    return Response(serializer.data)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            member = Member.objects.get(username=username)
        except Member.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'Invalid credentials'})
        if not member.check_password(password):
            return JsonResponse({'status': 'failed', 'message': 'Invalid credentials'})
        login(request, member)
        return JsonResponse({'status': 'success', 'user': member.first_name})
    else:
        return JsonResponse({'status': 'failed', 'message': 'Invalid request method'})
        
# Viwes for GYM

@api_view(['POST'])
def create_gym(request):
    serializer = GYMSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_gym(request, pk):
    try:
        gym = Gym.objects.get(pk=pk)
    except Gym.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = GYMSerializer(gym, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_gym(request, pk):
    try:
        gym = Gym.objects.get(pk=pk)
    except Gym.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    gym.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_gym(request):
    gym = Gym.objects.all()
    serializer = GYMSerializer(gym, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_gym(request, pk):
    try:
        gym = Gym.objects.get(pk=pk)
    except Gym.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = GYMSerializer(gym)
    return Response(serializer.data)