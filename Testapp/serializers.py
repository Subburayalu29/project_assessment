from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from .models import Category, Course, CourseModule, CourseModuleAttachment, \
    CourseModuleContent, CourseModuleComment, CourseModuleTag
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        return {
            "username": self.user.username,
            "email": self.user.email,
            "permissions": self.user.user_permissions.values_list("codename", flat=True),
            "groups": self.user.groups.values_list("name", flat=True),
            **attrs,
        }


# Serializer to Get User Details using SimpleJWT  Authentication
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username"]

        def __str__(self):
            return self.username


# Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
                  'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# Serializer to Category
class Categoryserializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']


# Serializer to Course
class Courseserializer(ModelSerializer):
    categories = Categoryserializer(read_only=True, many=False)
    members = UserSerializer(source='User', read_only=True, many=True)
    created_username = serializers.CharField(source="created_by", read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'course_name', 'course_id', 'categories', 'document', 'start_date',
                  'end_date', 'members', 'description', 'category', 'member', 'created_by',
                  'created_username']
        read_only_fields = ['created_by', 'created_username', ]

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        auth_user_id = User.objects.get(id=user_id)
        validated_data['created_by'] = auth_user_id
        user = Course.objects.create(**validated_data)
        return user


# Serializer to CourseModule
class CourseModuleSerializer(ModelSerializer):
    def to_representation(self, instance):
        children = CourseModuleSerializer(instance.child, many=True, read_only=True).data
        response = super().to_representation(instance)
        response['children'] = children

        return response

    class Meta:
        model = CourseModule
        fields = ['id', 'name', 'level', 'course_id', 'parent_id']


# Serializer to CourseModuleAttachment
class CourseModuleAttachmentSerializer(serializers.ModelSerializer):
    module = CourseModuleSerializer(read_only=True, many=True)
    course = Courseserializer(read_only=True, many=True)
    username = serializers.CharField(source="created_by", read_only=True)

    class Meta:
        model = CourseModuleAttachment
        fields = ['id', 'file', 'module_id', 'module', 'course', 'course_id', 'created_by', 'username', 'created_at',
                  'updated_at']
        read_only_fields = ['created_by', 'username']

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        auth_user_id = User.objects.get(id=user_id)
        validated_data['created_by'] = auth_user_id
        user = CourseModuleAttachment.objects.create(**validated_data)
        return user


# Serializer to CourseModuleContent
class CourseModuleContentSerializer(serializers.ModelSerializer):
    module_content = CourseModuleSerializer(read_only=True, many=True)
    course_content = Courseserializer(read_only=True, many=True)
    username = serializers.CharField(source="created_by", read_only=True)

    class Meta:
        model = CourseModuleContent
        fields = ['id', 'content', 'module_id', 'module_content', 'course_content', 'course_id', 'created_by',
                  'username', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'username']

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        auth_user_id = User.objects.get(id=user_id)
        validated_data['created_by'] = auth_user_id
        user = CourseModuleContent.objects.create(**validated_data)
        return user


class CourseModuleCommentSerializer(serializers.ModelSerializer):
    module_comment = CourseModuleSerializer(read_only=True, many=True)
    course_comment = Courseserializer(read_only=True, many=True)
    username = serializers.CharField(source="created_by", read_only=True)

    class Meta:
        model = CourseModuleComment
        fields = ['id', 'comment', 'module_id', 'module_comment', 'course_comment', 'course_id', 'created_by',
                  'username', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'username']

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        auth_user_id = User.objects.get(id=user_id)
        validated_data['created_by'] = auth_user_id
        user = CourseModuleComment.objects.create(**validated_data)
        return user


class CourseModuleTagSerializer(serializers.ModelSerializer):
    module_tag = CourseModuleSerializer(read_only=True, many=True)
    course_tag = Courseserializer(read_only=True, many=True)
    username = serializers.CharField(source="created_by", read_only=True)

    class Meta:
        model = CourseModuleTag
        fields = ['id', 'tag', 'module_id', 'module_tag', 'course_tag', 'course_id', 'created_by',
                  'username', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'username']

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        auth_user_id = User.objects.get(id=user_id)
        validated_data['created_by'] = auth_user_id
        user = CourseModuleTag.objects.create(**validated_data)
        return user
