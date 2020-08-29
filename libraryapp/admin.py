from django.contrib import admin
from .models import Category, Film, Image, Key, Post, Subcategory, Reading, Review, User

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Subcategory)
admin.site.register(Reading)
admin.site.register(Film)
admin.site.register(Image)
admin.site.register(Key)
admin.site.register(Review)
admin.site.register(User)
