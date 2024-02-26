from django.conf.urls import url
from . import views

app_name = 'hospital'

##########################################
#   URL PATTERN BLOCK
##########################################
# Creates the views of a webpage based on te views.py file. 
# The webpage has separate urls for the following:
urlpatterns = [
    ### Home page information
	url(r'^$', views.home, name='home'),
	url(r'^login$', views.login, name='login'),
	url(r'^login/submit$', views.loginSubmit, name='loginSubmit'),

	### Register patient webpages
	url(r'^register$', views.register, name='register'),
	url(r'^register/submit$', views.registerSubmit, name='registerSubmit'),

	### Register doctor webpages
	url(r'^register/registerDoctor/(?P<aid>\w+)$', views.registerDoctor, name='registerDoctor'),
	url(r'^register/registerDoctorSubmit/(?P<aid>\w+)$', views.registerDoctorSubmit, name='registerDoctorSubmit'),

	### Register nurse webpages
	url(r'^register/registerNurse/(?P<aid>\w+)$', views.registerNurse, name='registerNurse'),
	url(r'^register/registerNurseSubmit/(?P<aid>\w+)$', views.registerNurseSubmit, name='registerNurseSubmit'),

	### Register admin webpages
	url(r'^register/registerAdmin/(?P<aid>\w+)$', views.registerAdmin, name='registerAdmin'),
	url(r'^register/registerAdminSubmit/(?P<aid>\w+)$', views.registerAdminSubmit, name='registerAdminSubmit'),

	### patient, admin, doctor, and nurse info pages
	url(r'^pinfo/(?P<pid>\w+)$', views.pinfo, name='pinfo'),	
	url(r'^ainfo/(?P<aid>\w+)$', views.ainfo, name='ainfo'),
	url(r'^dinfo/(?P<did>\w+)$', views.dinfo, name='dinfo'),
	url(r'^ninfo/(?P<nid>\w+)$', views.ninfo, name='ninfo'),

    ### Log page
	url(r'^logs/(?P<aid>\w+)$', views.logs, name='logs'),

    ### Patient and doctor update pages
	url(r'^pupdate/(?P<pid>\w+)$', views.pUpdate, name='pupdate'),
    url(r'^dupdate/(?P<did>\w+)$', views.dUpdate, name='dupdate'),

    ### Update submissions
	url(r'^nupdate/(?P<nid>\w+)$', views.nUpdate, name='nupdate'),
	url(r'^pupdatesubmit/(?P<pid>\w+)$', views.pUpdateSubmit, name='pupdatesubmit'),
    url(r'^dupdatesubmit/(?P<did>\w+)$', views.dUpdateSubmit, name='dupdatesubmit'),
	url(r'^nupdatesubmit/(?P<nid>\w+)$', views.nUpdateSubmit, name='nupdatesubmit'),

    ### Patient list informations
    url(r'^dpatientlist/(?P<did>\w+)$', views.dpatientlist, name='dpatientlist'),
	url(r'^dpatientinfo/(?P<did>\w+)/(?P<pid>\w+)$', views.dpatientinfo, name='dpatientinfo'),
	url(r'^dpatientinfo/(?P<did>\w+)/(?P<pid>\w+)/submit$', views.dpatientinfoSubmit, name='dpatientinfoSumbit'),

	### Calendar pages
	url(r'^pcal/(?P<pid>\w+)$', views.pcal, name='pcal'),
    url(r'^dcal/(?P<did>\w+)$', views.dcal, name='dcal'),
	url(r'^ncal/(?P<nid>\w+)$', views.ncal, name='ncal'),

	### Patient appointment info
	url(r'^paddappt/(?P<pid>\w+)/(?P<date>\d+)$', views.paddappt, name='paddappt'),
	url(r'^paddappt/(?P<pid>\w+)/(?P<date>\d+)/submit$', views.paddapptSubmit, name='paddapptSubmit'),

    ### Patient edit appointment info
	url(r'^peditappt/(?P<pid>\w+)/(?P<appt>\d+)$', views.peditappt, name='peditappt'),
	url(r'^peditappt/(?P<pid>\w+)/(?P<appt>\d+)/submit$', views.peditapptSubmit, name='peditapptSubmit'),
	url(r'^pcancelappt/(?P<pid>\w+)/(?P<appt>\d+)$', views.pcancelappt, name='pcancelappt'),

	### Doctor appointment info
	url(r'^daddappt/(?P<did>\w+)/(?P<date>\d+)$', views.daddappt, name='daddappt'),
	url(r'^daddappt/(?P<did>\w+)/(?P<date>\d+)/submit$', views.daddapptSubmit, name='daddapptSubmit'),

	### Doctor edit appointment info
	url(r'^deditappt/(?P<did>\w+)/(?P<appt>\d+)$', views.deditappt, name='deditappt'),
	url(r'^deditappt/(?P<did>\w+)/(?P<appt>\d+)/submit$', views.deditapptSubmit, name='deditapptSubmit'),
	url(r'^dcancelappt/(?P<did>\w+)/(?P<appt>\d+)$', views.dcancelappt, name='dcancelappt'),

    ### Nurse edit appointment info
	url(r'^naddappt/(?P<nid>\w+)/(?P<date>\d+)$', views.naddappt, name='naddappt'),
	url(r'^naddappt/(?P<nid>\w+)/(?P<date>\d+)/submit$', views.naddapptSubmit, name='naddapptSubmit'),

	### Nurse edit appointment info
	url(r'^neditappt/(?P<nid>\w+)/(?P<appt>\d+)$', views.neditappt, name='neditappt'),
	url(r'^neditappt/(?P<nid>\w+)/(?P<appt>\d+)/submit$', views.neditapptSubmit, name='neditapptSubmit'),
	url(r'^ncancelappt/(?P<nid>\w+)/(?P<appt>\d+)$', views.ncancelappt, name='ncancelappt'),

    ### Nurse patient info pages
	url(r'^npatientlist/(?P<nid>\w+)$', views.npatientlist, name='npatientlist'),
	url(r'^npatientinfo/(?P<nid>\w+)/(?P<pid>\w+)$', views.npatientinfo, name='npatientinfo'),
	url(r'^npatientinfo/(?P<nid>\w+)/(?P<pid>\w+)/submit$', views.npatientinfoSubmit, name='npatientinfoSumbit'),

    ### Directory pages
    url(r'^aHospitaldir/(?P<aid>\w+)$', views.aHospitaldir, name='aHospitaldir'),
    url(r'^dHospitaldir/(?P<did>\w+)$', views.dHospitaldir, name='dHospitaldir'),
    url(r'^nHospitaldir/(?P<nid>\w+)$', views.nHospitaldir, name='nHospitaldir'),
    url(r'^pHospitaldir/(?P<pid>\w+)$', views.pHospitaldir, name='pHospitaldir'),

    ### Lab Pages
    url(r'^dViewLabs/(?P<did>\w+)$', views.dViewLabs, name='dViewLabs'),
    url(r'^dViewSpecificLab/(?P<did>\w+)$', views.dViewSpecificLab, name='dViewSpecificLab'),
    url(r'^dNewLab/(?P<did>\w+)$', views.dNewLab, name='dNewLab'),
    url(r'^dEditLab/(?P<did>\w+)$', views.dEditLab, name='dEditLab'),
    url(r'^pViewLabs/(?P<pid>\w+)$', views.pViewLabs, name='pViewLabs')

]