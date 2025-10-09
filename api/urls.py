from django.urls import path, include
from rest_framework.routers import DefaultRouter

from django.urls import path
from .views import (
    UserViewSet,
    ReviewViewSet,
    RegisterView,
    LoginView,
    LogoutView,
    ConversationViewSet,
    AgentViewSet,
    ToolViewSet,
    StepViewSet,
    RunViewSet,
    PasswordResetRequestView, 
    PasswordResetConfirmView
)


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'agents', AgentViewSet, basename='agents')
router.register(r'tools', ToolViewSet)
router.register(r'steps', StepViewSet, basename='steps')
router.register(r'runs', RunViewSet, basename='run')


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view({'post': 'create'}), name='register'),
    path('login/', LoginView.as_view({'post': 'login'}), name='login'),
    path('logout/', LogoutView.as_view({'post': 'logout'}), name='logout'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]


