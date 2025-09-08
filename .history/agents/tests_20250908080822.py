from django.test import TestCase
from .models import Agent

class AgentModelTest(TestCase):
    def setUp(self):
        self.agent = Agent.objects.create(
            agent_name="Test Agent",
            description="A test agent for unit testing."
        )

    def test_agent_creation(self):
        """Test that an agent can be created and saved."""
        self.assertEqual(self.agent.agent_name, "Test Agent")
        self.assertEqual(self.agent.description, "A test agent for unit testing.")
        self.assertIsInstance(self.agent, Agent)

    def test_agent_str_representation(self):
        """Test the string representation of the agent."""
        self.assertEqual(str(self.agent), "Test Agent")

    def test_agent_id_auto_increment(self):
        """Test that agent_id is auto-incremented and primary key."""
        another_agent = Agent.objects.create(
            agent_name="Second Agent",
            description="Another test agent."
        )
        self.assertNotEqual(self.agent.agent_id, another_agent.agent_id)
        self.assertTrue(another_agent.agent_id > self.agent.agent_id)