from django.db import models
from django.db.models import JSONField

class Agent(models.Model):
    agent_id = models.AutoField(primary_key=True)
    agent_name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.agent_name

class Tool(models.Model):
    tool_id = models.AutoField(
        primary_key=True,
        help_text="Unique ID for each tool."
    )
    tool_name = models.CharField(
        max_length=255,
        unique=True,
        help_text="The name of the tool."
    )
    tool_description = models.TextField(
        help_text="A description of what the tool does."
    )
    meta_data = models.JSONField(
        help_text="A JSON object that defines the required parameters for the tool."
    )
    def __str__(self):
        return self.tool_name

