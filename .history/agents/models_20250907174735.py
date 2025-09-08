from django.db import models

class Agent(models.Model):
    agent_id = models.AutoField(primary_key=True)
    agent_name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.agent_name