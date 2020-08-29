from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:category>', views.category, name='category'),
    path('<int:category>/<int:subcategory>',
         views.subcategory, name='subcategory'),
    path('<int:category>/<int:subcategory>/<int:reading_id>',
         views.reading, name='reading'),

    # search engine routes
    path('search/<int:category>', views.search, name='search'),
    path('search/<int:category>/<int:subcategory>',
         views.search_subcategoy, name='search_subcategoy'),

    # API routes
    path("edit/<int:post_id>", views.edit, name="editAPI"),
    path('edit-review/<int:review_id>',
         views.editReview, name='edit-review'),
    path('<int:category>/<int:subcategory>/delete/<int:reading_id>',
         views.delete_reading, name='delete_reading'),
    path('<int:category>/<int:subcategory>/bananalike/<int:reading_id>',
         views.bananaLike, name='bananaLike'),

    # authentication Routes
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
