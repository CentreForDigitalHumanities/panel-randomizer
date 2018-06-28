from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import Participant, Survey
from user_agents import parse #https://github.com/selwin/python-user-agents
from django.conf import settings
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import hashlib
from .forms import ParicipantForm # eigen form in forms.py
import base64


# Create your views here.
def url_invalid(request): #als variabele name niet is ingevuld
    template = loader.get_template('panelrandomizer_app/url_invalid.html')
    return render(request, 'panelrandomizer_app/url_invalid.html')


def index(request, name):
    try:
        # form = ParicipantForm() # hier formmodel dat gemaakt is als variabele en doorsturen naar index.html Even niet gebruiken, erg omslachtig voor 1 veld
        survey=Survey.objects.get(survey_name=name)
        template = loader.get_template('panelrandomizer_app/index.html')
        return render(request, 'panelrandomizer_app/index.html', {'name': name, 'expected_completion_time': survey.expected_completion_time,}) 
    
    except Survey.DoesNotExist:
        template = loader.get_template('panelrandomizer_app/url_invalid.html')
        return render(request, 'panelrandomizer_app/url_invalid.html')


def forward(request, name):

    student_number = request.POST['student_number']
    survey=Survey.objects.get(survey_name=name)
    
    # controleren of een nummer is ingevuld en anders de pagina opnieuw ophalen
    if student_number=="":
        error_message='vul aub uw studentnummer in'
        return render(request, 'panelrandomizer_app/index.html', {'name': name, 'expected_completion_time': survey.expected_completion_time, 'error_message':error_message}) 

    survey=Survey.objects.get(survey_name=name)
    param_st_enc=survey.integration_parameter_student_enc
    param_branching=survey.integration_parameter_branching

    key = settings.PANELRANDOMIZER_CONFIG[0]['ENCRYPTION_KEY'] # encryption key uit settings halen
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    BLOCK_SIZE = 32
    student_number_cipher = cipher.encrypt( pad( student_number.encode(), BLOCK_SIZE ) )  # alle data naar AES object moeten byte gecodeerd zijn, ook wat je wil encrypten
    student_number_cipher_dec=base64.b64encode(student_number_cipher ).decode() #  base64 coderen en van bytes een str maken om te kunnen meesturen in url
    student_number_hash = ( hashlib.sha1( student_number.encode() ) ).hexdigest()  # hash maken voor identificatie of student al heeeft meegedaan
    base_url = settings.PANELRANDOMIZER_CONFIG[0]['BASE_URL']  # base url ophalen uit settings
    user_agent = parse(request.META['HTTP_USER_AGENT']) # useragent, desktop of mobiel
    last_group=survey.last_group
    number_of_groups=survey.number_of_groups

    if (last_group < number_of_groups):
        new_group=last_group +1
    else:
        new_group=1
    
    


    # probleem: terugzoeken van encrypted nummer kan niet, want geeft telkens een andere, dus je kan er niet op filteren
    # ook studentnummer als hash opslaan, zodat je hier wel op kan zoeken, ivm het eenmalig invullen van vragenlijst
    # student_in_db_enc = Participant.objects.filter(studentnumber_enc= student_number_cipher) # zoeken in db , probleem encryption is telkens anders
    student_in_db_hash = Participant.objects.filter(studentnumber_hash= student_number_hash) # filter geeft een list, get geeft de feitelijke waarde, beter get gebruiken?
   
    if (student_in_db_hash):
        template = loader.get_template('panelrandomizer_app/exit.html')
        return render(request, 'panelrandomizer_app/exit.html')
    else:
        if(user_agent.is_pc | user_agent.is_tablet):
            survey_code=survey.survey_code_desktop
            #print('is pc')
        else:
            survey_code=survey.survey_code_mobile
            #print ('is mobiel')

        # url samenstellen
        redirect_url=base_url+"/"+survey_code+"?newtest=Y&Lang=nl&"+param_branching+"="+str(new_group)+"&"+param_st_enc+"="+student_number_cipher_dec
        
        # opslaan gehashed studentnummer en cipher(is opslaan cipher hier wel nodig?)
        p=Participant(studentnumber_enc=student_number_cipher, studentnumber_hash=student_number_hash )
        p.save()
        
        # tabel updaten met new_group voor roulatie
        Survey.objects.filter(survey_name = name).update(last_group = new_group)

        return redirect(redirect_url)


