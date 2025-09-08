from django.urls import path, include
from rest_framework.routers import DefaultRouter

from django.urls import path
from .views import (
    UserViewSet,
    ReviewViewSet,
    RegisterView,
    LoginView,
    LogoutView,
    AgentListCreateView, 
    AgentRetrieveUpdateDestroyView,
    ConversationViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'conversations', ConversationViewSet, basename='conversation')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view({'post': 'create'}), name='register'),
    path('login/', LoginView.as_view({'post': 'login'}), name='login'),
    path('logout/', LogoutView.as_view({'post': 'logout'}), name='logout'),
    path('agents/', AgentListCreateView.as_view(), name='agent-list-create'),
    path('agents/<int:agent_id>/', AgentRetrieveUpdateDestroyView.as_view(), name='agent-detail')
]


