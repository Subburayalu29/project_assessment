from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, MaxLengthValidator
from rest_framework.exceptions import ValidationError

from Testapp.validators import validate_file_size
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(blank=False, max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_name = models.CharField(blank=False, max_length=256)
    course_id = models.CharField(blank=True, max_length=256)
    category = models.ForeignKey(Category, related_name='categories', on_delete=models.CASCADE, null=True,
                                 blank=False)
    document = models.FileField(null=True, blank=True)
    start_date = models.DateField(auto_now_add=True, null=True)
    end_date = models.DateField(auto_now=True, null=True)
    member = models.ForeignKey(User, related_name='members', on_delete=models.CASCADE, null=True, blank=False)
    description = models.CharField(blank=False, max_length=256)
    created_by = models.ForeignKey(User, blank=False, null=True, related_name='course_user_id',
                                   on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.course_name


class CourseModule(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    name = models.CharField(max_length=256)
    level = models.IntegerField(default=1)
    parent_id = models.ForeignKey('self', blank=True, null=True, related_name='child', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, default=None)
    created_by = models.ForeignKey(User, blank=False, null=True, related_name='course_module_user_id',
                                   on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CourseModuleComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.TextField(validators=[MaxLengthValidator(512)])
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=False,
                                  related_name='course_comment')
    module_id = models.ForeignKey(CourseModule, on_delete=models.CASCADE, null=True, blank=False,
                                  related_name='module_comment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, blank=False, null=True, related_name='course_comment_user_id',
                                   on_delete=models.CASCADE)


class CourseModuleAttachment(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    file = models.FileField(blank=False, null=True, upload_to='files/',
                            validators=[FileExtensionValidator(allowed_extensions=["png", "jpg", "mp4"]),
                                        validate_file_size])
    module_id = models.ForeignKey(CourseModule, null=True, blank=False,
                                  related_name='module', on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=False,
                                  related_name='course')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, blank=False, null=True, related_name='user_id', on_delete=models.CASCADE)


class CourseModuleContent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(blank=True, null=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=False,
                                  related_name='course_content')
    module_id = models.ForeignKey(CourseModule, on_delete=models.CASCADE, null=True, blank=False,
                                  related_name='module_content')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, blank=False, null=True, related_name='course_content_user_id',
                                   on_delete=models.CASCADE)


class CourseModuleAssignee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assignee = models.ForeignKey(User, blank=False, null=True, related_name='course_module_assignee',
                                 on_delete=models.CASCADE)
    module_id = models.ForeignKey(CourseModule, on_delete=models.CASCADE, null=True, blank=False,
                                  related_name='module_assignee')
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=False,
                                  related_name='course_assignee')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, blank=False, null=True, related_name='assignee_user_id',
                                   on_delete=models.CASCADE)


class CourseModuleTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=False,
                                  related_name='course_id_tag')
    module_id = models.ForeignKey(CourseModule, on_delete=models.CASCADE, null=True, blank=False,
                                  related_name='module_id_tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, blank=False, null=True, related_name='course_tag_user_id',
                                   on_delete=models.CASCADE)
    tag = models.ManyToManyField('self')
    tag_limit = 64

    def tag_changed(sender, **kwargs):
        instance = kwargs['instance']
        if len(instance.tag.all()) >= instance.tag_limit:
            raise ValidationError(f'Max number of records is {instance.tag_limit}')
