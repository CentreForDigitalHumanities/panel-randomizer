from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.utils import translation
from django.utils.translation import gettext as _

from .models import Participant, Survey, SurveyGroup
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
        set_language(survey, request)
        template = loader.get_template('panel_randomizer_app/index.html')
        return render(request, 'panel_randomizer_app/index.html',
                      {
                          'name': name,
                          'welcome_text': survey.welcome_text.splitlines()
                      })

    except Survey.DoesNotExist:
        template = loader.get_template('panel_randomizer_app/url_invalid.html')
        return render(request, 'panel_randomizer_app/url_invalid.html')


def participate(request, name):
    student_number = request.POST.get('student_number', '0')
    survey = Survey.objects.get(survey_name=name)
    set_language(survey, request)

    if len(student_number) < 3:
        error_message = _('Fill in your student number.')
        return render(request, 'panel_randomizer_app/index.html', {
            'name': name,
            'student_number': student_number,
            'welcome_text': survey.welcome_text.splitlines(),
            'error_message': error_message
        })

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
            return render(request, 'panel_randomizer_app/exit.html', {'screen_out_text': survey.screen_out_text.splitlines()})
        else:
            return redirect(redirect_participant(request, name, student_number, student_number_cipher_dec))


def redirect_participant(request, name, student_number, student_number_cipher_dec):
    survey = Survey.objects.get(survey_name=name)

    set_language(survey, request)
    param_st_enc = survey.integration_parameter_student_enc
    param_branching = survey.integration_parameter_branching
    # use for testing connection and transfer of variables to limesurvey survey
    test_key = settings.APP_CONFIG['TEST_KEY']
    user_agent = user_agents.parse(request.META['HTTP_USER_AGENT'])

    # Is there a group to manually assign to?
    survey_groups = SurveyGroup.objects.filter(survey=survey)
    max_fill_count = 0
    manual_group = None
    for group in survey_groups:
        if group.fill_count > max_fill_count:
            max_fill_count = group.fill_count
            manual_group = group

    if manual_group != None:
        new_group = manual_group.group_number
        manual_group.fill_count -= 1
        manual_group.save()
    else:
        last_group = survey.last_group
        number_of_groups = survey.group_count

        if last_group < number_of_groups:
            new_group = last_group + 1
        else:
            new_group = 1

    survey_url = get_survey_url(survey, user_agent)[0]
    device_participant = get_survey_url(survey, user_agent)[1]

    params = {param_branching: new_group,
              param_st_enc: student_number_cipher_dec}

    if '?' in survey_url:
        redirect_url = survey_url + "&" + urllib.parse.urlencode(params)
    else:
        redirect_url = survey_url + "?" + urllib.parse.urlencode(params)

    if student_number != test_key:
        participation = Participant(
            student_number_enc=student_number_cipher_dec,
            url=redirect_url,
            device_participant=device_participant)
        participation.save()

        # update table for rotation increment
    Survey.objects.filter(survey_name=name).update(
        last_group=new_group)

    return redirect_url


def get_survey_url(survey, user_agent):
    device_participant = 'DESKTOP'
    if user_agent.is_pc or user_agent.is_tablet:
        survey_url = survey.survey_desktop_url
    else:
        if survey.survey_mobile_url != "":  # check if mobile url exists in database
            survey_url = survey.survey_mobile_url
            device_participant = 'MOBILE'
        else:
            survey_url = survey.survey_desktop_url
    return [survey_url, device_participant]


def set_language(survey, request):
    translation.activate(survey.language)
    request.LANGUAGE_CODE = translation.get_language()
