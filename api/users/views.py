from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, generics, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from api.users.models import User
from api.users.permissions import UserPermission
from api.users.serializers import UserRegistrationSerializer, MyAuthTokenSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()


class ObtainAuthToken(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MyAuthTokenSerializer
    queryset = User.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_me(self, request):
        user = get_object_or_404(self.queryset, email=request.user.email)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch_me(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(self.queryset, email=request.user.email)
            serializer = self.serializer_class(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserDetailViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]
    lookup_field = 'username'
    filter_backends = [SearchFilter]
    search_fields = ['username']