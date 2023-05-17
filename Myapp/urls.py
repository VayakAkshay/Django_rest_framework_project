from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'posts', views.PostViewset, basename='post')
router.register(r'like', views.LikeViewset, basename='like')
router.register(r'users', views.UserViewSet,basename="users")

urlpatterns = [
    path('',views.All_Posts,name="All_Posts"),
]

urlpatterns += router.urls