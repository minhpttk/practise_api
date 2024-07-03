from rest_framework import serializers
from .models import Employee
import datetime


class CreatEmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields=['id','fullname','date_of_birth','gender','profile_picture']

    def validate_date_of_birth(self, value):
        if value > datetime.date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value
    
    def validate_fullname(self, value):
        # Example: Ensure the fullname has a minimum length
        if len(value) < 3:
            raise serializers.ValidationError("Full name must be at least 3 characters long.")
        return value
    
    def validate_fullname(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Full name must be at least 3 characters long.")
        return value

    def to_internal_value(self, data):
        if 'gender' in data:
            gender = data['gender'].strip().lower()
            if gender in ['m', 'male']:
                data['gender'] = 'M'
            elif gender in ['f', 'female']:
                data['gender'] = 'F'
            elif gender in ['o', 'other']:
                data['gender'] = 'O'
            else:
                raise serializers.ValidationError({
                    'gender': ["Gender must be 'M', 'F', 'O', 'Male', 'Female', or 'Other'."]
                })
        return super().to_internal_value(data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['gender'] == 'M':
            representation['gender'] = 'Male'
        elif representation['gender'] == 'F':
            representation['gender'] = 'Female'
        elif representation['gender'] == 'O':
            representation['gender'] = 'Other'
        return representation
    
class FilterEmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields=['id','fullname','date_of_birth','gender','profile_picture']



class GetOneEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'  


class UpdateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields=['id','fullname','date_of_birth','gender','profile_picture']

    def validate_date_of_birth(self, value):
        if value > datetime.date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value
    
    def validate_fullname(self, value):
        # Example: Ensure the fullname has a minimum length
        if len(value) < 3:
            raise serializers.ValidationError("Full name must be at least 3 characters long.")
        return value
    
    def validate_fullname(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Full name must be at least 3 characters long.")
        return value

    def to_internal_value(self, data):
        if 'gender' in data:
            gender = data['gender'].strip().lower()
            if gender in ['m', 'male']:
                data['gender'] = 'M'
            elif gender in ['f', 'female']:
                data['gender'] = 'F'
            elif gender in ['o', 'other']:
                data['gender'] = 'O'
            else:
                raise serializers.ValidationError({
                    'gender': ["Gender must be 'M', 'F', 'O', 'Male', 'Female', or 'Other'."]
                })
        return super().to_internal_value(data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['gender'] == 'M':
            representation['gender'] = 'Male'
        elif representation['gender'] == 'F':
            representation['gender'] = 'Female'
        elif representation['gender'] == 'O':
            representation['gender'] = 'Other'
        return representation


class SoftDeleteEmployeeSerializer(serializers.Serializer):
    deleted = serializers.BooleanField(default=True)