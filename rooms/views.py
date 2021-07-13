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
from django.views.generic import ListView


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
