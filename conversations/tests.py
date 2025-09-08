from django.test import TestCase
from users.models import User
from .models import Conversation
from django.utils import timezone

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
