from django.urls import path
from . import views

urlpatterns = [
    path("all/", views.NewsListView.as_view(), name="news_list"),
    path("post/<uuid:pk>", views.PostDetailView.as_view(), name="post_detail"),
    path("search/", views.SearchNewsView.as_view(), name="search_news"),
    path("create/", views.create_post, name="create_post"),
    path('parsed/',views.all_posts,name='all_posts'),
    path('detail/<str:post_id>',views.post_detail,name='post_detail'),

]
