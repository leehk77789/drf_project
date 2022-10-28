from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    #비밀번호 해시처리
    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        #해싱 = set_password
        user.set_password(password)
        #db전달
        user.save()
        return user
    
    #정보 수정시 재검증
    def update(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user

#내가 보고싶은 토큰 내용 추가 (email을 추가함)
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email

        return token