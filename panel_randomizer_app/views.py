from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import Participant, Survey
from user_agents import parse
from django.conf import settings
from .forms import ParicipantForm # eigen form in forms.py
import base64


# Create your views here.
def url_invalid(request): #als variabele name niet is ingevuld
    template = loader.get_template('panel_randomizer_app/url_invalid.html')
    return render(request, 'panel_randomizer_app/url_invalid.html')


def index(request, name):
    try:
        survey=Survey.objects.get(survey_name=name)
        template = loader.get_template('panel_randomizer_app/index.html')
        return render(request, 'panel_randomizer_app/index.html', {'name': name, 'expected_completion_time': survey.expected_completion_time,}) 
    
    except Survey.DoesNotExist:
        template = loader.get_template('panel_randomizer_app/url_invalid.html')
        return render(request, 'panel_randomizer_app/url_invalid.html')


def participate(request, name):

    student_number = request.POST['student_number']
    survey=Survey.objects.get(survey_name=name)
    
    if (student_number=="" or len(student_number)<3 ):
        error_message='vul aub uw studentnummer in'
        return render(request, 'panel_randomizer_app/index.html', {
        'name': name, 
        'student_number': student_number,
        'expected_completion_time': survey.expected_completion_time, 
        'error_message':error_message}
        ) 

    survey=Survey.objects.get(survey_name=name)
    param_st_enc=survey.integration_parameter_student_enc
    param_branching=survey.integration_parameter_branching

    aes_secret = settings.PANELRANDOMIZER_CONFIG[0]['AES_SECRET'].encode() 
    hmac_secret = settings.PANELRANDOMIZER_CONFIG[0]['HMAC_SECRET'].encode() 
    student_number_cipher_dec=Participant.encode(aes_secret, hmac_secret, student_number) # method in Models

    test_key = settings.PANELRANDOMIZER_CONFIG[0]['TEST_KEY'] # tbv testen een nummer dat niet wordt opgeslagen
    user_agent = parse(request.META['HTTP_USER_AGENT']) # useragent, desktop of mobiel
    last_group=survey.last_group
    number_of_groups=survey.group_count

    if (last_group < number_of_groups):
        new_group=last_group +1
    else:
        new_group=1
    
    
    student_in_db_enc = Participant.objects.filter(student_number_enc= student_number_cipher_dec)
    
    if student_in_db_enc:
        template = loader.get_template('panel_randomizer_app/exit.html')
        return render(request, 'panel_randomizer_app/exit.html')
    else:
        if(user_agent.is_pc | user_agent.is_tablet):
            survey_url=survey.survey_desktop_url
            device_participant='DESKTOP'
        else:
            survey_url=survey.survey_mobile_url
            device_participant='MOBILE'

        redirect_url=survey_url+"&"+param_branching+"="+str(new_group)+"&"+param_st_enc+"="+student_number_cipher_dec
        
        # opslaan gehashed studentnummer en cipher, testkey voor testdoeleinden om doorverwijzing naar limesurvey te testen
        if(student_number != test_key):
            participation=Participant(student_number_enc=student_number_cipher_dec, device_participant=device_participant )
            participation.save()
        
         # update table for rotation increment
        Survey.objects.filter(survey_name = name).update(last_group = new_group)

        return redirect(redirect_url)


