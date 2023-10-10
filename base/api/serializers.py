from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from base.models import File


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        # Overriding the default behaviour of hte password field
        # to use set_password for hashing before saving
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class FileSerializer(ModelSerializer):
    class Meta: 
        model = File
        fields = '__all__'
        