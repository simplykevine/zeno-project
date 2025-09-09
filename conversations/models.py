from django.db import models
from users.models import User
from agents.models import Agent, Tool

class Conversation(models.Model):
   conversation_id = models.AutoField(primary_key=True)
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
   title = models.TextField()
   created_at = models.DateTimeField(auto_now_add=True)


   class Meta:
       db_table = 'conversation'
       ordering = ['-created_at']


   def __str__(self):
    return f"Conversation {self.conversation_id}: {self.title} (User: {self.user.email})"


class Step(models.Model):
    STEP_TYPE_CHOICES = [
        ('thought', 'Thought'),
        ('tool_call', 'Tool Call'),
        ('observation', 'Observation'),
        ('sub_agent_call', 'Sub Agent Call'),
    ]

    step_id = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='steps')
    step_order = models.IntegerField()
    type = models.CharField(max_length=20, choices=STEP_TYPE_CHOICES)
    content = models.JSONField() 
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, null=True, blank=True, related_name='steps')
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True, blank=True, related_name='steps')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['conversation', 'step_order']
        verbose_name = "Step"
        verbose_name_plural = "Steps"
        indexes = [
            models.Index(fields=['conversation', 'step_order']),
        ]

    def __str__(self):
        return f"Step {self.step_order} in Conversation {self.conversation_id} ({self.get_type_display()})"