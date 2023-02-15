from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Member
from .serializers import MemberSerializer

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
