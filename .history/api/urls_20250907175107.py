from django.urls import path
from .views import AgentListCreateView, AgentRetrieveUpdateDestroyView

urlpatterns = [
    path('agents/', AgentListCreateView.as_view(), name='agent-list-create'),
    path('agents/<int:agent_id>/', AgentRetrieveUpdateDestroyView.as_view(), name='agent-detail'),
]