from django.contrib.auth import get_user_model
from rest_framework import permissions, decorators, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from source.accounts.serializers import UserCreateSerializer

User = get_user_model()


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def register(request):
    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    refresh = RefreshToken.for_user(user)
    response = {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    return Response(response, status.HTTP_201_CREATED)
