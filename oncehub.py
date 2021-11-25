import requests
headers = {"Accept": "application/json",
            "API-Key":'93ac76f21aa5562d1e7ed19391e9620c'}

def booking_page_owner(bp_id):
    url = "https://api.oncehub.com/v2/booking-pages/"+bp_id
    return requests.request("GET", url, headers=headers).json()['name']

def client_bookings(cient_email):
    url = "https://api.oncehub.com/v2/bookings"
    response=requests.request("GET", url, headers=headers).json()['data']
    return [
            (booking['starting_time'],
            booking['subject'],
            booking_page_owner(booking['booking_page']),
            booking['virtual_conferencing']) 
            for booking in response 
            if booking['form_submission']['email']==cient_email
                and booking['status']!='canceled']
def oncehub_user_id(coach_email):
    url = "https://api.oncehub.com/v2/users"
    users=requests.request("GET", url, headers=headers).json()['data']
    for user in users:
        if user['email']==coach_email:
            return user['id']

def coach_bookings(coach_email):
    url = "https://api.oncehub.com/v2/bookings"
    response=requests.request("GET", url, headers=headers).json()['data']
    return [
            (booking['starting_time'],
            booking['subject'],
            booking['form_submission']['name'],
            booking['virtual_conferencing']) 
            for booking in response 
            if booking['owner']==oncehub_user_id(coach_email)
                and booking['status']!='canceled']