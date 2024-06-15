from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, FriendRequest, Message
from .serializers import UserSerializer, FriendRequestSerializer, MessageSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        from_user = request.user
        to_user = User.objects.get(id=data['to_user'])
        friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
        if created:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.accepted = True
        instance.save()
        from_user = instance.from_user
        to_user = instance.to_user
        from_user.friends.add(to_user)
        to_user.friends.add(from_user)
        return Response(status=status.HTTP_200_OK)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        sender = request.user
        receiver = User.objects.get(id=data['receiver'])
        message = Message.objects.create(sender=sender, receiver=receiver, content=data['content'])
        return Response(status=status.HTTP_201_CREATED)
