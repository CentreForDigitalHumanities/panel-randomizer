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
def index(request, name):
    template = loader.get_template('panelrandomizer_app/index.html')
    return render(request, 'panelrandomizer_app/index.html', {'name': name,}) #name van het onderzoek wordt doorgegeven

def forward(request, name):
    student_number = request.POST['student_number']  # request.POST is a dictionary-like object that lets you access submitted data by key name. In this case, request.POST['choice']
    
    key = settings.PANELRANDOMIZER_CONFIG[0]['ENCRYPTION_KEY'] # encryption key uit settings halen
    cipher = AES.new(key.encode(), AES.MODE_EAX)
    student_number_cipher = cipher.encrypt_and_digest(student_number.encode())  # alle data naar AES object moeten byte gecodeerd zijn, ook wat je wil encrypten!
    student_number_hash = (hashlib.sha1(student_number.encode())).hexdigest()  # hash maken voor identificatie of student al heeeft meegedaan
    
    print(student_number_hash)

    base_url = settings.PANELRANDOMIZER_CONFIG[0]['BASE_URL']  # base url ophalen uit settings
    user_agent = parse(request.META['HTTP_USER_AGENT']) # useragent, desktop of mobiel

    # probleem: terugzoeken van encrypted nummer kan niet, want geeft telkens een andere, dus je kan er niet op filteren
    # idee: ook studentnummer als hash opslaan, zodat je hier wel op kan zoeken, ivm het eenmalig invullen van vragenlijst
    # student_in_db_enc = Participant.objects.filter(studentnumber_enc= student_number_cipher) # zoeken in db , probleem encryption is telkens anders
    student_in_db_hash = Participant.objects.filter(studentnumber_hash= student_number_hash)
    print(student_in_db_hash)



    if (student_in_db_hash):
         return HttpResponse('student gevonden')
        # return redirect('https://nl-nl.facebook.com/')
    
    else:

        #os=user_agent.os
        #user_agent.is_mobile dit geeft false of true
        #user_agent.is_pc true or false
        #user_agent.is_tablet

        p=Participant(studentnumber_enc=student_number_cipher, studentnumber_hash=student_number_hash ) #participation_date moet verplicht ingevuld worden not_null, datetime field
        p.save()
        
        
        return HttpResponse(base_url)
        
        # return redirect(base_url)

	    #return HttpResponse(request)

