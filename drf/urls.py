from django.urls import path
from drf.v1.blog_post.views import PostViewSet

app_name = "drf"

urlpatterns = [
    path('blog/post/', PostViewSet.as_view({'get': 'get'})),
    path('blog/post/<int:pk>', PostViewSet.as_view({'get': 'retrieve'})),
]