from django.urls import path, include
from rest_framework.routers import DefaultRouter

from django.urls import path
from .views import (
    UserViewSet,
    ReviewViewSet,
    RegisterView,
    LoginView,
    LogoutView,
    AgentViewSet,
    ToolViewSet
)


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'agents', AgentViewSet, basename='agents')
router.register(r'tools', ToolViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view({'post': 'create'}), name='register'),
    path('login/', LoginView.as_view({'post': 'login'}), name='login'),
    path('logout/', LogoutView.as_view({'post': 'logout'}), name='logout'),
   
]


