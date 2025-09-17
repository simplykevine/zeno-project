from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, role="User", password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role="Admin",
            password=password,
            **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("User", "User"),
        ("Admin", "Admin"),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="User")
    email = models.EmailField(max_length=255, unique=True)
    image = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.email} ({self.role})"
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    




class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    review_text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="reviews")
    rating = models.IntegerField(choices=[(1, "Positive"), (0, "Negative")])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.review_id} by {self.user.first_name if self.user else 'Anonymous'}"




