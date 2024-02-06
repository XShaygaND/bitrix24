# Bitrix24

This project is a handler for saving deal details to the database and posting them to Google Sheets

##
The project was designed for a job interview, so in case of seeing a few flaws, it was a matter of time

## Running the project
Install required packages

	pip install -r requirements.txt

Clone project to your computer

	git clone https://github.com/XShaygaND/bitrix24.git

Migrate project

	python manage.py migrate
		
Run the server on your localhost

	python manage.py runserver