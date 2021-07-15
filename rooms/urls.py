from django.urls import path
from django.urls import path
from . import views

app_name = "rooms"

# 함수방식
# urlpatterns = [path("<int:pk>", views.room_detail, name="detail")]

# DetailView class 방식
urlpatterns = [path("<int:pk>", views.RoomDetail.as_view(), name="detail")]
