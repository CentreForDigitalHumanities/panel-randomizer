from django.db import models
from Cryptodome.Cipher import AES
from django.conf import settings
from base64 import b64encode
from Cryptodome.Util.Padding import pad, unpad
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
    survey_name = models.CharField(max_length=200)
    survey_desktop_url = models.CharField(max_length=200)
    survey_mobile_url = models.CharField(max_length=200)
    expected_completion_time = models.CharField(max_length=200, default='10')
    group_count = models.IntegerField()
    integration_parameter_student_enc = models.CharField(max_length=200)
    integration_parameter_branching = models.CharField(
        max_length=200, null=True, blank=True)
    last_group = models.IntegerField(default=0)

    def __str__(self):
        return 'naam onderzoek: {}'.format(self.survey_name)
