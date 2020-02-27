from rest_framework import serializers, viewsets
from rest_framework.permissions import AllowAny
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    permission_classes = (AllowAny,)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'gender', 'age', 'username', 'created_on', 'last_login',
                  'password', 'pref_mode_travel', 'pref_gender', 'rating', 'country', 'phone_number']

    def save(self):
        userDetails = User(first_name=self.validated_data['first_name'],
                           last_name=self.validated_data['last_name'],
                           gender=self.validated_data['gender'],
                           email=self.validated_data['email'],
                           username=self.validated_data['username'],
                           age=self.validated_data['age'],
                           pref_mode_travel=self.validated_data['pref_mode_travel'],
                           pref_gender=self.validated_data['pref_gender'],
                           country=self.validated_data['country'],
                           phone_number=self.validated_data['phone_number']
                           )
        password = self.validated_data['password']
        userDetails.set_password(password)
        userDetails.save()
        return userDetails

