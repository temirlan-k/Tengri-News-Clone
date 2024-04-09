import uuid
from tengrinews import settings
from django.db import models
from autoslug import AutoSlugField
from django.urls import reverse
from django.http import request


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="name")

    def __str__(self):
        return self.name


class NewsPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(max_length=1500, blank=True)
    image_link = models.CharField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def get_absolute_url(self):
        url = reverse("post_detail", kwargs={"pk": self.pk})

        current_request = request
        base_url = settings.BASE_URL
        absolute_url = base_url + url
        return absolute_url

    def __str__(self):
        return self.title
