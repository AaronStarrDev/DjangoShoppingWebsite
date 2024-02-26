===========================================================================
AMAZING GROUP 4 SWEN 261 README
1. INSTALLATION
2. KNOWN BUGS AND DISCLAIMERS
3. KNOWN MISSING RELEASE-1 FEATURES
4. LOGIN ACCOUNTS
===========================================================================
1) Installation:  

1.	If receiving folder is zipped, unzip folder into desired directory to keep files.
2.	Open command prompt and navigate to directory of the ‘mysite’ folder that contains the manage.py file, mysite folder 
3.	Run the command:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py runserver
4.	Enter the following in the internet browser address bar:
	http://127.0.0.1:8000/
5.	Log on with an account in Section 4
6.	Enjoy


===========================================================================
2) Known bugs and disclaimers.
Refer to the Test plan document for more.
Some bugs may overlap with the test plan document:

- Nurses produced by the admin user will result in a crash
- Doctors produced by the admin user will result in that doctor having no primary hospital
- Appointments can be scheduled at any time, no restrictions
- Usernames can be created with whitespaces, but will cause a crash
- Fill in all fields on every page or the system may crash


===========================================================================
3) Known missing Release-x features

USE CASE 2:		SOME FUNCTIONALITY
				Administrators can be added by other administrators,
				Doctors can be added, but have no hospital
				Nurses cannot be added (Recent build broke nurse additions)
				
USE CASE 3:		NEED ADD EXCEPTION HANDLING
				Patients can currently update their own medical information
				
USE CASE 6:		NEED ADD EXCEPTION HANDLING
				Appointments can be currently made even if the doctor/patient is busy
				
USE CASE 9:		TO BE INCLUDED IN R2
				Currently, no prescriptions

USE CASE 10:	SOME FUNCTIONALITY
				Employees can view patient information but prescriptions, and test results not yet implemented

USE CASE 13:	TO BE INCLUDED IN R2
				Currently no admissions

USE CASE 15:	TO BE INCLUDED IN R2

USE CASE 16: 	TO BE INCLUDED IN R2

===========================================================================
4) Basic execution and usage instructions (logins & passwords)
Log into the Django Admin portal:
USERNAME: admin
PASSWORD: hospital


For our actual website and not the django admin:

USERNAME: admin
PASSWORD: admin

For a patient, use:

USERNAME: test
PASSWORD: pass

USERNAME: john
PASSWORD: password

USERNAME: dxf7606
PASSWORD: password

Doctor:

USERNAME: bible
PASSWORD: test

USERNAME: doc
PASSWORD: pass

NURSE:

USERNAME: joy
PASSWORD: pokemon

USERNAME: throws
PASSWORD: hard

===========================================================================