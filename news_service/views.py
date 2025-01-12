import json
from django.db.models import Q
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .aws import s3_manager, AWS_BUCKET_NAME
from .forms import NewsFilterForm, PostForm
from .models import NewsPost


class NewsListView(generic.ListView):
    model = NewsPost
    template_name = "html/news/news_list.html"
    context_object_name = "news"
    ordering = ["-created_at"]
    paginate_by = 6

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
    ordering = ["-created_at"]
    paginate_by = 6

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

        if category:
            queryset = queryset.filter(category_id=category)

        if sort_by:
            if sort_by == "created_at_asc":
                queryset = queryset.order_by("created_at")
            elif sort_by == "created_at_desc":
                queryset = queryset.order_by("-created_at")

        return queryset


class PostDetailView(generic.DetailView):
    model = NewsPost
    template_name = "html/news/post_detail.html"
    context_object_name = "post"


@login_required(login_url="/user/login/")
@require_POST
def create_post(request):
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user

        image = form.cleaned_data["image_link"]
        image_link = s3_manager.upload_image(image, AWS_BUCKET_NAME, image.name)

        if image_link:
            post.image_link = image_link
            post.save()  #

            return redirect("post_detail", pk=post.pk)
        else:
            form.add_error(None, "Failed to upload image. Please try again.")
    return render(request, "html/news/create_post.html", {"form": form})


def all_posts(request):
    query = request.GET.get("q")
    with open("news_service/utils/parsed_data.json", "r", encoding="utf-8") as file:
        posts = json.load(file)

    if query:
        posts = [post for post in posts if query.lower() in post["title"].lower()]

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
