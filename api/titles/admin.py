from django.contrib import admin

from api.titles.models import Titles, Review, Comment


class TitleAdmin(admin.ModelAdmin):
    list_display = ("name",)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("text",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("text",)


admin.site.register(Titles)
admin.site.register(Review)
admin.site.register(Comment)
