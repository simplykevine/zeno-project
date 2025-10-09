from django.test import TestCase
from users.models import User, Review


# Create your tests here.


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@gmail.com",
            first_name="Test",
            last_name="User",
            password="Password@123"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("password123"))
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.last_name, "User")
        self.assertEqual(self.user.role, "User") 

    def test_str_method(self):
        self.assertEqual(str(self.user), "test@example.com (User)")

    def test_get_full_name(self):
        self.assertEqual(self.user.get_full_name(), "Test User")

class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="reviewer@gmail.com",
            first_name="Review",
            last_name="Author",
            password="Password@123"
        )
        self.review = Review.objects.create(
            review_text="The response is insightful",
            user=self.user,
            rating=1
        )
    
    def test_review_creation(self):
        self.assertEqual(self.review.review_text, "The response is insightful")
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.rating, 1)

    def test_review_str_method(self):
        self.assertEqual(str(self.review), f"Review {self.review.review_id} by {self.user.first_name}")

