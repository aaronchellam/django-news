from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin

from .forms import CommentForm
from .models import Article


# Create your views here.
class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "article_list.html"


class CommentGet(DetailView):
    model = Article
    template_name = "article_detail.html"

    def get_context_data(self, **kwargs):
        # Pull all existing information into the context.
        context = super().get_context_data(**kwargs)

        # Update the context.
        context['form'] = CommentForm()
        return context


class CommentPost(SingleObjectMixin, FormView):
    model = Article
    form_class = CommentForm
    template_name = "article_detail.html"

    def post(self, request, *args, **kwargs):
        # Use get_object() from SingleObjectMixin which allows us to grab the article pk from the url.
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    # form_valid() is called when form validation has succeeded.
    def form_valid(self, form):
        # Before saving the comment to the database, we have to specify the article is belongs to.
        # Initially we save the for but set commit=False because in the next line we must associate the correct article with the form object.
        comment = form.save(commit=False)
        comment.article = self.object

        # Set the author to be the current logged in user.
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        article = self.get_object()
        return reverse("article_detail", kwargs={"pk": article.pk})


class ArticleDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = (
        "title",
        "body"
    )
    template_name = "article_edit.html"

    def test_func(self):
        # Get the current object returned by the view.
        obj = self.get_object()

        # If the author on the current object matches the current user on the webpage (whoever is logged in), then allow the change.
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user



# LoginRequiredMixin will redirect users to the login page if attempting to access the creation url.
class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "article_new.html"
    fields = (
        'title',
        'body',
        # 'author'
    )

    # New articles' authors should default to the logged in user.
    # form_valid is called when the submitted form is valid.
    def form_valid(self, form):
        # Override the default behaviour to set the author of the new article to the currently logged in user.
        form.instance.author = self.request.user
        # Call the parent class's 'form_valid' method
        return super().form_valid(form)
