from rest_framework import serializers
from service.models import *

class RegisterClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        exclude = ['card_number']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        extra_kwargs = {'card_number': {'read_only': True}}


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        exclude = ['last_login']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        role = validated_data.pop('role')
        user = Instructor.objects.create(**validated_data)
        user.role.set(role)
        user.set_password(validated_data['password'])
        user.save()


        return user

class IntervalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interval
        fields = '__all__'

class PassTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassType
        fields = '__all__'

class SectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionType
        fields = '__all__'

class PassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pass
        fields = '__all__'

    def validate(self, data):
        if data['section'] is None and data['pass_type'] is None:
            raise serializers.ValidationError("One of these fields is required")
        if data['section'] is not None and data['pass_type'] is not None:
            raise serializers.ValidationError("Only one of these fields is required")

        return data

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'