from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import Participant, Survey
from user_agents import parse #https://github.com/selwin/python-user-agents
from django.conf import settings
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES
from pprint import pprint
import hashlib

# Create your views here.
def url_invalid(request): #als variabele name niet is ingevuld
    template = loader.get_template('panelrandomizer_app/url_invalid.html')
    return render(request, 'panelrandomizer_app/url_invalid.html')

def index(request, name):
    try:
        survey=Survey.objects.get(survey_name=name)
        template = loader.get_template('panelrandomizer_app/index.html')
        return render(request, 'panelrandomizer_app/index.html', {'name': name, 'expected_completion_time': survey.expected_completion_time,}) 
    except Survey.DoesNotExist:
        template = loader.get_template('panelrandomizer_app/url_invalid.html')
        return render(request, 'panelrandomizer_app/url_invalid.html')

def forward(request, name):

    # TODO: valideren op aanwezigheid studentnummer
    student_number = request.POST['student_number']  # request.POST is a dictionary-like object that lets you access submitted data by key name. In this case, request.POST['choice']
    survey=Survey.objects.get(survey_name=name)
    key = settings.PANELRANDOMIZER_CONFIG[0]['ENCRYPTION_KEY'] # encryption key uit settings halen
    cipher = AES.new(key.encode(), AES.MODE_EAX)
    student_number_cipher = cipher.encrypt_and_digest(student_number.encode())  # alle data naar AES object moeten byte gecodeerd zijn, ook wat je wil encrypten!
    student_number_hash = (hashlib.sha1(student_number.encode())).hexdigest()  # hash maken voor identificatie of student al heeeft meegedaan
    base_url = settings.PANELRANDOMIZER_CONFIG[0]['BASE_URL']  # base url ophalen uit settings
    user_agent = parse(request.META['HTTP_USER_AGENT']) # useragent, desktop of mobiel

    # probleem: terugzoeken van encrypted nummer kan niet, want geeft telkens een andere, dus je kan er niet op filteren
    # idee: ook studentnummer als hash opslaan, zodat je hier wel op kan zoeken, ivm het eenmalig invullen van vragenlijst
    # student_in_db_enc = Participant.objects.filter(studentnumber_enc= student_number_cipher) # zoeken in db , probleem encryption is telkens anders
    student_in_db_hash = Participant.objects.filter(studentnumber_hash= student_number_hash) # filter geeft een list, get geeft de feitelijke waarde, beter get gebruiken?
    

    if (student_in_db_hash):
        template = loader.get_template('panelrandomizer_app/exit.html')
        return render(request, 'panelrandomizer_app/exit.html')
    else:
         #user_agent.is_mobile dit geeft false of true
        #user_agent.is_pc true or false
        #user_agent.is_tablet
        if(user_agent.is_pc | user_agent.is_tablet):
            survey_code=survey.survey_code_desktop
        else:
            survey_code=survey.survey_code_mobile
          

        redirect_url=base_url+"/"+survey_code
        print (redirect_url)
        #opslaan gehashed studentnummer en cipher(is opslaan cipher hier wel nodig?)
        p=Participant(studentnumber_enc=student_number_cipher, studentnumber_hash=student_number_hash )
        p.save()
        
        # return HttpResponse(redirect_url)
        
        return redirect(redirect_url)

	    #return HttpResponse(request)

