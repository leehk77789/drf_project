from dataclasses import field
from rest_framework import serializers
from articles.models import Article, Comment

class CommentSerializer(serializers.ModelSerializer):
    #user를 email로 바꿔준다. user는 이제 email값이 된다.
    user = serializers.SerializerMethodField()
    def get_user(self, obj):
        return obj.user.email
    
    class Meta:
        model = Comment
        exclude = ("article", )

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content", )

class ArticleSerializer(serializers.ModelSerializer):
    #게시글 조회할 때 댓글 정보도 같이 보여주기
    user = serializers.SerializerMethodField()
    #user를 email로 바꿔준다. user는 이제 email값이 된다.
    comment_set = CommentSerializer(many=True)
    #users의 model.user의 값을 email로 해놨기 때문에 연결된 값인 email로 값을 보여준다.
    likes = serializers.StringRelatedField(many=True)

    def get_user(self, obj):
        return obj.user.email

    class Meta:
        model = Article
        fields = '__all__'

class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("title", "image", "content")

class ArticleListSerializer(serializers.ModelSerializer):
    #시리얼라이저 메소드 필드를 위해서 원하는 값들을 추가로 보여줄 수 있음
    user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.email

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comment_set.count()

    class Meta:
        model = Article
        fields = ("pk", "title", "image", "updated_at", "user", "likes_count", "comments_count")