from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Patient

##########################################
#   CREATE PATIENT TEST
##########################################
#	Unused class to create patient
#	Returns a patient with credentials that should be made.
def createPatient(firstName, lastName, userName, password, ):
        return Patient.objects.create(firstName=firstName,lastName=lastName,
                                      userName=userName,password=password, isActive=True)

##########################################
#   METHOD TESTS
##########################################
#	Unused method tests. For R2
class methodTests(TestCase):
    def test_creation_of_a_patient(self):
        createPatient(firstName="Ty", lastName = "Die", userName="TD", password="dt")
        response = self.client.get('hospital:pinfo', kwargs={'pid':'TD'})
