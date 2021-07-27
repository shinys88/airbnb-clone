from math import ceil
from datetime import datetime
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from . import models, forms


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




# 6-1. 검색기능 직접 만들기.
def search1(request):

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
    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")
    
    print(s_amenities, s_facilities)

    form = {
        "city": city, 
        "s_room_type": room_type, 
        "s_country": country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "superhost": superhost
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


    filter_args = {}

    # if price != 0:
    #     qs.filter(price__lte=price)

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country"] = country

    if room_type != 0 :
        # filter_args["room_type__pk__exact"] = room_type
        filter_args["room_type__pk"] = room_type

    if price != 0:
        filter_args["price__lte"] = price

    if guests != 0:
        filter_args["guests__gte"] = guests

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if beds != 0:
        filter_args["beds__gte"] = beds

    if baths != 0:
        filter_args["baths__gte"] = baths

    if instant is True:
        filter_args["instant_book"] = True

    # Room Objects의 host => Forenkey => superhost
    if superhost is True:
        filter_args["host__superhost"] = True

    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            filter_args["amenities__pk"] = int(s_amenity)

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            filter_args["facilities__pk"] = int(s_facility)




    rooms = models.Room.objects.filter(**filter_args)


    


    return render(
        request,
        "rooms/search1.html",
        {**form, **choices, "rooms":rooms},
    )



from django.views.generic import View



# 6-2. 검색기능 Django forms 기능 활용하여 만들기.
# def search(request):
class SearchView(View):
    def get(self, request):

        country = request.GET.get("country")

        if country:

            form = forms.SearchForm(request.GET)
            if form.is_valid():
                print(form.cleaned_data)

                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                price = form.cleaned_data.get("price")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")


                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                # rooms = models.Room.objects.filter(**filter_args)
                qs = models.Room.objects.filter(**filter_args).order_by("created")
                paginator = Paginator(qs, 10, orphans=5)
                page = request.GET.get("page", 1)
                rooms = paginator.get_page(page)

                return render(request, "rooms/search.html", {"form":form, "rooms":rooms})


        else:
            form = forms.SearchForm()
            # rooms = models.Room.objects.all()

        # unbound form

        return render(request, "rooms/search.html", {"form":form})





from django.views.generic import UpdateView
from users import mixins as user_mixins
from django.http import Http404


# 챕터24. Room 수정, 생성, 이미지
class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


#사진 삭제
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "cant delete that photo")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo Deleted")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))

    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))