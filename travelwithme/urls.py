from django.urls import path

from . import views

app_name = 'travelwithme'

urlpatterns = [
    path('', views.index, name='index'),
    path('search_trips', views.search_trips, name='search_trips'),
    path('login', views.login_page, name='login'),
    path('signup', views.signup, name='signup'),
    path('signup_user', views.signup_user, name='signup_user'),
    path('create_trip', views.create_trip, name='create_trip'),
    path('logout', views.log_user_out, name='logout'),
    path('mytrips', views.mytrips, name='mytrips'),
    path('user_info/<int:traveller_id>', views.user_info, name='user_info'),
    path('log_user_in', views.log_user_in, name='log_user_in'),
    path('myrequests', views.my_requests, name='myrequests'),
    path('send_trip_request/<int:trip_id>', views.send_trip_request, name='send_trip_request'),
    path('cancel_trip_request/<int:trip_request_id>', views.cancel_trip_request, name='cancel_trip_request'),
    path('decline_trip_request/<int:trip_request_id>', views.decline_trip_request, name='decline_trip_request'),
    path('accept_trip_request/<int:trip_request_id>', views.accept_trip_request, name='accept_trip_request'),
    path('requests_to_my_trip/<int:trip_id>', views.see_requests_to_my_trip, name='requests_to_my_trip'),
    path('complete_trip/<int:trip_id>', views.complete_trip, name='complete_trip'),
    path('rate_user/<int:trip_id>/<int:user_id>', views.rate_user, name='rate_user'),
    path('submit_rating/<int:user_id>', views.submit_rating, name='submit_rating'),
]
