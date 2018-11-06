from django.db import models

# Create your models here.

class Traveller(models.Model):
    '''
    id - automatic
    name - CharField
    email - EmailField
    rating - IntField
    hobby - TextField
    '''
    pass
    


class Trip(models.Model):
    '''
    When trip is done it should delete all corresponding requests. 
    Or they must be cleaned once trip is locked (???)
    id
    creator -> association with Traveller
    place
    start_date
    end_date
    request_sent - boolean (indicates if it is possible to send a request or not)
    '''
    pass

#Maybe add EmailRequest model. Via email people can discuss more.

class TripRequest(models.Model):
    '''
    In order to decline the trip from trip owner perspective:
    Make a post request and delete the TripRequest from DB.
    Optionally notify the initiator by using his id and email via emailing backend.
    Accept button will lock the trip to be proceeding (started).
    id
    initiator - relationships
    trip_owner - relationships
    '''
    pass

class Comment(models.Model):
    '''
    id
    content
    creator - association with traveller
    receiver - association with traveller
    '''
    pass

class TripRecording(models.Model):
    '''
    Can be used to prevent unwanted commenting.
    Only people who were on a trip could comment each other.
    As an idea...
    '''
    pass