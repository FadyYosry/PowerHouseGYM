from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Member, Gym
from .serializers import MemberSerializer, GYMSerializer
from django.contrib.auth import login
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth import login

@api_view(['POST'])
def create_gym_member(request):
    serializer = MemberSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        response_data = {
            'status': True,
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    response_data = {
        'status': False,
        'errors': serializer.errors
    }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


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
        return Response({'Status' : 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

    member.delete()
    return Response({'Status' : 'Deleted successfuly'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def list_gym_members(request):
    members = Member.objects.all()
    serializer = MemberSerializer(members, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_gym_member(request, pk=None, username=None):
    if pk is not None:
        member = get_object_or_404(Member, pk=pk)
    elif username is not None:
        member = get_object_or_404(Member, username=username)
    else:
        return Response({'error': 'Either pk or username must be provided'}, status=400)
    serializer = MemberSerializer(member)
    return Response(serializer.data)
    
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')
        member = None

        if username_or_email is not None:  # Add a check to ensure username_or_email is not None
            # Check if input is an email address
            if '@' in username_or_email:
                try:
                    member = Member.objects.get(email=username_or_email)
                except Member.DoesNotExist:
                    return JsonResponse({'status': 'false', 'message': 'Email not Found!'})

        # If input is not an email, lookup by username
        if not member:
            try:
                member = Member.objects.get(username=username_or_email)
            except Member.DoesNotExist:
                return JsonResponse({'status': 'false', 'message': 'Invalid credentials username', 'username' : username_or_email})

        if not member:
            return JsonResponse({'status': 'false', 'message': 'Invalid credentials'})

        # If member is found, check password and log in
        if member.check_password(password):
            login(request, member)
            return JsonResponse({'status': 'true', 'message': 'Login successfully'  , 'user': member.first_name})
        else:
            return JsonResponse({'status': 'false', 'message': 'Password is not correct!'})
    else:
        return JsonResponse({'status': 'false ', 'message': 'Invalid request method'})

        
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
    return Response({'Status' : 'Deleted successfuly'},status=status.HTTP_204_NO_CONTENT)

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