from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from travelwithme.models import Traveller

# Create your views here.
def index(request):
    return render(request, "travelwithme/searchtrip.html")
def users(request):
    return render(request, "travelwithme/alltrips.html")
def login(request):
    return render(request, "travelwithme/login.html")
def signup(request):
    return render(request, "travelwithme/signup.html")


#POST handlers

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
                print("!!!!!!!")
                username = email
                user = User.objects.create_user(username, email=email, first_name=first_name, last_name=last_name, password=password)
                traveller = Traveller.objects.create(user=user, hobbies=hobbies, nationality=nationality, birthday=birthday, gender=gender).save()
                user.save()
                return redirect("travelwithme:index")


        else:
            return render(request, "travelwithme/signup.html", {error:"Error in fields"})
    else:
        return render(request, "travelwithme/signup.html")
