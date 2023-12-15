from django.contrib import admin

from .models import Article, Comment


class CommentInline(admin.TabularInline):
    model = Comment

    # No extra blank comment lines in the admin page.
    extra = 0

class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,


    ]


# Register your models here.
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
