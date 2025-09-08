from django.db import models
from users.models import User

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
