from django.db import models
from Cryptodome.Cipher import AES
from django.conf import settings
from base64 import b64encode
from Cryptodome.Hash import HMAC, SHA256


class Participant(models.Model):
    student_number_enc = models.CharField(
        unique=True, blank=True, max_length=255)
    url = models.CharField(max_length=250)
    participation_date = models.DateTimeField(auto_now_add=True, blank=True)

    DEVICE = (
        ("DESKTOP", "desktop"),
        ("TABLET", "tablet"),
        ("MOBILE", "mobile"),
    )
    device_participant = models.CharField(max_length=7, choices=DEVICE)

    @staticmethod
    def encode(aes_secret: bytes, hmac_secret: bytes, text: str) -> str:

        # Deterministically encodes a text.
        iv = HMAC.new(hmac_secret, text.encode(), digestmod=SHA256).digest()
        cipher = AES.new(aes_secret, AES.MODE_CFB, iv=iv[:16])
        ct_bytes = cipher.encrypt(text.encode())
        return b64encode(ct_bytes).decode('utf-8')


class Survey(models.Model):

    survey_name = models.CharField(
        max_length=200,
        help_text='Will be shown to respondents and is used for creating the URL for this survey.')
    survey_desktop_url = models.CharField(
        max_length=200,
        help_text='Copy from LimeSurvey')
    survey_mobile_url = models.CharField(
        max_length=200,
        blank=True,
        default='',
        help_text='Optional. Copy from LimeSurvey')
    language = models.CharField(
        max_length=5,
        choices=(
            ('nl-NL', 'Dutch'),
            ('en-GB', 'English')
        ),
        default='en-GB'
    )

    welcome_text = models.TextField(
        default='',
        help_text='This text is shown when the user enters the survey.')
    screen_out_text = models.TextField(
        default='',
        verbose_name='Screen-out text',
        help_text='This text is shown when the participant has already participated in another survey and is not allowed to participate.')
    group_count = models.PositiveIntegerField(
        help_text='The number of groups you wish to rotate')
    # Name of the query string parameter containing the encoded student number for identification.
    # This the "parameter" in the Panel Integration of LimeSurvey.
    integration_parameter_student_enc = models.CharField(
        max_length=200,
        verbose_name="Student number parameter",
        help_text='The same value should be set in LimeSurvey\'s Panel Integration')
    # Name of the query string parameter containing the group number to use for branching
    integration_parameter_branching = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Branching parameter",
        help_text='Optional. The same value should be set in LimeSurvey\'s Panel Integration')
    last_group = models.IntegerField(default=0)

    def __str__(self):
        return self.survey_name
