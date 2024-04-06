from django.contrib.auth.models import User
from django.db import models
from news_service.models import Category
from django.utils.crypto import get_random_string


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name="subscriptions")
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        categories_names = ", ".join(
            [category.name for category in self.categories.all()]
        )
        return f"{self.user.email} - {categories_names} Subscription"

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"


class EmailConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=32)

    @classmethod
    def create(cls, user):
        token = get_random_string(length=32)
        return cls.objects.create(user=user, token=token)
