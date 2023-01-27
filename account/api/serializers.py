from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    is_admin = SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'is_admin']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def get_is_admin(self, obj):
        return obj.is_superuser

    def validate(self, attrs):
        try:
            self.Meta.model.objects.get(username=attrs['email'])
            raise ValidationError({'email': 'User already exists!'})
        except self.Meta.model.DoesNotExist:
            pass
        try:
            validate_password(attrs['password'])
        except DjangoValidationError as e:
            raise ValidationError({'password': e.messages})
        return attrs

    def create(self, validated_data):
        user = get_user_model()(
            email=validated_data['email'],
            username=validated_data['email'],
            last_name=validated_data['last_name'],
            first_name=validated_data['first_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
