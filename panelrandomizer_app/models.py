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
    survey_name=models.CharField(max_length=200)
    survey_code_desktop=models.CharField(max_length=200) 
    # dit misschien als many to one in ander object om meerdere codes te kunnen toevoegen? en dan veld user_agent (desktop of mobile) erbij
    survey_code_mobile=models.CharField(max_length=200)
    expected_completion_time=models.CharField(max_length=200, default='10')
    number_of_groups=models.IntegerField()
    integration_parameter_student_enc=models.CharField(max_length=200) # naam van de var die in de url moet om studentcode inte vullen Heet eigenlijk 'parameter' in panel integration
    integration_parameter_branching=models.CharField(max_length=200,null=True,blank=True) # naam van de var in de url die alvast het groepnummer beantwoordt die questiongroup kiest
    last_group=models.IntegerField(default=0) # 
    
    def __str__(self):
        return 'naam onderzoek: {}'.format(self.survey_name)



class Lastgroup(models.Model):
    survey_code=models.IntegerField()
    last_group=models.IntegerField()
