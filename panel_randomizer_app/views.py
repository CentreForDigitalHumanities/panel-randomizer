from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import Participant, Survey
import user_agents
from django.conf import settings
import base64
from django.db import transaction
import urllib.parse


def url_invalid(request):
    template = loader.get_template('panel_randomizer_app/url_invalid.html')
    return render(request, 'panel_randomizer_app/url_invalid.html')


def index(request, name):
    try:
        survey = Survey.objects.get(survey_name=name)
        template = loader.get_template('panel_randomizer_app/index.html')
        return render(request, 'panel_randomizer_app/index.html', {'name': name, 'expected_completion_time': survey.expected_completion_time, })

    except Survey.DoesNotExist:
        template = loader.get_template('panel_randomizer_app/url_invalid.html')
        return render(request, 'panel_randomizer_app/url_invalid.html')


def participate(request, name):

    student_number = request.POST['student_number']
    survey = Survey.objects.get(survey_name=name)

    if len(student_number) < 3:
        error_message = 'vul aub uw studentnummer in'
        return render(request, 'panel_randomizer_app/index.html', {
            'name': name,
            'student_number': student_number,
            'expected_completion_time': survey.expected_completion_time,
            'error_message': error_message}
        )

    aes_secret = settings.APP_CONFIG['AES_SECRET'].encode()
    hmac_secret = settings.APP_CONFIG['HMAC_SECRET'].encode()
    student_number_cipher_dec = Participant.encode(
        aes_secret, hmac_secret, student_number)  # method in Models

    #  start transaction
    with transaction.atomic():

        student_in_db_enc = Participant.objects.filter(
            student_number_enc=student_number_cipher_dec)

        if student_in_db_enc:
            template = loader.get_template('panel_randomizer_app/exit.html')
            return render(request, 'panel_randomizer_app/exit.html')
        else:
            return redirect(redirect_participant(request, name, student_number, student_number_cipher_dec))


def redirect_participant(request, name, student_number, student_number_cipher_dec):
    survey = Survey.objects.get(survey_name=name)
    param_st_enc = survey.integration_parameter_student_enc
    param_branching = survey.integration_parameter_branching
    # use for testing connection and transfer of variables to limesurvey survey
    test_key = settings.APP_CONFIG['TEST_KEY']
    user_agent = user_agents.parse(request.META['HTTP_USER_AGENT'])
    last_group = survey.last_group
    number_of_groups = survey.group_count

    if (last_group < number_of_groups):
        new_group = last_group + 1
    else:
        new_group = 1

    survey_url = get_survey_url(survey, user_agent)[0]
    device_participant = get_survey_url(survey, user_agent)[1]

    params = {param_branching: new_group,
              param_st_enc: student_number_cipher_dec}

    if '?' in survey_url:
        redirect_url = survey_url+"&"+urllib.parse.urlencode(params)
    else:
        redirect_url = survey_url+"?"+urllib.parse.urlencode(params)

    if(student_number != test_key):
        participation = Participant(
            student_number_enc=student_number_cipher_dec, device_participant=device_participant)
        participation.save()

        # update table for rotation increment
        Survey.objects.filter(survey_name=name).update(
            last_group=new_group)

    return redirect_url


def get_survey_url(survey, user_agent):
    device_participant = 'DESKTOP'
    if(user_agent.is_pc or user_agent.is_tablet):
        survey_url = survey.survey_desktop_url
    else:
        if survey.survey_mobile_url != "":  # check if mobile url exists in database
            survey_url = survey.survey_mobile_url
            device_participant = 'MOBILE'
        else:
            survey_url = survey.survey_desktop_url
    return [survey_url, device_participant]
