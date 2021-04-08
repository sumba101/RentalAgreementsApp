### Rental agreement Django Web App

#### How to run
* First set up virtual environment using the requirements.txt
* `cd django_mockup` and then run command 'python3 manage.py runserver'

#### To Sagar
look at this file in path `django_mockup/sub_app/template_processor.py`
This file contains the function that receives the map of the values taken by the form
You can use this to fill in the rental agreement template using moustache or something
After that we can save it in path `"./RentalAgreementsData/RentalAgreementTextFiles/rental.txt"`
We can then convert the .txt to a .pdf using the code present in `pdfConverter.py`