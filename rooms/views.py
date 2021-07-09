from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from . import models


def all_rooms_test(request):
    # print(vars(request))
    now = datetime.now()
    hungry = True
    # return HttpResponse(content=f"hello{now}")
    return render(
        request, "all_rooms_test.html", context={"now": now, "hungry": hungry}
    )


def all_rooms(request):
    all_rooms = models.Room.objects.all()
    return render(request, "rooms/home.html", context={"potato": all_rooms})
