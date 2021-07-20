from math import ceil
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models


# 1. render 실습 : 화면 테스트
def all_rooms_test(request):
    # print(vars(request))
    now = datetime.now()
    hungry = True
    # return HttpResponse(content=f"hello{now}")
    return render(
        request, "rooms/all_rooms_test.html", context={"now": now, "hungry": hungry}
    )


# 2. page 수동으로 직접 만들기
def all_rooms_page(request):

    page = request.GET.get("page", 1)
    page = int(page or 1)
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    all_rooms = models.Room.objects.all()[offset:limit]
    page_count = ceil(models.Room.objects.count() / page_size)

    return render(
        request,
        "rooms/home_paging.html",
        context={
            "potato": all_rooms,
            "page": page,
            "page_count": page_count,
            "page_range": range(1, page_count),
        },
    )


# 3. django 페이지네이터 활용
from django.core.paginator import Paginator, EmptyPage


# View => 함수 방식
def all_rooms(request):

    page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)

    # rooms = paginator.get_page(page)
    try:
        rooms = paginator.page(int(page))
        # print(room_list)
        return render(
            request,
            "rooms/home.html",
            context={"page": rooms},
        )

    except EmptyPage:
        # rooms = paginator.page(1)
        return redirect("/")


# 위에는 Function Base View
# ------------------------------------------------
# 4. 아래는 django Class Base View 사용
from django.utils import timezone
from django.views.generic import ListView, DetailView


class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    # page_kwarg = "potato"
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context


# 5-1. 상세페이지 함수방식
# from django.urls import reverse
# from django.http import Http404
# def room_detail(request, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, "rooms/detail.html", {"room": room})
#     except models.Room.DoesNotExist:
#         # return redirect("/")
#         # return redirect(reverse("core:home"))
#         raise Http404()


# 5-2. 상세페이지 DetailView class 방식
class RoomDetail(DetailView):

    """RoomDetail Definition"""

    model = models.Room
    # pk_url_kwarg = "pk"


from django_countries import countries


def search(request):

    # print(request.GET)
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))

    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))


    form = {
        "city": city, 
        "s_room_type": room_type, 
        "s_country": country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
    }


    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    return render(
        request,
        "rooms/search.html",
        {**form, **choices},
    )
