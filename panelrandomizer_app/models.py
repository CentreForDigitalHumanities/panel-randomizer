from django.db import models

# Create your models here.


class Participant(models.Model):

    """
    def __init__(self, student_number):
        self.enc_st_number = self.hash_password(student_number)

    def hash_password():
        return 'myhasged pwd'
    """

    studentnumber_enc=models.TextField(null=True,blank=True)
    studentnumber_hash=models.TextField(null=True,blank=True)
    url=models.CharField(max_length=250)
    #participation_date = models.DateTimeField('participation date')
    participation_date = models.DateTimeField(auto_now_add=True, blank=True)
    device_participant=models.CharField(max_length=250)

class Survey(models.Model):
    survey_code_desktop=models.CharField(max_length=200)
    survey_code_mobile=models.CharField(max_length=200)
    survey_name=models.CharField(max_length=200)
    number_of_goups=models.IntegerField()
    question_name_student_enc=models.CharField(max_length=200) # naam van de var die in de url moet om studentcode inte vullen




 


class Lastgroup(models.Model):
    survey_code=models.IntegerField()
    last_group=models.IntegerField()
