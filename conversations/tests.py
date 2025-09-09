from django.test import TestCase
from users.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from agents.models import Agent, Tool
from conversations.models import Conversation, Step


class ConversationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )

    def test_conversation_creation(self):
        conversation = Conversation.objects.create(
            user=self.user,
            title='Test Conversation'
        )
        self.assertEqual(conversation.title, 'Test Conversation')
        self.assertEqual(conversation.user, self.user)
        self.assertIsNotNone(conversation.created_at)
        self.assertIsInstance(conversation.created_at, timezone.now().__class__)
        self.assertEqual(
            str(conversation),
            f"Conversation {conversation.conversation_id}: {conversation.title} (User: {self.user.email})"
        )

    def test_conversation_ordering(self):
        first = Conversation.objects.create(user=self.user, title='First')
        second = Conversation.objects.create(user=self.user, title='Second')
        conversations = Conversation.objects.all()
        self.assertEqual(conversations[0], second)
        self.assertEqual(conversations[1], first)

    def test_conversation_db_table(self):
        self.assertEqual(Conversation._meta.db_table, 'conversation')


class StepModelTestCase(TestCase):
 def setUp(self):
    self.user = User.objects.create_user(
        email="testuser@example.com",
        password="password123",
        first_name="Test",
        last_name="User"
    )

 
    self.conversation = Conversation.objects.create(
        user=self.user,
        title="Test Conversation"
    )

   
    self.agent = Agent.objects.create(
        agent_id="agent_001",
        description="An agent for testing",
        config={}  
    )

    self.tool = Tool.objects.create(
        tool_name="calculator",
        description="Performs math operations",
        config={}
    )

    def test_step_creation(self):
        """Test creating a Step with valid data"""
        step = Step.objects.create(
            conversation=self.conversation,
            step_order=1,
            type='thought',
            content={"text": "I am thinking..."},
            agent=self.agent,
            tool=self.tool
        )

        self.assertIsNotNone(step.step_id)
        self.assertEqual(step.conversation, self.conversation)
        self.assertEqual(step.step_order, 1)
        self.assertEqual(step.type, 'thought')
        self.assertEqual(step.content, {"text": "I am thinking..."})
        self.assertEqual(step.agent, self.agent)
        self.assertEqual(step.tool, self.tool)
        self.assertIsNotNone(step.created_at)

    def test_step_str_representation(self):
        """Test __str__ method"""
        step = Step.objects.create(
            conversation=self.conversation,
            step_order=2,
            type='tool_call',
            content={"tool": "calculator", "args": [1, 2]}
        )
        expected_str = f"Step 2 in Conversation {self.conversation.conversation_id} (Tool Call)"
        self.assertEqual(str(step), expected_str)

    def test_step_requires_conversation(self):
        """Test that conversation is required"""
        with self.assertRaises(IntegrityError):
            Step.objects.create(
                conversation=None, 
                step_order=1,
                type='thought',
                content={}
            )

    def test_step_requires_step_order(self):
        """Test that step_order is required"""
        with self.assertRaises(IntegrityError):
            Step.objects.create(
                conversation=self.conversation,
                step_order=None,  
                type='thought',
                content={}
            )

    def test_step_requires_type(self):
        """Test that type is required and must be valid choice"""
        
        with self.assertRaises(IntegrityError):
            Step.objects.create(
                conversation=self.conversation,
                step_order=1,
                type=None,
                content={}
            )

      
        with self.assertRaises(ValidationError):
            step = Step(
                conversation=self.conversation,
                step_order=1,
                type='invalid_type',
                content={}
            )
            step.full_clean()  

    def test_step_content_accepts_json(self):
        """Test that content accepts valid JSON structures"""
        valid_contents = [
            {"key": "value"},
            [1, 2, 3],
            "string is allowed in JSONField in newer Django",
            42,
            True,
            None
        ]

        for content in valid_contents:
            step = Step.objects.create(
                conversation=self.conversation,
                step_order=1,
                type='observation',
                content=content
            )
            self.assertEqual(step.content, content)

    def test_optional_tool_and_agent(self):
        """Test that tool and agent can be null"""
        step = Step.objects.create(
            conversation=self.conversation,
            step_order=3,
            type='thought',
            content={"text": "No tool or agent needed"}
        )

        self.assertIsNone(step.tool)
        self.assertIsNone(step.agent)

    def test_step_ordering(self):
        """Test default ordering by conversation then step_order"""
        step3 = Step.objects.create(conversation=self.conversation, step_order=3, type='thought', content={})
        step1 = Step.objects.create(conversation=self.conversation, step_order=1, type='thought', content={})
        step2 = Step.objects.create(conversation=self.conversation, step_order=2, type='thought', content={})

        steps = Step.objects.filter(conversation=self.conversation)
        self.assertEqual(list(steps), [step1, step2, step3]) 
    def test_index_usage(self):
        """Smoke test: Ensure query uses index (no error, observe in EXPLAIN if needed)"""
     
        for i in range(1, 4):
            Step.objects.create(
                conversation=self.conversation,
                step_order=i,
                type='thought',
                content={"step": i}
            )

      
        steps = Step.objects.filter(conversation=self.conversation).order_by('step_order')
        self.assertEqual(steps.count(), 3)
      