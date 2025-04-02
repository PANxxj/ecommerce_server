from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from apps.helper import keys

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source="profile.gender")
    profile_photo = serializers.ImageField(source="profile.profile_photo")
    full_name = serializers.SerializerMethodField(source="get_full_name")

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "full_name",
            "gender",
        ]



    def to_representation(self, instance):
        representation = super(UserSerializer, self).to_representation(instance)
        if instance.is_superuser:
            representation["admin"] = True
        return representation


class CreateUserSerializer(UserCreateSerializer):
    id  = serializers.SerializerMethodField(read_only=True)
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["id", "full_name", "email","user_type", "password"]
        
    def get_id(self,obj):
        return obj.pk
        


class RegisterUserSerializer(serializers.ModelSerializer):
    id  = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email', 'user_type', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', ''),
            user_type=validated_data.get('user_type', keys.CUSTOMER) 
        )
        return user

    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value
    
    def get_id(self,obj):
        return obj.pk

