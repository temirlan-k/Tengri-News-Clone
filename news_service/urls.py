from django.urls import path
from . import views

urlpatterns = [
    path("", views.NewsListView.as_view(), name="news_list"),
    path("news/post/<uuid:pk>", views.PostDetailView.as_view(), name="post_detail"),
    path("news/search/", views.SearchNewsView.as_view(), name="search_news"),
    path("news/create/", views.create_post, name="create_post"),
    path("news/parsed/", views.all_posts, name="all_parsed_posts"),
    path("news/parsed/detail/<str:post_id>", views.post_detail, name="post_detail"),
]
