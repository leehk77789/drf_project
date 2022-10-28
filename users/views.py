from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

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