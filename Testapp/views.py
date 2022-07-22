from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Category, CourseModule, Course, CourseModuleAttachment, \
    CourseModuleContent, CourseModuleComment, CourseModuleTag, CourseModuleAssignee
from .serializers import Categoryserializer, RegisterSerializer, UserSerializer, \
    CourseModuleSerializer, CourseModuleAttachmentSerializer, Courseserializer, \
    CourseModuleContentSerializer, CourseModuleCommentSerializer, MyTokenObtainPairSerializer, \
    CourseModuleTagSerializer, CourseModuleAssigneeSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserDetailAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = Categoryserializer


class CourseView(ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = Courseserializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


class ModuleView(ModelViewSet):
    serializer_class = CourseModuleSerializer
    queryset = CourseModule.objects.filter(parent_id=None).all()


class ModuleAttachmentView(ModelViewSet):
    queryset = CourseModuleAttachment.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CourseModuleAttachmentSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


class ModuleContentView(ModelViewSet):
    queryset = CourseModuleContent.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CourseModuleContentSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


class ModuleCommentView(ModelViewSet):
    queryset = CourseModuleComment.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CourseModuleCommentSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


class ModuleTagView(ModelViewSet):
    queryset = CourseModuleTag.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CourseModuleTagSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


class CourseModuleAssigneeView(ModelViewSet):
    queryset = CourseModuleAssignee.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CourseModuleAssigneeSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}