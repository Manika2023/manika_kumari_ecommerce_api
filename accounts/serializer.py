from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
# your custom user model
# from accounts.models import User 
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken

# get_user_model() dynamically fetches the active User model.
#    This is better than importing User directly, because:
#    - You might later use a custom user model (with email, phone, etc.).
#    - It ensures compatibility with AUTH_USER_MODEL in settings.py.
User = get_user_model()
print("user",User)

# serializer for User Profile
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=['username','first_name','last_name','email','address','phone']

# serializer for registration        
class RegisterSerializer(serializers.ModelSerializer):
    # write_only=True means:
    #    - This field is accepted in input (when registering a user).
    #    - BUT it is NOT shown in API responses (to protect sensitive data).
    #    - Example: password is stored securely, never exposed in JSON output.
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'phone', 'address']

    def create(self, validated_data):
        # create_user() automatically hashes the password before saving.
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone', ''),
            address=validated_data.get('address', '')
        )
        return user

# validating input and returning tokens.
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    print("user in serilaizer: ",User)
    password = serializers.CharField(write_only=True)

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    print(email,password,access,refresh)
    
    def validate(self, attrs):
        # access above attrs
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # authenticate returns- None if Credentials are invalid
            user= authenticate(email=email,password=password)
            if not user:
                raise serializers.ValidationError("Invalid email")
            if not user.is_active:
                raise serializers.ValidationError("user account is disabled")

            # genrate tokens
            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)
            # add in attrs by these keys
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(access)
            # include user object if needed
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError("email and password are required")    
        
# serializer for profile
 