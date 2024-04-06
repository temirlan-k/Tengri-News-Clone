import uuid
from django.db import models

from autoslug import AutoSlugField


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="name")

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class NewsPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(max_length=1500, blank=True)
    image_link = models.CharField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
