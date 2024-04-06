import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect

from .aws import s3_manager, AWS_BUCKET_NAME
from .forms import NewsFilterForm, PostForm
from .models import NewsPost


class NewsListView(generic.ListView):
    model = NewsPost
    template_name = "html/news/news_list.html"
    context_object_name = "news"
    ordering = ["-created_at"]
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = context["news"]
        context["filter_form"] = NewsFilterForm(self.request.GET)
        paginator = Paginator(news, self.paginate_by)
        page = self.request.GET.get("page")

        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)

        context["news"] = news
        context["user"] = self.request.user
        return context


class SearchNewsView(generic.ListView):
    model = NewsPost
    template_name = "html/news/news_list.html"
    context_object_name = "object_list"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = NewsFilterForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        sort_by = self.request.GET.get("sort_by")
        category = self.request.GET.get("category")

        if query:
            queryset = queryset.filter(Q(title__icontains=query))

        if sort_by:
            if sort_by == "created_at_asc":
                queryset = queryset.order_by("created_at")
            elif sort_by == "created_at_desc":
                queryset = queryset.order_by("-created_at")

        if category:
            queryset = queryset.filter(category_id=category)

        return queryset


class PostDetailView(generic.DetailView):
    model = NewsPost
    template_name = "html/news/post_detail.html"
    context_object_name = "post"


def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            category = form.cleaned_data["category"]
            image = request.FILES["image_link"]

            image_link = s3_manager.upload_image(image, AWS_BUCKET_NAME, image.name)
            if image_link:
                post = NewsPost(
                    title=title,
                    content=content,
                    category=category,
                    image_link=image_link,
                )
                post.save()

                return redirect("post_detail", pk=post.pk)
            else:

                print("fail")
    else:
        form = PostForm()
    return render(request, "html/news/create_post.html", {"form": form})


def all_posts(request):
    with open("news_service/utils/parsed_data.json", "r", encoding="utf-8") as file:
        posts = json.load(file)

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    try:
        page_posts = paginator.page(page_number)
    except PageNotAnInteger:
        page_posts = paginator.page(1)
    except EmptyPage:
        page_posts = paginator.page(paginator.num_pages)

    context = {"posts": page_posts}
    return render(request, "html/news/parsed_news.html", context)


def post_detail(request, post_id):
    with open("news_service/utils/parsed_data.json", "r", encoding="utf-8") as file:
        posts = json.load(file)

    post = None
    for p in posts:
        if p["id"] == post_id:
            post = p
            break

    context = {"post": post}
    return render(request, "html/news/parsed_news_details.html", context)
