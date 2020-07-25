from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,
                                     style={"input_type": "password"})
    password_confirm = serializers.CharField(write_only=True, style={"input_type": "password"},
                                             label="Confirm password")

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password_confirm')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        confirm_password = validated_data['password_confirm']

        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise serializers.ValidationError(
                {"email": "Email address must be unique."}
            )
        if password != confirm_password:
            raise serializers.ValidationError(
                {"password": "Two passwords are different."}
            )
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return user
