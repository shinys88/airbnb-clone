from django.urls import path
from . import views

app_name = "rooms"

# 함수방식
# urlpatterns = [path("<int:pk>", views.room_detail, name="detail")]

# DetailView class 방식
urlpatterns = [
    path("<int:pk>", views.RoomDetail.as_view(), name="detail"),
    path("<int:pk>/edit/", views.EditRoomView.as_view(), name="edit"),
    path("<int:pk>/photos/", views.RoomPhotosView.as_view(), name="photos"),
    path("<int:room_pk>/photos/<int:photo_pk>/delete/", views.delete_photo, name="delete-photo"),
    # path("search/", views.search, name="search"),
    path("search/", views.SearchView.as_view(), name="search")
]
