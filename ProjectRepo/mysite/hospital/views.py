from django.shortcuts import *
from django.http import *
from django.core.urlresolvers import *
from . import models, logger
from django.utils import timezone
import datetime
import re

##########################################
#	HOME VIEW
##########################################
#	Takes a request then returns a rendered version of the html template named 'index'
def home(request):
	return render(request, 'hospital/index.html', {})

##########################################
#	LOGIN VIEW
##########################################
#	Takes a request then returns a rendered version of the html template named 'login'
def login(request):
	return render(request, 'hospital/login.html', {})

##########################################
#	PATIENT REGISTER VIEW
##########################################
#	Takes a request then returns a rendered version of the html template named 'register'
def register(request):
	return render(request, 'hospital/register.html', {'hospitals':models.Hospital.objects})
	
##########################################
#	DOCTOR REGISTER 
##########################################
#	Takes a request then returns a rendered version of the html template named 'registerDoctor'
def registerDoctor(request, aid):
	return render(request, 'hospital/registerDoctor.html', {'hospitals':models.Hospital.objects, 'aid':aid})
	
##########################################
#	NURSE REGISTER 
##########################################
#	Takes a request then returns a rendered version of the html template named 'registerNurse'
def registerNurse(request, aid):
	return render(request, 'hospital/registerNurse.html', {'hospitals':models.Hospital.objects, 'aid':aid})

##########################################
#	ADMIN REGISTER 
##########################################
#	Takes a request then returns a rendered version of the html template named 'registerAdmin'
def registerAdmin(request, aid):
	return render(request, 'hospital/registerAdmin.html', {'hospitals':models.Hospital.objects, 'aid':aid})
	
##########################################
#	PATIENT INFO UPDATE VIEW
##########################################
#	Takes a request and the PatientID
#	If patient exists -> render html template 'pupdate', else present error message
def pUpdate(request, pid):
	try:
		user = models.Patient.objects.get(userName=pid)
	except models.Patient.DoesNotExist:
		return render(request, 'hospital/pupdate.html', {'error_message':"Patient does not exist",'hospitals':models.Hospital.objects, 'user':user})

	return render(request, 'hospital/pupdate.html', {'hospitals':models.Hospital.objects, 'user':user})

##########################################
#	DOCTOR INFO UPDATE VIEW
##########################################
#	Takes a request and the PatientID
#	If patient exists -> render html template 'dupdate', else present error message
def dUpdate(request, did):
	try:
		user = models.Doctor.objects.get(userName=did)
	except models.Doctor.DoesNotExist:
		return render(request, 'hospital/dupdate.html', {'error_message':"Doctor does not exist",'hospitals':models.Hospital.objects, 'user':user})

	return render(request, 'hospital/dupdate.html', {'hospitals':models.Hospital.objects, 'user':user})

##########################################
#	NUPDATE-NURSE INFO UPDATE VIEW
##########################################
def nUpdate(request, nid):
	try:
		user = models.Nurse.objects.get(userName=nid)
	except models.Nurse.DoesNotExist:
		return render(request, 'hospital/nupdate.html', {'error_message':"Nurse does not exist"})

	return render(request, 'hospital/nupdate.html', {'hospitals':models.Hospital.objects, 'user':user})

##########################################
#	LOGIN REQUEST
##########################################
#	Takes a request to log in
#	Tries each person model to log into if user and password are correct.
#	If the login is unsucessful print an error and return to same urlresolvers
#	If the login is successful, log in to the corresponding model account
def loginSubmit(request):
	try:
		user = models.Patient.objects.get(userName=request.POST['username']) #applies username to current person attempting to log in.
		if request.POST['password'] != user.password: #If the password they answer does not match on file password
			return render(request, 'hospital/login.html', {'error_message':"Password does not match"})
		logger.write(timezone.now(), user.userName, "LOGIN", " Patient "+user.userName+" logged in.")
		return HttpResponseRedirect(reverse('hospital:pinfo', kwargs={'pid':request.POST['username']})) #sends them to pinfo page
	except models.Patient.DoesNotExist:
		pass
	
	try:
		user = models.Administrator.objects.get(userName=request.POST['username'])
		if request.POST['password'] != user.password:
			return render(request, 'hospital/login.html', {'error_message':"Password does not match"})
		logger.write(timezone.now(), user.userName, "LOGIN", " Admin "+user.userName+" logged in.")
		return HttpResponseRedirect(reverse('hospital:ainfo', kwargs={'aid':request.POST['username']}))
	except models.Administrator.DoesNotExist:
		pass
	
	try:
		user = models.Doctor.objects.get(userName=request.POST['username'])
		if request.POST['password'] != user.password:
			return render(request, 'hospital/login.html', {'error_message':"Password does not match"})
		logger.write(timezone.now(), user.userName, "LOGIN", " Doctor "+user.userName+" logged in.")
		return HttpResponseRedirect(reverse('hospital:dinfo', kwargs={'did':request.POST['username']}))
	except models.Doctor.DoesNotExist:
		pass
		
	try:
		user = models.Nurse.objects.get(userName=request.POST['username'])
		if request.POST['password'] != user.password:
			return render(request, 'hospital/login.html', {'error_message':"Password does not match"})
		logger.write(timezone.now(), user.userName, "LOGIN", " Nurse "+user.userName+" logged in.")
		return HttpResponseRedirect(reverse('hospital:ninfo', kwargs={'nid':request.POST['username']}))
	except models.Nurse.DoesNotExist:
		pass
	
	return render(request, 'hospital/login.html', {'error_message':"Username not found"})

##########################################
#	ADMIN HOSPITAL DIRECTORY LIST
##########################################
#	Takes a request and admin id
#	Returns the hospital directory.
def aHospitaldir(request, aid):
	user = models.Administrator.objects.get(userName=aid)
	patients = models.Patient.objects.all()
	doctors = models.Doctor.objects.all()
	nurses = models.Nurse.objects.all()
	admins = models.Administrator.objects.all()
	return render(request, 'hospital/aHospitaldir.html', {'user':user, 'patients':patients, 'doctors':doctors, 'nurses':nurses, 'admins':admins})

##########################################
#	DOCTOR HOSPITAL DIRECTORY LIST
##########################################
#	Takes a request and doctor id
#	Returns the hospital directory.
def dHospitaldir(request, did):
	user = models.Doctor.objects.get(userName=did)
	patients = models.Patient.objects.all()
	doctors = models.Doctor.objects.all()
	nurses = models.Nurse.objects.all()
	admins = models.Administrator.objects.all()
	return render(request, 'hospital/dHospitaldir.html', {'user':user, 'patients':patients, 'doctors':doctors, 'nurses':nurses, 'admins':admins})

##########################################
#	NURSE HOSPITAL DIRECTORY LIST
##########################################
#	Takes a request and nurse id
#	Returns the hospital directory.
def nHospitaldir(request, nid):
	user = models.Nurse.objects.get(userName=nid)
	patients = models.Patient.objects.all()
	doctors = models.Doctor.objects.all()
	nurses = models.Nurse.objects.all()
	admins = models.Administrator.objects.all()
	return render(request, 'hospital/nHospitaldir.html', {'user':user, 'patients':patients, 'doctors':doctors, 'nurses':nurses, 'admins':admins})

##########################################
#	PATIENT HOSPITAL DIRECTORY LIST
##########################################
#	Takes a request and patient id
#	Returns the hospital directory.
def pHospitaldir(request, pid):
	user = models.Patient.objects.get(userName=pid)
	doctors = models.Doctor.objects.all()
	nurses = models.Nurse.objects.all()
	admins = models.Administrator.objects.all()
	return render(request, 'hospital/pHospitaldir.html', {'user':user, 'doctors':doctors, 'nurses':nurses, 'admins':admins})

##########################################
#	DOCTOR'S PATIENT LIST QUERY
##########################################
#	Takes a request and doctor ID
#	Returns the patient list at the doctor requests at url dpatientlist
def dpatientlist(request, did):
	patients = models.Patient.objects.all()
	user = models.Doctor.objects.get(userName=did)
	return render(request, 'hospital/dpatientlist.html', {'user':user,'did':did,'patients':patients})

##########################################
#	DOCTOR'S PATIENT LIST QUERY
##########################################
#	Takes a request, doctor ID, and patient ID
#	Allows the doctor to change the patient's medical information
def dpatientinfo(request, did, pid):
	try:
		user = models.Patient.objects.get(userName=pid)
	except models.Patient.DoesNotExist:
		return render(request, 'hospital/dpatientinfo.html', {'error_message':"Patient does not exist", 'hospitals':models.Hospital.objects, 'user':user, 'did':did})

	return render(request, 'hospital/dpatientinfo.html', {'hospitals':models.Hospital.objects, 'user':user, 'did':did})

def dpatientinfoSubmit(request, did, pid):
	try:
		user = models.Patient.objects.get(userName=pid)
	except models.Patient.DoesNotExist:
		return render(request, 'hospital/dpatientinfo.html', {'error_message':"Patient does not exist", 'hospitals':models.Hospital.objects, 'user':user, 'did':did})
	
	prefHosp = models.Hospital.objects.get(id=request.POST['prefferedHospital'])
	
	user.medicalInfo = request.POST['medInfo']
	user.address = request.POST['address']
	user.phoneNumber = request.POST['phoNum']
	user.email = request.POST['email']
	user.preferredHospital = prefHosp

	user.save()

	logger.write(timezone.now(), user.userName, "PATIENT INFO UPDATE", " Doctor "+did+" updated their medical info.")

	return HttpResponseRedirect(reverse('hospital:dpatientlist', args=[did]))

##########################################
#	NURSE'S PATIENT LIST QUERY
##########################################
def npatientlist(request, nid):
	patients = models.Patient.objects.all()
	user = models.Nurse.objects.get(userName=nid)
	return render(request, 'hospital/npatientlist.html', {'user':user,'nid':nid,'patients':patients})

def npatientinfo(request, nid, pid):
	try:
		user = models.Patient.objects.get(userName=pid)
	except models.Patient.DoesNotExist:
		return render(request, 'hospital/npatientinfo.html', {'error_message':"Patient does not exist", 'hospitals':models.Hospital.objects, 'user':user, 'nid':nid})

	return render(request, 'hospital/npatientinfo.html', {'hospitals':models.Hospital.objects, 'user':user, 'nid':nid})

def npatientinfoSubmit(request, nid, pid):
	try:
		user = models.Patient.objects.get(userName=pid)
	except models.Patient.DoesNotExist:
		return render(request, 'hospital/npatientinfo.html', {'error_message':"Patient does not exist", 'hospitals':models.Hospital.objects, 'user':user, 'nid':nid})
	
	prefHosp = models.Hospital.objects.get(id=request.POST['prefferedHospital'])
	
	user.medicalInfo = request.POST['medInfo']
	user.address = request.POST['address']
	user.phoneNumber = request.POST['phoNum']
	user.email = request.POST['email']
	user.preferredHospital = prefHosp

	user.save()

	logger.write(timezone.now(), user.userName, "PATIENT INFO UPDATE", " Nurse "+nid+" updated their medical info.")

	return HttpResponseRedirect(reverse('hospital:npatientlist', args=[nid]))

##########################################
#	REGISTER PATIENT
##########################################
#	Takes a request. 
#	Logic to create a patient.
#	Try to find other users with the same name for each model.
#	If same username, throw error. Else pass with success
def registerSubmit(request):
	if request.POST['password'] != request.POST['password2']:
		return render(request, 'hospital/register.html', {'error_message':"Passwords did not match",'hospitals':models.Hospital.objects})

	try:
		models.Patient.objects.get(userName=request.POST['username'])
		return render(request, 'hospital/register.html', {'error_message':"Username already exists",'hospitals':models.Hospital.objects})
	except models.Patient.DoesNotExist:
		pass
	
	try:
		models.Administrator.objects.get(userName=request.POST['username'])
		return render(request, 'hospital/register.html', {'error_message':"Username already exists",'hospitals':models.Hospital.objects})
	except models.Administrator.DoesNotExist:
		pass
		
	try:
		models.Nurse.objects.get(userName=request.POST['username'])
		return render(request, 'hospital/register.html', {'error_message':"Username already exists",'hospitals':models.Hospital.objects})
	except models.Nurse.DoesNotExist:
		pass
	
	try:
		models.Doctor.objects.get(userName=request.POST['username'])
		return render(request, 'hospital/register.html', {'error_message':"Username already exists",'hospitals':models.Hospital.objects})
	except models.Doctor.DoesNotExist:
		pass
	
	if not re.match(r"^\w+$", request.POST['username']):
		return render(request, 'hospital/register.html', {'error_message':"Username is invalid",'hospitals':models.Hospital.objects})
	
	if not request.POST['password']:
		return render(request, 'hospital/register.html', {'error_message':"Password cannot be empty",'hospitals':models.Hospital.objects})
	
	prefHosp = models.Hospital.objects.get(id=request.POST['prefferedHospital'])
	
	email = None
	if request.POST['email']:
		email = models.Email(email=request.POST['email'])
		email.save()
	
	phoneNumber = None
	if request.POST['phoNum']:
		phoneNumber = models.PhoneNumber(phoneNumber=request.POST['phoNum'])
		phoneNumber.save()
	
	user = models.Patient(
		userName = request.POST['username'],
		password = request.POST['password'],
		firstName = request.POST['fname'],
		lastName = request.POST['lname'],
		isActive = True,
		medicalInfo = request.POST['medInfo'],
		address = request.POST['address'],
		phoneNumber = phoneNumber,
		email = email,
		preferredHospital = prefHosp,
	)
	user.save()
	
	logger.write(timezone.now(), user.userName, "REGISTER", " Patient "+user.userName+" was registered.")
	
	return HttpResponseRedirect(reverse('hospital:pinfo', kwargs={'pid':request.POST['username']}))

##########################################
#	REGISTER DOCTOR 
##########################################
#	Takes a request and admin ID 
#	Logic to create a Doctor.
#	Try to find other users with the same name for each model.
#	If same username, throw error. Else pass with success
def registerDoctorSubmit(request, aid):
	if request.POST['password'] != request.POST['password2']:
		return render(request, 'hospital/registerDoctor.html', {'aid':aid, 'error_message':"Passwords did not match",'hospitals':models.Hospital.objects})
	
	try:
		models.Doctor.objects.get(userName=request.POST['username'])
		return render(request, 'hospital/registerDoctor.html', {'aid':aid, 'error_message':"Username already exists",'hospitals':models.Hospital.objects})
	except models.Doctor.DoesNotExist:
		pass
		
	try:
		models.Patient.objects.get(userName=request.POST['username'])
		return render(request, 'hospital/registerDoctor.html', {'aid':aid, 'error_message':"Username already exists",'hospitals':models.Hospital.objects})
	except models.Patient.DoesNotExist:
		pass
	
	try:
		models.Administrator.objects.get(userName=request.POST['username'])
		return render(request, 'hospital/registerDoctor.html', {'aid':aid, 'error_message':"Username already exists",'hospitals':models.Hospital.objects})
	except models.Administrator.DoesNotExist:
		pass
		
	try:
		models.Nurse.objects.get(userName=request.POST['username'])
		return render(request, 'hospital/registerDoctor.html', {'aid':aid, 'error_message':"Username already exists",'hospitals':models.Hospital.objects})
	except models.Nurse.DoesNotExist:
		pass
	
	if not re.match(r"^\w+$", request.POST['username']):
		return render(request, 'hospital/registerDoctor.html', {'aid':aid, 'error_message':"Username is invalid",'hospitals':models.Hospital.objects})
	
	if not request.POST['password']:
		return render(request, 'hospital/registerDoctor.html', {'aid':aid, 'error_message':"Password cannot be empty",'hospitals':models.Hospital.objects})
	
	worksAtHospital = models.Hospital.objects.get(id=request.POST['worksAtHospital'])
	
	user = models.Doctor(
		userName = request.POST['username'],
		password = request.POST['password'],
		firstName = request.POST['fname'],
		lastName = request.POST['lname'],
		isActive = True,
	)
	user.save()
	user.doctorList.add(worksAtHospital)
	user.save()
	
	logger.write(timezone.now(), user.userName, "REGISTER", " Doctor "+user.userName+" was registered.")
	
	return HttpResponseRedirect(reverse('hospital:ainfo', kwargs={'aid':aid}))

##########################################
#	REGISTER NURSE 
##########################################
#	Takes a request and admin ID
#	Logic to create a Nurse.
#	Try to find other users with the same name for each model.
#	If same username, throw error. Else pass with success
def registerNurseSubmit(request, aid): 
	if request.POST['password'] != request.POST['password2']:
		return render(request, 'hospital/registerNurse.html', {'aid':aid, 'error_message':"Passwords did not match",'hospitals':models.Hospital.objects})
	
	try:
		models.Doctor.objects.get(userName=request.POST['username'])
		return render(request, 'hospital/registerNurse.html', {'aid':aid, 'error_message':"Username already exists",'hospitals':models.Hospital.objects})
	except models.Doctor.DoesNotExist:
		pass
		
	try:
		models.Patient.objects.get(userName=request.POST['username'])
		return render(request, 'hospital/registerNurse.html', {'aid':aid, 'error_message':"Username already exists",'hospitals':models.Hospital.objects})
	except models.Patient.DoesNotExist:
		pass
	
	try:
		models.Administrator.objects.get(userName=request.POST['username'])
		return render(request, 'hospital/registerNurse.html', {'aid':aid, 'error_message':"Username already exists",'hospitals':models.Hospital.objects})
	except models.Administrator.DoesNotExist:
		pass
		
	try:
		models.Nurse.objects.get(userName=request.POST['username'])
		return render(request, 'hospital/registerNurse.html', {'aid':aid, 'error_message':"Username already exists",'hospitals':models.Hospital.objects})
	except models.Nurse.DoesNotExist:
		pass
		
	if not re.match(r"^\w+$", request.POST['username']):
		return render(request, 'hospital/registerNurse.html', {'aid':aid, 'error_message':"Username is invalid",'hospitals':models.Hospital.objects})
	
	if not request.POST['password']:
		return render(request, 'hospital/registerNurse.html', {'aid':aid, 'error_message':"Password cannot be empty",'hospitals':models.Hospital.objects})
	
	worksAtHospital = models.Hospital.objects.get(id=request.POST['worksAtHospital'])
	
	user = models.Nurse(
		userName = request.POST['username'],
		password = request.POST['password'],
		firstName = request.POST['fname'],
		lastName = request.POST['lname'],
		address = request.POST['address'],
		phoneNumber = request.POST['phoNum'],
		email = request.POST['email'],
		isActive = True,
		hospital = worksAtHospital,
	)
	# user.doctorList.add(worksAtHospital)
	
	user.save()
	
	logger.write(timezone.now(), user.userName, "REGISTER", " Nurse "+user.userName+" was registered.")
	
	return HttpResponseRedirect(reverse('hospital:ainfo', kwargs={'aid':aid}))

##########################################
#	REGISTER ADMINISTRATOR
##########################################
#	Takes a request and admin ID
#	Logic to create a Admin.
#	Try to find other users with the same name for each model.
#	If same username, throw error. Else pass with success
def registerAdminSubmit(request, aid):
	if request.POST['password'] != request.POST['password2']:
		return render(request, 'hospital/registerAdmin.html', {'error_message':"Passwords did not match",'hospitals':models.Hospital.objects})
	
	try:
		models.Patient.objects.get(userName=request.POST['username'])
		return render(request, 'hospital/registerAdmin.html', {'error_message':"Username already exists",'hospitals':models.Hospital.objects})
	except models.Patient.DoesNotExist:
		pass
	
	try:
		models.Administrator.objects.get(userName=request.POST['username'])
		return render(request, 'hospital/registerAdmin.html', {'error_message':"Username already exists",'hospitals':models.Hospital.objects})
	except models.Administrator.DoesNotExist:
		pass
		
	try:
		models.Nurse.objects.get(userName=request.POST['username'])
		return render(request, 'hospital/registerAdmin.html', {'error_message':"Username already exists",'hospitals':models.Hospital.objects})
	except models.Nurse.DoesNotExist:
		pass
	
	try:
		models.Doctor.objects.get(userName=request.POST['username'])
		return render(request, 'hospital/registerAdmin.html', {'error_message':"Username already exists",'hospitals':models.Hospital.objects})
	except models.Doctor.DoesNotExist:
		pass
		
	if not re.match(r"^\w+$", request.POST['username']):
		return render(request, 'hospital/registerAdmin.html', {'aid':aid, 'error_message':"Username is invalid",'hospitals':models.Hospital.objects})
	
	if not request.POST['password']:
		return render(request, 'hospital/registerAdmin.html', {'aid':aid, 'error_message':"Password cannot be empty",'hospitals':models.Hospital.objects})
	
	prefHosp = models.Hospital.objects.get(id=request.POST['prefferedHospital'])
	
	user = models.Administrator(
		userName = request.POST['username'],
		password = request.POST['password'],
		firstName = request.POST['fname'],
		lastName = request.POST['lname'],
		isActive = True,

		adminList = prefHosp,
	)
	user.save()
	
	logger.write(timezone.now(), user.userName, "REGISTER", " Administrator "+user.userName+" was registered.")
	
	return HttpResponseRedirect(reverse('hospital:ainfo', kwargs={'aid':aid}))


##########################################
#	PATIENT INFO UPDATE
##########################################
#	Takes a request and patient ID.
#	Updates a patient's information
#	Returns a rendered version of the html template of patient info
def pUpdateSubmit(request, pid):

	if request.POST['password'] != request.POST['password2']:
		return render(request, 'hospital/pupdate.html', {'error_message':"Passwords did not match"})

	try:
		user = models.Patient.objects.get(userName=pid)
	except models.Patient.DoesNotExist:
		return render(request, 'hospital/pupdate.html', {'error_message':"Patient does not exist"})

	prefHosp = models.Hospital.objects.get(id=request.POST['prefferedHospital'])

	user.password = request.POST['password']
	user.firstName = request.POST['fname']
	user.lastName = request.POST['lname']
	user.isActive = True
	user.address = request.POST['address']
	
	if request.POST['phoNum']:
		if user.phoneNumber:
			user.phoneNumber.phoneNumber = request.POST['phoNum']
			user.phoneNumber.save()
		else:
			phone = models.PhoneNumber(phoneNumber=request.POST['phoNum'])
			phone.save()
			user.phoneNumber = phone
	else:
		if user.phoneNumber:
			user.phoneNumber.delete()
			user.phoneNumber = None
	
	if request.POST['email']:
		if user.email:
			user.email.email = request.POST['email']
			user.email.save()
		else:
			email = models.Email(email=request.POST['email'])
			email.save()
			user.email = email
	else:
		if user.email:
			user.email.delete()
			user.email = None
	
	user.preferredHospital = prefHosp

	user.save()

	logger.write(timezone.now(), user.userName, "PATIENT INFO UPDATE", " Patient "+user.userName+" updated their medical info.")

	return HttpResponseRedirect(reverse('hospital:pinfo', args=[user.userName]))

##########################################
#	DOCTOR INFO UPDATE
##########################################
#	Takes a request and doctor ID.
#	Updates a doctor's information
#	Returns a rendered version of the html template of doctor info
def dUpdateSubmit(request, did):

	if request.POST['password'] != request.POST['password2']:
		return render(request, 'hospital/dupdate.html', {'error_message':"Passwords did not match"})

	try:
		user = models.Doctor.objects.get(userName=did)
	except models.Doctor.DoesNotExist:
		return render(request, 'hospital/dupdate.html', {'error_message':"Doctor does not exist"})

	user.password = request.POST['password']
	user.firstName = request.POST['fname']
	user.lastName = request.POST['lname']
	user.address = request.POST['address']
	
	if request.POST['phoNum']:
		if user.phoneNumber:
			user.phoneNumber.phoneNumber = request.POST['phoNum']
			user.phoneNumber.save()
		else:
			phone = models.PhoneNumber(phoneNumber=request.POST['phoNum'])
			phone.save()
			user.phoneNumber = phone
	else:
		if user.phoneNumber:
			user.phoneNumber.delete()
			user.phoneNumber = None
	
	if request.POST['email']:
		if user.email:
			user.email.email = request.POST['email']
			user.email.save()
		else:
			email = models.Email(email=request.POST['email'])
			email.save()
			user.email = email
	else:
		if user.email:
			user.email.delete()
			user.email = None

	user.save()

	logger.write(timezone.now(), user.userName, "DOCTOR INFO UPDATE",
				 " Doctor "+user.userName+" updated their info.")

	return HttpResponseRedirect(reverse('hospital:dinfo', args=[user.userName]))

##########################################
#	NURSE INFO UPDATE
##########################################
#	Takes a request and nurse ID.
#	Updates a nurse's information
#	Returns a rendered version of the html template of nurse info
def nUpdateSubmit(request, nid):

	if request.POST['password'] != request.POST['password2']:
		return render(request, 'hospital/nupdate.html', {'error_message':"Passwords did not match"})

	try:
		user = models.Nurse.objects.get(userName=nid)
	except models.Nurse.DoesNotExist:
		return render(request, 'hospital/nupdate.html', {'error_message':"Nurse does not exist"})

	user.password = request.POST['password']
	user.firstName = request.POST['fname']
	user.lastName = request.POST['lname']
	
	if request.POST['phoNum']:
		if user.phoneNumber:
			user.phoneNumber.phoneNumber = request.POST['phoNum']
			user.phoneNumber.save()
		else:
			phone = models.PhoneNumber(phoneNumber=request.POST['phoNum'])
			phone.save()
			user.phoneNumber = phone
	else:
		if user.phoneNumber:
			user.phoneNumber.delete()
			user.phoneNumber = None
	
	if request.POST['email']:
		if user.email:
			user.email.email = request.POST['email']
			user.email.save()
		else:
			email = models.Email(email=request.POST['email'])
			email.save()
			user.email = email
	else:
		if user.email:
			user.email.delete()
			user.email = None

	user.save()

	logger.write(timezone.now(), user.userName, "NURSE INFO UPDATE",
				 " Nurse "+user.userName+" updated their info.")

	return HttpResponseRedirect(reverse('hospital:ninfo', args=[user.userName]))
	
##########################################
#	PATIENT INFO
##########################################
#	Takes a request and patient info.
#	Returns a rendered html template of the patient info page at pinfo.html for the patient
def pinfo(request, pid):
	user = models.Patient.objects.get(userName=pid)
	return render(request, 'hospital/pinfo.html', {'user':user})

##########################################
#	ADMIN INFO
##########################################
#	Takes a request and Admin info.
#	Returns a rendered html template of the admin info page at ainfo.html for the admin
def ainfo(request, aid):
	user = models.Administrator.objects.get(userName=aid)
	return render(request, 'hospital/ainfo.html', {'user':user,'aid':aid})
	
##########################################
#	DOCTOR INFO
##########################################
#	Takes a request and doctor info.
#	Returns a rendered html template of the doctor info page at dinfo.html for the doctor
def dinfo(request, did):
	user = models.Doctor.objects.get(userName=did)
	return render(request, 'hospital/dinfo.html', {'user':user,'did':did})
	
##########################################
#	NURSE INFO
##########################################
#	Takes a request and nurse info.
#	Returns a rendered html template of the nurse info page at ninfo.html for the nurse
def ninfo(request, nid):
	user = models.Nurse.objects.get(userName=nid)
	return render(request, 'hospital/ninfo.html', {'user':user,'nid':nid})

###########################################
#	DOCTOR EDIT LAB
###########################################
def dEditLab(request, did, lab):
	lab = models.Lab.objects.get(labName=lab)
	user = models.Doctor.objects.get(userName=did)

	return render(request, 'hospital/dEditLab.html', {'user':user, 'lab':lab})

###########################################
#	DOCTOR VIEW SPECIFIC LAB
###########################################
def dViewSpecificLab(request, did, lab):
	lab = models.Lab.objects.get(labName=lab)
	user = models.Doctor.objects.get(userName=did)

	return render(request, 'hospital/dViewLabs.html', {'user':user, 'lab':lab})

###########################################
#	DOCTOR VIEW LABS
###########################################
def dViewLabs(request, did):
	user = models.Doctor.objects.get(userName=did)
	labs = models.Lab.objects.all()

	return render(request, 'hospital/dViewLabs.html', {'user':user, 'labs':labs})

###########################################
#	PATIENT VIEW LABS
###########################################
def pViewLabs(request, pid):
	user = models.Patient.objects.get(userName=pid)
	labs = models.Lab.objects.all()

	return render(request, 'hospital/pViewLabs.html', {'user':user, 'labs':labs})

##########################################
#	NEW LAB
##########################################
def dNewLab(request):
	try:
		models.Lab.objects.get(labName=request.POST['labName'])
		return render(request, 'hospital/dNewLab.html', {'error_message':"Lab already exists",'patients':models.Patient.objects.all(), 'doctors':models.Doctor.objects.all()})
	except models.Lab.DoesNotExist:
		pass

	if not re.match(r"^\w+$", request.POST['labName']):
		return render(request, 'hospital/register.html', {'error_message':"Lab Name is invalid",'patients':models.Patient.objects.all(), 'doctors':models.Doctor.objects.all()})

	if not request.POST['labName']:
		return render(request, 'hospital/register.html', {'error_message':"Lab Name cannot be empty",'patients':models.Patient.objects.all(), 'doctors':models.Doctor.objects.all()})

	if not request.POST['description']:
		return render(request, 'hospital/register.html', {'error_message':"Description cannot be empty",'patients':models.Patient.objects.all(), 'doctors':models.Doctor.objects.all()})

	lab = models.Lab(
		labName = request.POST['labName'],
		attending = request.POST['attending'],
		patient = request.POST['patient'],
		state = request.POST['state'],
		description = request.POST['description']
	)
	lab.save()

	logger.write(timezone.now(), lab.labName, "CREATION", " Lab "+lab.labName+" was created.")

	return HttpResponseRedirect(reverse('hospital:dViewLabs', kwargs={'did':request.POST['attending']}))

##########################################
#	EDIT LAB SUBMIT
##########################################
#	Takes a request and doctor ID.
#	Updates a doctor's information
#	Returns a rendered version of the html template of doctor info
def labUpdate(request, did, lab):

	lab.labName = request.POST['labName'],
	lab.attending = request.POST['attending'],
	lab.patient = request.POST['patient'],
	lab.state = request.POST['state'],
	lab.description = request.POST['description']

	lab.save()

	logger.write(timezone.now(), lab.labName, "CREATION",
				 " Lab "+lab.labName+" was updated.")

	return HttpResponseRedirect(reverse('hospital:dViewLabs', args=[did]))


##########################################
#	LOG INFO
##########################################
#	Takes a request and admin info.
#	Returns a rendered html template of the log info page at logs.html
def logs(request, aid):
	logger.write(timezone.now(), aid, "VIEW", "Admin "+aid+" viewed the system logs.")
	return render(request, 'hospital/logs.html', {'aid':aid, 'log':logger.read()})

##########################################
#	PATIENT CALENDAR
##########################################
#	Takes a request and patient 
#	Returns a render of the calendar view, template from pcal.html with the calendar type
def pcal(request,pid):
	user = models.Patient.objects.get(userName=pid)
	
	calType = 'week'
	try:
		calType = request.GET['type']
	except:
		pass
	
	date = datetime.date.today()
	try:
		date = datetime.date.fromordinal(int(request.GET['date']))
	except:
		pass
	
	inc = 1
	if calType == 'day':
		inc = 1
	elif calType == 'week':
		inc = 7
	elif calType == 'month':
		inc = 7*5
	
	dates = [date + datetime.timedelta(days=i) for i in range(inc)]
	
	return render(request, 'hospital/pcal.html', {
		'user':user,
		'caltype':calType,
		'dates':dates,
		'appts':models.Appointment.objects.filter(patientAppointment = user),
		'prevday':(date - datetime.timedelta(days=inc)).toordinal(),
		'nextday':(date + datetime.timedelta(days=inc)).toordinal(),
	})
	
###########################################
#	PATIENT ADD APPT.
###########################################
#	Takes a request, patient ID, and date
#	returns a render of the patient's appointment page at paddappt.html
def paddappt(request, pid, date):
	user = models.Patient.objects.get(userName=pid)
	
	return render(request, 'hospital/paddappt.html', {
		'user':user,
		'date':datetime.datetime.fromordinal(int(date)),
		'hospitals':models.Hospital.objects,
		'doctors':models.Doctor.objects,
	})

###########################################
#	PATIENT ADD APPOINTMENT SUBMIT 
###########################################
#	Takes a request, patient ID, and date
#	Functionality for a patient to add appointments. 
#	Also takes the start and end time to add appointments for a certain doctor at a hospital
#	Logs this action in logger service
#	Returns a redirect of the patient calendar 
def paddapptSubmit(request, pid, date):
	d = datetime.datetime.fromordinal(int(date))
	startTime = datetime.datetime.strptime(request.POST['start'], "%H:%M")
	endMins = int(request.POST['end'])
	endTime = startTime + datetime.timedelta(minutes=endMins)
	
	appt = models.Appointment(
		startTime = (datetime.datetime(day=d.day,month=d.month,year=d.year,hour=startTime.hour,minute=startTime.minute)).strftime("%Y-%m-%d %H:%M"),
		endTime = (datetime.datetime(day=d.day,month=d.month,year=d.year,hour=endTime.hour,minute=endTime.minute)).strftime("%Y-%m-%d %H:%M"),
		atHospital = models.Hospital.objects.get(id=request.POST['hospital']),
		patientAppointment = models.Patient.objects.get(userName=pid),
		doctorAppointment = models.Doctor.objects.get(id=request.POST['doctor']),
		notes=request.POST['notes'],
	)
	appt.save()
	
	logger.write(timezone.now(), pid, "APPT", " Patient "+pid+" added a new appointment with "+appt.doctorAppointment.userName)
	
	return HttpResponseRedirect(reverse('hospital:pcal', args=[pid]))
	
###########################################
#	PATIENT EDIT APPT.
###########################################
#	Takes a request, patient ID, and appointment
#	Edits a patient appointment invoked by a patient
#	Return a render of the url template peditappt.html
def peditappt(request, pid, appt):
	user = models.Patient.objects.get(userName=pid)
	a = models.Appointment.objects.get(id=appt)
	
	return render(request, 'hospital/peditappt.html', {
		'user':user,
		'appt':a,
		'hospitals':models.Hospital.objects,
		'doctors':models.Doctor.objects,
		'date':a.startTime.strftime("%Y-%m-%d"),
		'startTime':a.startTime.strftime("%H:%M"),
		'endTime':a.endTime.strftime("%H:%M"),
		'delta':(a.endTime-a.startTime).seconds/60,
	})

###########################################
#	PATIENT EDIT APPT. SUBMIT
###########################################
#	Takes a request, patient ID, and appointment
#	Saves a patient appointment edit invoked by a patient
#	Return a redirect of the patient calendar
def peditapptSubmit(request, pid, appt):
	user = models.Patient.objects.get(userName=pid)
	a = models.Appointment.objects.get(id=appt)
	
	date = datetime.datetime.strptime(request.POST['date'], "%Y-%m-%d")
	start = datetime.datetime.strptime(request.POST['start'], "%H:%M")
	endMins = int(request.POST['end'])
	end = start + datetime.timedelta(minutes=endMins)
	
	a.startTime = datetime.datetime(day=date.day,month=date.month,year=date.year,hour=start.hour,minute=start.minute)
	a.endTime = datetime.datetime(day=date.day,month=date.month,year=date.year,hour=end.hour,minute=end.minute)
	a.notes = request.POST['notes']
	a.atHospital = models.Hospital.objects.get(id=request.POST['hospital'])
	a.doctorAppointment = models.Doctor.objects.get(id=request.POST['doctor'])
	
	a.save()
	
	logger.write(timezone.now(), user.userName, "APPT", " Patient "+user.userName+" edited their appointment with "+a.doctorAppointment.userName)
	
	return HttpResponseRedirect(reverse('hospital:pcal', args=[pid]))
	
###########################################
#	PATIENT CANCEL APPT.
###########################################
#	Takes a request, patient ID, and appointment
#	Cancels an appointment, from the invoking patient
#	Deletes the appointment object
#	Returns the patients calendar view
def pcancelappt(request, pid, appt):
	user = models.Patient.objects.get(userName=pid)
	a = models.Appointment.objects.get(id=appt)
	
	logger.write(timezone.now(), user.userName, "APPT", " Patient "+user.userName+" cancelled their appointment with "+a.doctorAppointment.userName)
	
	a.delete()
	
	return HttpResponseRedirect(reverse('hospital:pcal', args=[pid]))

###########################################
#	DOCTOR CALENDAR
###########################################
#	Takes a request and a doctor ID
#	Returns a doctor's view for the calendar at hospital/dcal.html
def dcal(request,did):
	user = models.Doctor.objects.get(userName=did)
	
	calType = 'week'
	try:
		calType = request.GET['type']
	except:
		pass

	date = datetime.date.today()
	try:
		date = datetime.date.fromordinal(int(request.GET['date']))
	except:
		pass

	inc = 1
	if calType == 'day':
		inc = 1
	elif calType == 'week':
		inc = 7
	elif calType == 'month':
		inc = 7*5

	dates = [date + datetime.timedelta(days=i) for i in range(inc)]
		
	return render(request, 'hospital/dcal.html', {
		'user':user,
		'caltype':calType,
		'dates':dates,
		'appts':models.Appointment.objects.filter(doctorAppointment = user),
		'prevday':(date - datetime.timedelta(days=inc)).toordinal(),
		'nextday':(date + datetime.timedelta(days=inc)).toordinal(),
	})
	
#################################################
#	DOCTOR ADD APPT
#################################################
#	Takes a request, doctor ID, and date
#	Adds appointments from the doctor view
#	Return a render of the hospital/daddappt.html template for adding appointments
def daddappt(request, did, date):
	user = models.Doctor.objects.get(userName=did)
	
	return render(request, 'hospital/daddappt.html', {
		'user':user,
		'date':datetime.datetime.fromordinal(int(date)),
		'hospitals':models.Hospital.objects,
		'patients':models.Patient.objects,
	})
	
#################################################
#	DOCTOR ADD APPT SUBMIT
#################################################
#	Takes request, doctor ID, and date
#	Logic for creating an appointment with starting time and ending time of an appointment for an appointment model.
#	Return the doctor view for calendar
def daddapptSubmit(request, did, date):
	d = datetime.datetime.fromordinal(int(date))
	startTime = datetime.datetime.strptime(request.POST['start'], "%H:%M")
	endMins = int(request.POST['end'])
	endTime = startTime + datetime.timedelta(minutes=endMins)
	
	appt = models.Appointment(
		startTime = (datetime.datetime(day=d.day,month=d.month,year=d.year,hour=startTime.hour,minute=startTime.minute)).strftime("%Y-%m-%d %H:%M"),
		endTime = (datetime.datetime(day=d.day,month=d.month,year=d.year,hour=endTime.hour,minute=endTime.minute)).strftime("%Y-%m-%d %H:%M"),
		atHospital = models.Hospital.objects.get(id=request.POST['hospital']),
		doctorAppointment = models.Doctor.objects.get(userName=did),
		patientAppointment = models.Patient.objects.get(id=request.POST['patient']),
		notes=request.POST['notes'],
	)
	appt.save()
	
	logger.write(timezone.now(), did, "APPT", " Doctor "+did+" added a new appointment with "+appt.patientAppointment.userName)
	
	return HttpResponseRedirect(reverse('hospital:dcal', args=[did]))
	
###########################################
#	DOCTOR EDIT APPT.
###########################################
#	Takes a request, doctor ID, and appointment 
#	Edits an appointment from the invoking doctor
#	Return the deditappt.html template for the doctors appointment view
def deditappt(request, did, appt):
	user = models.Doctor.objects.get(userName=did)
	a = models.Appointment.objects.get(id=appt)
	
	return render(request, 'hospital/deditappt.html', {
		'user':user,
		'appt':a,
		'hospitals':models.Hospital.objects,
		'patients':models.Patient.objects,
		'date':a.startTime.strftime("%Y-%m-%d"),
		'startTime':a.startTime.strftime("%H:%M"),
		'endTime':a.endTime.strftime("%H:%M"),
		'delta':(a.endTime-a.startTime).seconds/60,
	})

###########################################
#	DOCTOR EDIT APPT. SUBMIT
###########################################
#	Takes a request, doctor ID, and appointment 
#	Edits an appointment from the invoking doctor
#	Return the deditappt.html template for the doctors appointment view
def deditapptSubmit(request, did, appt):
	user = models.Doctor.objects.get(userName=did)
	a = models.Appointment.objects.get(id=appt)
	
	date = datetime.datetime.strptime(request.POST['date'], "%Y-%m-%d")
	start = datetime.datetime.strptime(request.POST['start'], "%H:%M")
	endMins = int(request.POST['end'])
	end = start + datetime.timedelta(minutes=endMins)
	
	a.startTime = datetime.datetime(day=date.day,month=date.month,year=date.year,hour=start.hour,minute=start.minute)
	a.endTime = datetime.datetime(day=date.day,month=date.month,year=date.year,hour=end.hour,minute=end.minute)
	a.notes = request.POST['notes']
	a.atHospital = models.Hospital.objects.get(id=request.POST['hospital'])
	a.patientAppointment = models.Patient.objects.get(id=request.POST['patient'])
	
	a.save()
	
	logger.write(timezone.now(), user.userName, "APPT", " Doctor "+user.userName+" edited their appointment with "+a.patientAppointment.userName)
	
	return HttpResponseRedirect(reverse('hospital:dcal', args=[did]))
	
###########################################
#	DOCTOR CANCEL APPT.
###########################################
#	Takes a request, doctor ID, appointment ID
#	Cancels an appointment from the doctor's schedule
#	Returns the doctor's calendar view

def dcancelappt(request, did, appt):
	user = models.Doctor.objects.get(userName=did)
	a = models.Appointment.objects.get(id=appt)
	
	logger.write(timezone.now(), user.userName, "APPT", " Doctor "+user.userName+" cancelled their appointment with "+a.patientAppointment.userName)
	
	a.delete()
	
	return HttpResponseRedirect(reverse('hospital:dcal', args=[did]))

##########################################
#	NURSE CALENDAR
##########################################
#	Takes a request, nurse ID
#	Show the nurse calendar view
#	Returns the nurse's calendar view with spec of day,week, or month
def ncal(request, nid):
	user = models.Nurse.objects.get(userName=nid)
	
	caltype = 'week'
	try:
		caltype = request.GET['type']
	except:
		pass
	
	date = datetime.date.today()
	try:
		date = datetime.date.fromordinal(int(request.GET['date']))
	except:
		pass
	
	inc = 1
	if caltype == 'day':
		inc = 1
	elif caltype == 'week':
		inc = 7
	elif caltype == 'month':
		inc = 7*5
	
	dates = [date + datetime.timedelta(days=i) for i in range(inc)]
	
	return render(request, 'hospital/ncal.html', {
		'user':user,
		'caltype':caltype,
		'dates':dates,
		'appts':models.Appointment.objects.filter(atHospital = user.hospital),
		'prevday':(date - datetime.timedelta(days=inc)).toordinal(),
		'nextday':(date + datetime.timedelta(days=inc)).toordinal(),
	})

#################################################
#	NURSE ADD APPT
#################################################
#	Takes a request, nurse ID, and date
#	Allows nurses to add appointments
#	Returns the add appointment view for nurse
def naddappt(request, nid, date):
	user = models.Nurse.objects.get(userName=nid)
	
	return render(request, 'hospital/naddappt.html', {
		'user':user,
		'date':datetime.datetime.fromordinal(int(date)),
		'hospitals':models.Hospital.objects,
		'patients':models.Patient.objects,
		'doctors':models.Doctor.objects,
	})

###########################################
#	NURSE ADD APPT. SUBMIT
###########################################
#	Takes a request, nurse ID, and date
#	submits the request for a nurse to add an appointment
#	Returns the nurse's calendar
def naddapptSubmit(request, nid, date):
	d = datetime.datetime.fromordinal(int(date))
	startTime = datetime.datetime.strptime(request.POST['start'], "%H:%M")
	endMins = int(request.POST['end'])
	endTime = startTime + datetime.timedelta(minutes=endMins)
	
	appt = models.Appointment(
		startTime = (datetime.datetime(day=d.day,month=d.month,year=d.year,hour=startTime.hour,minute=startTime.minute)).strftime("%Y-%m-%d %H:%M"),
		endTime = (datetime.datetime(day=d.day,month=d.month,year=d.year,hour=endTime.hour,minute=endTime.minute)).strftime("%Y-%m-%d %H:%M"),
		atHospital = models.Hospital.objects.get(id=request.POST['hospital']),
		doctorAppointment = models.Doctor.objects.get(id=request.POST['doctor']),
		patientAppointment = models.Patient.objects.get(id=request.POST['patient']),
		notes=request.POST['notes'],
	)
	appt.save()
	
	return HttpResponseRedirect(reverse('hospital:ncal', args=[nid]))
	
###########################################
#	NURSE EDIT APPT.
###########################################
#	Takes a request, nurse iD, and appointment
#	Functionality for nurses to edit a specific appointment
#	Returns nurse edit appointment view
def neditappt(request, nid, appt):
	user = models.Nurse.objects.get(userName=nid)
	a = models.Appointment.objects.get(id=appt)
	
	return render(request, 'hospital/neditappt.html', {
		'user':user,
		'appt':a,
		'hospitals':models.Hospital.objects,
		'patients':models.Patient.objects,
		'doctors':models.Doctor.objects,
		'date':a.startTime.strftime("%Y-%m-%d"),
		'startTime':a.startTime.strftime("%H:%M"),
		'endTime':a.endTime.strftime("%H:%M"),
		'delta':(a.endTime-a.startTime).seconds/60,
	})

###########################################
#	NURSE EDIT APPT. SUBMIT
###########################################
#	Takes a request, nurse ID, and appointment
#	Submits request for nurses to edit a specific appointment
#	Returns nurse whole calendar view 

def neditapptSubmit(request, nid, appt):
	user = models.Nurse.objects.get(userName=nid)
	a = models.Appointment.objects.get(id=appt)
	
	date = datetime.datetime.strptime(request.POST['date'], "%Y-%m-%d")
	start = datetime.datetime.strptime(request.POST['start'], "%H:%M")
	endMins = int(request.POST['end'])
	end = start + datetime.timedelta(minutes=endMins)
	
	a.startTime = datetime.datetime(day=date.day,month=date.month,year=date.year,hour=start.hour,minute=start.minute)
	a.endTime = datetime.datetime(day=date.day,month=date.month,year=date.year,hour=end.hour,minute=end.minute)
	a.notes = request.POST['notes']
	a.atHospital = models.Hospital.objects.get(id=request.POST['hospital'])
	a.patientAppointment = models.Patient.objects.get(id=request.POST['patient'])
	a.doctorAppointment = models.Doctor.objects.get(id=request.POST['doctor'])
	
	a.save()
	
	logger.write(timezone.now(), user.userName, "APPT", " Nurse "+user.userName+" edited an appointment with "+a.patientAppointment.userName)
	
	return HttpResponseRedirect(reverse('hospital:ncal', args=[nid]))
	
###########################################
#	NURSE CANCEL APPT.
###########################################
#	Takes a request, nurse ID, and appointment
#	Functionality for nurses to cancel a specific appointment
#	Returns nurse whole calendar view on success

def ncancelappt(request, nid, appt):
	user = models.Nurse.objects.get(userName=nid)
	a = models.Appointment.objects.get(id=appt)
	
	logger.write(timezone.now(), user.userName, "APPT", " Nurse "+user.userName+" cancelled an appointment with "+a.patientAppointment.userName)
	
	a.delete()
	
	return HttpResponseRedirect(reverse('hospital:ncal', args=[nid]))