from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from .models import Article


# Create your views here.
class ArticleListView(ListView):
    model = Article
    template_name = "article_list.html"


class ArticleDetailView(DetailView):
    model = Article
    template_name = "article_detail.html"


class ArticleUpdateView(UpdateView):
    model = Article
    fields = (
        "title",
        "body"
    )
    template_name = "article_edit.html"


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")


class ArticleCreateView(CreateView):
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
