from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from travelwithme.models import Traveller, Trip, TripRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.utils.dateparse import parse_date
from enum import Enum


FEMALE_AVATAR = "https://www.shareicon.net/download/2016/06/26/786569_people_512x512.png"
MALE_AVATAR = "https://www.shareicon.net/download/2016/07/05/791215_people_512x512.png"

class TripRequestStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"

class TripStatus(Enum):
    TERMINATED = "terminated"
    COMPLETED = "completed"
    ONGOING = "ongoing"
    OPEN = "open"


# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request, "travelwithme/searchtrip.html", {"user":request.user})
def login_page(request):
    if request.user.is_authenticated:
         return redirect("travelwithme:index")
    return render(request, "travelwithme/login.html")

def signup(request):
    if request.user.is_authenticated:
         return redirect("travelwithme:index")
    return render(request, "travelwithme/signup.html")

def log_user_out(request):
    logout(request)
    return redirect("travelwithme:index")

def mytrips(request):
    if request.user.is_authenticated:
        traveller = request.user.traveller
        trips = Trip.objects.filter(creator=traveller)
        return render(request, "travelwithme/mytrips.html",{"trips":trips})
    return render(request, "travelwithme/login.html")

def user_info(request,traveller_id):
    if request.method == "GET":
        if request.user.is_authenticated:
            traveller = get_object_or_404(Traveller,pk=traveller_id)
            return render(request, "travelwithme/user_info.html", {"traveller":traveller})
        else:
            return redirect("travelwithme:login")

def my_requests(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            trip_requests = TripRequest.objects.filter(initiator=request.user.traveller)
            return render(request, "travelwithme/myrequests.html", {"trip_requests":trip_requests})
        else:
            return redirect("travelwithme:login")

def see_requests_to_my_trip(request,trip_id):
    if request.method == "GET":
        if request.user.is_authenticated:
            trip = get_object_or_404(Trip, pk=trip_id)
            requests_to_my_trip = TripRequest.objects.filter(trip=trip.id)
            return render(request, "travelwithme/requests_to_my_trip.html", {"requests_to_my_trip":requests_to_my_trip})
        else:
            return redirect("travelwithme:login")







#POST handlers

def complete_trip(request, trip_id):
    if request.method == "GET":
        if request.user.is_authenticated:
            trip = get_object_or_404(Trip, pk=trip_id)
            if trip.creator.user.id != request.user.id:
                return render(request, "travelwithme/alltrips.html", {"error": "Can not complete other's trips"})
            else:
                Trip.objects.filter(pk=trip_id).update(status=TripStatus.COMPLETED.value)
                return HttpResponseRedirect('/requests_to_my_trip/%d'%trip.id)
        else:
            return redirect("travelwithme:login")

    else:
        return HttpResponse(status=500)


def accept_trip_request(request, trip_request_id):
    if request.method == "GET":
        if request.user.is_authenticated:
            trip_request = get_object_or_404(TripRequest, pk=trip_request_id)
            if trip_request.trip.creator.user.id != request.user.id:
                return render(request, "travelwithme/alltrips.html", {"error": "Accepting request not belonging to your trip"})
            else:
                TripRequest.objects.filter(pk=trip_request_id).update(status=TripRequestStatus.CONFIRMED.value)
                Trip.objects.filter(pk=trip_request.trip.id).update(status=TripStatus.ONGOING.value)
                return HttpResponseRedirect('/requests_to_my_trip/%d'%trip_request.trip.id)
        else:
            return redirect("travelwithme:login")

    else:
        return HttpResponse(status=500)


def decline_trip_request(request, trip_request_id):
    if request.method == "GET":
        if request.user.is_authenticated:
            trip_request = get_object_or_404(TripRequest, pk=trip_request_id)
            if trip_request.trip.creator.user.id != request.user.id:
                return render(request, "travelwithme/alltrips.html", {"error": "Deleting request not belonging to your trip"})
            else:
                TripRequest.objects.get(pk=trip_request_id).delete()
                return redirect("travelwithme:mytrips")
        else:
            return redirect("travelwithme:login")

    else:
        return HttpResponse(status=500)


def cancel_trip_request(request, trip_request_id):
    if request.method == "GET":
        if request.user.is_authenticated:
            trip_request = get_object_or_404(TripRequest, pk=trip_request_id)
            if trip_request.initiator.user.id != request.user.id:
                return render(request, "travelwithme/alltrips.html", {"error": "Can not cancel other people requests."})
            else:
                TripRequest.objects.get(pk=trip_request_id).delete()
                return redirect("travelwithme:myrequests")
        else:
            return redirect("travelwithme:login")

    else:
        return HttpResponse(status=500)



def send_trip_request(request, trip_id):
    if request.method == "GET":
        if request.user.is_authenticated:
            #validate if request already there
            trip = get_object_or_404(Trip, pk=trip_id)
            trip_request = TripRequest.objects.filter(initiator=request.user.traveller, trip=trip)
            if trip_request.count() != 0 and trip.creator.user.id != request.user.id:
                return render(request, "travelwithme/alltrips.html", {"error": "Request was already sent. Check your requests"})
            else:
                TripRequest.objects.create(initiator=request.user.traveller, trip=trip, status=TripRequestStatus.PENDING.value)
                return redirect("travelwithme:myrequests")
        else:
            return redirect("travelwithme:login")

    else:
        return HttpResponse(status=500)




def search_trips(request):
    if request.method == "POST":
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        destination = request.POST["destination"]
        if start_date is not None and end_date is not None and destination is not None:
            if not start_date and not end_date and not destination:
                trips = Trip.objects.all()
                if request.user.is_authenticated:
                    trips = Trip.objects.filter(~Q(creator = request.user.traveller))
            elif not start_date and not end_date:
                trips = Trip.objects.filter(place__icontains=destination)
                if request.user.is_authenticated:
                    trips = Trip.objects.filter(~Q(creator = request.user.traveller),place__icontains=destination)
            elif not start_date or not end_date:
                return render(request, "travelwithme/searchtrip.html",{"error":"Date must be provided"})
            elif not destination:
                #search by dates
                trips = Trip.objects.filter(start_date__range=(start_date, end_date))
                if request.user.is_authenticated:
                    trips = Trip.objects.filter(~Q(creator = request.user.traveller), start_date__range=(start_date, end_date))
            else:
                #normal search
                trips = Trip.objects.filter(place=destination, start_date__range=(start_date, end_date))
                if request.user.is_authenticated:
                    trips = Trip.objects.filter(~Q(creator = request.user.traveller),place=destination, start_date__range=(start_date, end_date))
        return render(request, "travelwithme/alltrips.html",{"trips":trips})
    else:
        return HttpResponse(status=500)

def create_trip(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user
            place = request.POST['place']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            if place is not None and start_date is not None and end_date is not None:
                if not place or not start_date or not end_date:
                    return render(request, "travelwithme/searchtrip.html", {"error":"Empty fields"})
                else:
                    date_start_date = parse_date(start_date)
                    date_end_date = parse_date(end_date)
                    if date_end_date < date_start_date:
                        return render(request, "travelwithme/searchtrip.html", {"error":"Dates mismatch"})
                    Trip.objects.create(creator=user.traveller, place=place, start_date=start_date, end_date=end_date, status=TripStatus.OPEN.value)
                    return redirect("travelwithme:mytrips")
                    #redirect to my trips.

        else:
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=500)


def signup_user(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        nationality = request.POST['nationality']
        birthday = request.POST['birthday']
        gender = request.POST['gender']
        password = request.POST['password']
        hobbies = request.POST['hobbies']
        if first_name is not None and last_name is not None and email is not None and nationality is not None and birthday is not None and password is not None and gender is not None and hobbies is not None:
            if not first_name or not last_name or not email or not nationality or not birthday or not gender or not password:
                return render(request, "travelwithme/signup.html", {"error":"Empty fields"})
            elif User.objects.filter(email=email).exists():
                return render(request, "travelwithme/signup.html", {"error":"User exists"})
            else:
                username = email
                if gender == "male":
                    user = User.objects.create_user(username, email=email, first_name=first_name, last_name=last_name, password=password)
                    traveller = Traveller.objects.create(user=user, hobbies=hobbies, nationality=nationality, birthday=birthday, gender=gender, avatar=MALE_AVATAR).save()
                elif gender == "female":
                    user = User.objects.create_user(username, email=email, first_name=first_name, last_name=last_name, password=password)
                    traveller = Traveller.objects.create(user=user, hobbies=hobbies, nationality=nationality, birthday=birthday, gender=gender, avatar=FEMALE_AVATAR).save()
                user.save()
                login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                return redirect("travelwithme:index")


        else:
            return render(request, "travelwithme/signup.html", {"error":"Error in fields"})
    else:
        return render(request, "travelwithme/signup.html")

def log_user_in(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        if email is not None and password is not None:
            if not email or not password:
                return render(request, "travelwithme/login.html", {"error": "Empty input"})

            else:
                username = email
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("travelwithme:index")
                else:
                    return render(request, "travelwithme/login.html", {"error":"Wrong username or password"})

        else:
            return render(request, "travelwithme/login.html", {"error": "Error in fields"})
    else:
        return redirect("travelwithme:login")
