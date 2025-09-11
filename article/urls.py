from . import views
from django.urls import path



urlpatterns = [
    path("article/<slug:slug>/", views.article_detail, name="article_list"),
    path ('gallery/', views.gallery, name='gallery')
]
