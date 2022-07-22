from rest_framework.routers import DefaultRouter
from .views import CategoryView, ModuleView, ModuleAttachmentView, UserDetailAPI, \
    RegisterUserAPIView, CourseView, ModuleContentView, ModuleCommentView, MyTokenObtainPairView, ModuleTagView, \
    CourseModuleAssigneeView
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView,
)

router = DefaultRouter()
router.register('category', CategoryView)
router.register('course', CourseView)
router.register('module', ModuleView)
router.register('attachment', ModuleAttachmentView)
router.register('content', ModuleContentView)
router.register('comment', ModuleCommentView)
router.register('tag', ModuleTagView)
router.register('assignee', CourseModuleAssigneeView)

urlpatterns = [
    path('api/', include(router.urls)),
    path("get-details", UserDetailAPI.as_view()),
    path('user-register', RegisterUserAPIView.as_view()),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
