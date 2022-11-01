from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from articles.serializers import ArticleListSerializer

#유저 정보 가져오기
class UserPorifleSerializer(serializers.ModelSerializer):
    #팔로우, 팔로잉 둘 다 이메일로 표현
    followers = serializers.StringRelatedField(many=True)
    followings = serializers.StringRelatedField(many=True)

    #내가 작성한 글
    article_set = ArticleListSerializer(many=True)

    #내가 좋아요한 글
    like_articles = ArticleListSerializer(many=True)
    class Meta:
        model = User
        fields = ("id", "email", "followings", "followers", "article_set", "like_articles")

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