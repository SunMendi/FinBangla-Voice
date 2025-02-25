from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


# Create your views here.
def home(request):
    context = {"posts": Post.objects.all(), "title": "Home"}
    return render(request, "blogs/blog_home.html", context)


class PostListView(ListView):
    model = Post
    template_name = "blogs/blog_home.html"  # <app> / <model>_<viewtype>.html
    context_object_name = "posts"
    ordering = ["-date_posted"]  # for ordering the newest blog to the top of the page.
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Blogs"
        return context


class UserPostListView(ListView):
    model = Post
    template_name = "blogs/user_posts.html"  # <app> / <model>_<viewtype>.html
    context_object_name = "posts"
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted")

    """
    the upper function 'get_queryset' must be this spelling. if there occurs any mispelling 
    then the posts of every particular author will not be shown correctly at
    user_posts.html page. 
    """


class PostDetailView(DetailView):
    model = Post
    template_name = "blogs/post_detail.html"  # Specify the template location
    context_object_name = "post"  # Name of the object in the template context

    def get_context_data(self, **kwargs):
        """
        Add additional context data, such as the current user, to the template.
        """
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user  # Add the current user to the context
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
