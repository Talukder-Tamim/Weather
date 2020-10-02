from django.shortcuts import render, redirect
import requests
from .models import State
from .forms import StateForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=69fe0e2a1a17172799635b20f80df522'
    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = StateForm(request.POST)
        if form.is_valid():
            new_state = form.cleaned_data['name']
            state_count = State.objects.filter(name=new_state).count()

            if state_count == 0:
                data = requests.get(url.format(new_state)).json()
                if data['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City doesnt exist in the world!'
            else:
                err_msg = 'City already exists in the database!'
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully'
            message_class = 'is-success'

    forms = StateForm()

    states = State.objects.all()

    weather_info = []

    for state in states:
        data = requests.get(url.format(state)).json()

        state_weather = {
            'city': state.name,
            'temperature': (data['main']['temp'] -32) * 5//9,
            'description': data['weather'][0]['description'], 
            'icon': data['weather'][0]['icon']
        }

        weather_info.append(state_weather)

    context = {
        'state_temp': weather_info,
        'forms': forms,
        'message': message,
        'message_class': message_class
        }
    return render(request, 'weather.html', context)


def delete_state(request, ct_name):
    state = State.objects.get(name=ct_name)
    state.delete()
    return redirect('index')