from django.db import models
from Cryptodome.Cipher import AES
from django.conf import settings
from Cryptodome.Util.Padding import pad, unpad
import hashlib

# Create your models here.
class Participant(models.Model):
    student_number_enc=models.CharField(unique=True,blank=True,max_length=255)
    url=models.CharField(max_length=250)
    participation_date = models.DateTimeField(auto_now_add=True, blank=True)

    DEVICE=(
        ("DESKTOP", "desktop"),
        ("TABLET", "tablet"),
        ("MOBILE", "mobile"),
    )
    device_participant=models.CharField(max_length=7, choices=DEVICE)

    def encrypt(self):

        # TODO de IV maken
        BLOCK_SIZE = 16
        key = settings.PANELRANDOMIZER_CONFIG[0]['ENCRYPTION_KEY'] 
        hashed_key=hashlib.sha256(key.encode()).digest() # geeft lengte van 32 bytes = 256 bits?
        hashed_key_half_1= hashed_key[:16]
        hashed_key_half_2= hashed_key[16:]

        #print(hashed_key)
        #print(hashed_key_half_1)
        #print(len(hashed_key_half_1))
        #rint(hashed_key_half_2)
        #print(len(hashed_key_half_2))
        #iv=os.urandom(128)


        cipher = AES.new(hashed_key_half_1, AES.MODE_CBC, 'This is an IV123'.encode()) # encode: convert all strings to byte
        student_number_cipher = cipher.encrypt( pad( self.encode(), BLOCK_SIZE ) )
        return student_number_cipher


class Survey(models.Model):
    survey_name=models.CharField(max_length=200)
    survey_desktop_url=models.CharField(max_length=200)
    survey_mobile_url=models.CharField(max_length=200)
    expected_completion_time=models.CharField(max_length=200, default='10')
    group_count=models.IntegerField()
    integration_parameter_student_enc=models.CharField(max_length=200) # naam van de var die in de url moet om studentcode inte vullen Heet eigenlijk 'parameter' in panel integration
    integration_parameter_branching=models.CharField(max_length=200,null=True,blank=True) # naam van de var in de url die alvast het groepnummer beantwoordt die questiongroup kiest
    last_group=models.IntegerField(default=0) # 
    
    def __str__(self):
        return 'naam onderzoek: {}'.format(self.survey_name)
