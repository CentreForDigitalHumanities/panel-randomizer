# Panel Randomizer #

Panel Randomizer is a Python/Django application to create URLs that forward to a specified Lime Survey questionaire

* The respondent fills out his/her ID, which is saved AES encoded in the database.
* Respondents are only forwarded the first time to a questionaire. If the respondents ID is found, the respondent is redirected to a screenout. 
* The resulting forwarding URL contains two GET variables that can be used to prefill questions in the Lime Survey questionaire.
	*  Respondent ID. The key can be named randomly in the admin
	*  Routing. The key van be named randomly in the admin. The value in the URL is a rotating number, which runs from 1 to the limit value that is defined in the admin. Using this as a pre-answered value, a group of questions can be shown in Lime Survey using Lime Surveys so called 'relevance equatation'

###Prerequisites ###
Python > 3.0 <br>
Django > 2.0<br>


###Next steps###

Download or clone from GitHub


