from django.urls import path, include
from . import views
from .views import PostViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'articles', PostViewSet, basename='article')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.home, name='home'),
    path('articles/<int:pk>/', views.article, name='single_article'),
    path('add_post/', views.add_post, name='add_post'),
    path('edit_post/<int:pk>/', views.update_post, name='update-post'),
    path('delete_post/<int:pk>/', views.delete_post, name='delete-post'),
]
