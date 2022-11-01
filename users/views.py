from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from users import serializers
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer, UserPorifleSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User

class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

class FollowView(APIView):
    def post(self, request, user_id):
        you = get_object_or_404(User, id=user_id)
        me = request.user
        #내가 너의 팔로워에 있으면 나를 팔로워 목록에서 지워라
        if me in you.followers.all():
            you.followers.remove(me)
            return Response("unfollow했습니다.", status=status.HTTP_200_OK)
        #아니면 나를 팔로워 목록에 추가해라
        else:
            you.followers.add(request.user)
            return Response("follow했습니다.", status=status.HTTP_200_OK)

#내가 보고싶은 토큰 내용 추가
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

#로그인 확인
class mockView(APIView):
    #로그인 되었을때만
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        user.is_admin = True
        user.save()
        return Response("get요청")

class ProfileView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserPorifleSerializer(user)

        return Response(serializer.data)