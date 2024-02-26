from django.db import models
from django import forms
from django.utils import timezone
from django.core.validators import RegexValidator

###########################################
#	Phone Class that's just for a field
###########################################
#	regVal = Validator ensuring only numbers, 9 - 15 characters in length
#	phoneNumber = the actual number, having been validated
class PhoneNumber(models.Model):
    regVal = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Please enter as '+##########'")
    phoneNumber = models.CharField(max_length=15, validators=[regVal], null=True, blank=True) 
	
##########################################
#	Email Class that's just for a field
##########################################
#	regVal = Validator ensuring valid email
#	email = the actual email
class Email(models.Model):
	regVal = RegexValidator(regex=r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$', message="Emails are case-insensitive")
	email = models.CharField(max_length=50, validators=[regVal], null=True, blank=True)

##########################################
#   PERSON CLASS/MODEL
##########################################
#	firstname = first name of Person, up to 30 characters
#	lastname = last name of Person, up to 30 characters
#	username = login/username of Person, up to 20 characters
#	password = login password, up to 20 characters
#	isActive = True is Person is active at the hospital, False if they are discharged, or no longer work there.
class Person(models.Model):
	firstName = models.CharField(max_length=30, null=True, blank=True)
	lastName = models.CharField(max_length=30, null=True, blank=True)
	userName = models.CharField(max_length=20)
	password = models.CharField(max_length=20)
	isActive = models.BooleanField()
	address = models.CharField(max_length=75, null=True, blank=True)
	phoneNumber = models.ForeignKey(PhoneNumber, null=True, blank=True)
	email = models.ForeignKey(Email, null=True, blank=True)
	#TODO2 inbox
	#TODO2 outbox


    # STR FUNCTION ::: for returning firstname
	def __str__(self):
		return self.userName

	# def sendMessage(toWhom)

##########################################
#   PATIENT CLASS/MODEL
##########################################
#	preferredHospital = name of the hospital in charfield
#	medicalInfo = Medical Information provided in form, up to 500 characters
#	contactInfo = Contact Information provided in form, up to 200 characters
class Patient(Person):
	preferredHospital = models.ForeignKey(
		'Hospital',
		on_delete = models.CASCADE,
		
	)
	medicalInfo = models.CharField(max_length=500, null=True, blank=True)
	#appointment is a many to one relation from appt to patient
	#TODO2: labResults

	#TODO2: admissions
	#TODO2: images
	
##########################################
#   PRESCRIPTION CLASS/MODEL
##########################################
#	drug = the name of the drug
#	dosage = the dosage for this drug, up to 10 chars ( eg 10mg)
#	prescribedFrom = the doctor that prescribed this. many prescriptions to one doctor
#	prescribedFor = many prescriptions belong to one patient
#	prescribedOn = date prescription opens
#	prescribedUntil = date prescription endswith
class Prescription(models.Model):
	drug = models.ForeignKey(
	'Drug',
	on_delete = models.CASCADE,
	)
	
	dosage = models.CharField(max_length = 20)
	#many prescriptions for a patient
	prescribedFor = models.ForeignKey(
	'Patient',
	on_delete = models.CASCADE,
	)
	
	#many prescriptions to one doctor
	prescribedFrom = models.ForeignKey(
	'Doctor',
	on_delete = models.CASCADE,
	)
	
	prescribedOn = models.DateTimeField
	prescribedUntil = models.DateTimeField
	
	# STR FUNCTION ::: for returning info
	def __str__(self):
		return self.drug.name + " " + self.dosage

##########################################
#   DRUG CLASS/MODEL
##########################################
#	name = the name
class Drug(models.Model):
	name = models.CharField(max_length = 70)
	
	# STR FUNCTION ::: for returning info
	def __str__(self):
		return self.name

##########################################
#   LAB CLASS
##########################################
class Lab(models.Model):
	labName = models.CharField(max_length=50, null=True, blank=True)
	attending = models.ForeignKey(
		'Doctor',
		on_delete = models.CASCADE,
	)
	patient = models.ForeignKey(
		'Patient',
		on_delete = models.CASCADE,
	)
	state = forms.ChoiceField(choices=[(z, z) for z in ("Pending", "Completed")])
	description = models.CharField(max_length=500, null=True, blank=True)

	# STR FUNCTION ::: for returning labName
	def __str__(self):
		return self.labName

##########################################
#   NURSE CLASS/MODEL
##########################################
#	hospital = many nurses correspond to one hospital
class Nurse(Person):
	hospital = models.ForeignKey(
		'Hospital',
		on_delete = models.CASCADE,
	)


##########################################
#   DOCTOR CLASS/MODEL
##########################################
#	doctorList = many doctors to many hospital
class Doctor(Person):
	doctorList = models.ManyToManyField('Hospital')

	#TODO2 addPrescription
	#TODO2 removePrescription


##########################################
#   ADMINISTRATOR CLASS/MODEL
##########################################
#	adminList = contains the list of admins for a hospital
class Administrator(Person):
	
	#many admins to one hospital
	adminList = models.ForeignKey(
		'Hospital',
		on_delete = models.CASCADE,
		
	)
		
##########################################
#   APPOINTMENT CLASS/MODEL
##########################################
#	Doctor = Doctor name
#	Patient = Patient name
#	time = time of the appointment
#	atHospital = Hospital at which the appointment takes place
#	notes = Possibly notes about the appointment, up to 500 characters
#	patientAppointment = contains appointments for a patient
#	doctorAppointment = contains appointments for a doctor
class Appointment(models.Model):
	
	startTime = models.DateTimeField('Start time')
	endTime = models.DateTimeField('End time')
	atHospital = models.ForeignKey(
	'Hospital',
	on_delete = models.CASCADE,
	)
	
	notes = models.CharField(max_length=500)
	
	#many appts to one patient	
	patientAppointment = models.ForeignKey(
		'Patient',
		on_delete = models.CASCADE,
	)
		
	#many appts to one doctor
	doctorAppointment = models.ForeignKey(
		'Doctor',
		on_delete = models.CASCADE,
	)
	# STR FUNCTION ::: for returning time
	def __str__(self):
		return str(self.startTime) + " to " + str(self.endTime)
	

##########################################
#   HOSPITAL CLASS/MODEL
##########################################
#	name = name of the hospital
class Hospital(models.Model):
	name = models.CharField(max_length = 200)

	# STR FUNCTION ::: for returning hospitalname
	def __str__(self):
		return self.name

##########################################
#   ADMISSION CLASS/MODEL
##########################################
#	patient = the patient involved
#	hospital = the hospital discharged at
#	admitted = The time the patient was admitted
class Admission(models.Model):
	patient = models.ForeignKey(
		'Patient',
		on_delete = models.CASCADE,
	)
	hospital = models.ForeignKey(
		'Hospital',
		on_delete = models.CASCADE,
	)
	admitted = models.DateTimeField('Time Admitted')
	
	# STR FUNCTION ::: for returning info
	def __str__(self):
		return self.patient.userName + "'s admission (id " + str(self.id) + ")"