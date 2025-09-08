from django.contrib import admin
from .models import Agent, Tool

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('agent_id', 'agent_name', 'description')
    search_fields = ('agent_name',)
    list_filter = ('agent_name',)

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('tool_id', 'tool_name', 'tool_description')
    search_fields = ('tool_name',)
    list_filter = ('tool_name',)