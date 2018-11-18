from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from travelwithme.models import Traveller, Trip
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request, "travelwithme/searchtrip.html", {"user":request.user})

def users(request):
    return render(request, "travelwithme/alltrips.html")

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


#POST handlers

def create_trip(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user
            place = request.POST['place']
            start_date = request.POST['start_date']
            end_date = request.POST['start_date']
            if place is not None and start_date is not None and end_date is not None:
                if not place or not start_date or not end_date:
                    return render(request, "travelwithme/searchtrip.html", {"error":"Empty fields"})
                else:
                    Trip.objects.create(creator=user.traveller, place=place, start_date=start_date, end_date=end_date)
                    return redirect("travelwithme:index")
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
                user = User.objects.create_user(username, email=email, first_name=first_name, last_name=last_name, password=password)
                traveller = Traveller.objects.create(user=user, hobbies=hobbies, nationality=nationality, birthday=birthday, gender=gender).save()
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
