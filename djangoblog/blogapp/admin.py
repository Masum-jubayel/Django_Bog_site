from django.contrib import admin
from .models import author, category, article,postComment


# Register your models here.
class authorModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__", "details"]
    list_per_page = 10

    class Meta:
        Model = author


admin.site.register(author, authorModel)


class articleModel(admin.ModelAdmin):
    list_display = ("__str__", "posted_on", "article_author")
    search_fields = ["__str__", "details", "body"]
    list_per_page = 10
    list_filter = ("posted_on", "category", "title")

    class Meta:
        Model = article


admin.site.register(article, articleModel)


class categoryModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__"]
    list_per_page = 10

    class Meta:
        Model = category


admin.site.register(category, categoryModel)

class postCommentModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__"]
    list_per_page = 10

    class Meta:
        Model = postComment


admin.site.register(postComment, postCommentModel)
