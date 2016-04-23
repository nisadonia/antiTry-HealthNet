import datetime as dt

from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from .models import *
from .utility.options import *

c = Client()

# Create a standard naming scheme so we can understand what you are doing -- Matt

# You don't need failure cases, your cases should test things that would be failures, if they fail the failure cases
# are never reached anyway. -- Matt
"""
The general Naming Scheme for test cases is as follows:
test_[user who is performing act]_[the action being performed]_[optional: user being acted upon]
    _[optional: the thing being acted upon]
Note: _success or _fail will be in all of the tests. The function names are intended to be read how they were written
      in the TestTracker.doc
e.g. test_doc_update_pat_med_info_success
"""


# create all the dictionaries for all the users
def create_patient_dict(email, password, user_type, name="The L Diablo", dob=dt.datetime.now(), gender=Gender.MALE, height1=7,
                        height2=11, height3=1, weight=100, hunits=Units.CUSTOMARY, wunits=Units.CUSTOMARY, secq=SecQ.Q1,
                        seca="testsec", insurance=INSURANCE_CHOICES[0][0], bloodtype=BloodType.O,
                        contact_name="Test Contact", contact_email="contact@c.com", contact_primary="516-123-4567",
                        contact_secondary='', contact_relationship=Relationship.OTHER, address_line_one="Blah",
                        address_line_two=None, address_city="Bleh", address_state="NY", address_zipcode="12345"):
    bits = name.split(sep=' ')
    if len(bits) < 2:
        raise ValueError('Name must have at least two parts, detected %d' % len(bits))
    elif len(bits) == 2:
        fname = bits[0]
        lname = bits[1]
        minitial = ''
    else:
        fname = bits[0]
        minitial = bits[1]
        lname = bits[2]

    return {
        'first_name': fname,
        'middle_initial': minitial,
        'last_name': lname,
        'date_of_birth': dob.strftime('%m/%d/%Y'),
        'gender': gender,
        'security_question': secq,
        'security_answer': seca,
        'height_0': hunits,
        'height_1': height1,
        'height_2': height2,
        'height_3': height3,
        'weight_0': wunits,
        'weight_1': weight,
        'insurance': insurance,
        'blood_type': bloodtype,
        'email': email,
        'password': password,
        'contact_name': contact_name,
        'contact_email': contact_email,
        'contact_primary': contact_primary,
        'contact_secondary': contact_secondary,
        'contact_relationship': contact_relationship,
        'address1': address_line_one,
        'address2': address_line_two,
        'address_city': address_city,
        'address_state': address_state,
        'address_zipcode': address_zipcode,
        'user_type': user_type,
    }


def create_appt_dict(date='04/28/2016', time = '12:00', doctor = 'John J Doe', patient = 'Anthony Perez',
                     location = 'Anthony'):
    return {
        'date': date,
        'time': time,
        'doctor': doctor,
        'patient': patient,
        'location': location,
    }


def create_admin_dict(email, password, user_type, name="Im An Admin", dob=dt.datetime.now(), gender=Gender.MALE, secq=SecQ.Q1,
                      seca="testsec", address_line_one="Blah", address_line_two=None, address_city="Bleh",
                      address_state="NY", address_zipcode="12345", is_sysadmin=False, hospital=None):
    bits = name.split(sep=' ')
    if len(bits) < 2:
        raise ValueError('Name must have at least two parts, detected %d' % len(bits))
    elif len(bits) == 2:
        fname = bits[0]
        lname = bits[1]
        minitial = ''
    else:
        fname = bits[0]
        minitial = bits[1]
        lname = bits[2]

    return {
        'first_name': fname,
        'middle_initial': minitial,
        'last_name': lname,
        'date_of_birth': dob.strftime('%m/%d/%Y'),
        'gender': gender,
        'security_question': secq,
        'security_answer': seca,
        'email': email,
        'password': password,
        'address1': address_line_one,
        'address2': address_line_two,
        'address_city': address_city,
        'address_state': address_state,
        'address_zipcode': address_zipcode,
        'is_sysadmin': is_sysadmin,
        'hospital': hospital,
        'user_type': user_type,
    }


def create_doct_dict(email, password, user_type, name="Im A Doctor", dob=dt.datetime.now(), gender=Gender.MALE, secq=SecQ.Q1,
                      seca="testsec", address_line_one="Blah", address_line_two=None, address_city="Bleh",
                      address_state="NY", address_zipcode="12345",hospitals=None)
    bits = name.split(sep=' ')
    if len(bits) < 2:
        raise ValueError('Name must have at least two parts, detected %d' % len(bits))
    elif len(bits) == 2:
        fname = bits[0]
        lname = bits[1]
        minitial = ''
    else:
        fname = bits[0]
        minitial = bits[1]
        lname = bits[2]

    return {
        'first_name': fname,
        'middle_initial': minitial,
        'last_name': lname,
        'date_of_birth': dob.strftime('%m/%d/%Y'),
        'gender': gender,
        'security_question': secq,
        'security_answer': seca,
        'email': email,
        'password': password,
        'address1': address_line_one,
        'address2': address_line_two,
        'address_city': address_city,
        'address_state': address_state,
        'address_zipcode': address_zipcode,
        'user_type': user_type,
        'hospitals': hospitals,
    }


def create_nurse_dict(email, password, user_type, name="Im A Nurse", dob=dt.datetime.now(), gender=Gender.MALE, secq=SecQ.Q1,
                      seca="testsec", address_line_one="Blah", address_line_two=None, address_city="Bleh",
                      address_state="NY", address_zipcode="12345", hospital=None):
    bits = name.split(sep=' ')
    if len(bits) < 2:
        raise ValueError('Name must have at least two parts, detected %d' % len(bits))
    elif len(bits) == 2:
        fname = bits[0]
        lname = bits[1]
        minitial = ''
    else:
        fname = bits[0]
        minitial = bits[1]
        lname = bits[2]

    return {
        'first_name': fname,
        'middle_initial': minitial,
        'last_name': lname,
        'date_of_birth': dob.strftime('%m/%d/%Y'),
        'gender': gender,
        'security_question': secq,
        'security_answer': seca,
        'email': email,
        'password': password,
        'address1': address_line_one,
        'address2': address_line_two,
        'address_city': address_city,
        'address_state': address_state,
        'address_zipcode': address_zipcode,
        'hospital': hospital,
        'user_type': user_type,
    }


class RegistrationTest(TestCase):
    """
    All cases involving Patient registration and Staff Registration (Nurse or Doc)
    """
    # create hospital
    def setUp(self):
        hospital = Hospital(name="Matt", address="Matt",state="Ma",zipcode="06288")
        hospital.save()
    # patient registration cases
    def test_pat_reg_pat_and_user_exist(self):
        email = "test@test.com"
        passwd = 'qwerty123'
        user_type = "Patient"

        c.post(reverse('registry:register'), data=create_patient_dict(email, passwd, user_type))

        user = DjangoUser.objects.get(email=email)

        pat = Patient.objects.get(auth_user_id=user.id)
        self.assertIsInstance(pat, Patient, 'get_subclass did not return patient!')
        self.assertIsInstance(pat, User, 'get_subclass patient is not also user!')
        self.assertIsNotNone(pat.auth_user.username, 'Patient username not set properly!')

    # Note: ec = Emergency Contact
    # success cases
    def test_pat_reg_success_add_ec(self):
        pat = Patient.objects.get(email="test@test.com")
        contact = PatientContact.objects.get(contact_email="contacts@c.com")

        self.assertTrue(pat.contact_set.filter(contact_email=contact.contact_email).exists())

    # failure cases
    def test_pat_reg_fail_incomplete(self):
        email = "test2@test2.com"
        pw = None
        user_type = "Patient"

        c.post(reverse('registry:register'), data=create_patient_dict(email, pw, user_type))
        self.assertFalse(Patient.objects.filter(email=email).exists())


    # staff registration cases
    # Note: The admin registers the staff!
    # success case
    def test_admin_reg_staff_success(self):
        # admin info
        email_admin = "admin@admin.com"
        pw_admin = 'qwerty123'
        user_type_admin = "Admin"
        hospital = Hospital.objects.get(name='Matt')

        # doctor info
        email_doc = "doc@doc.com"
        pw_doc = "qwerty123"
        user_type_doc = "Doc"
        hospitals = Hospital.objects.get(name="Matt")

        # nurse info
        email_nurse = "nurse@nurse.com"
        pw_nurse = "qwerty123"
        user_type_nurse = "Nurse"
        # Shares hospital variable already made for admin info

        # can admin register doctor?
        c.post(reverse('registry:user_create'), data=create_doct_dict(email_doc, pw_doc, hospitals, user_type_doc))
        self.assertTrue(Doctor.objects.filter(email=email_doc).exists())
        # can admin register nurse?
        c.post(reverse('registry:user_create'), data=create_nurse_dict(email_nurse, pw_nurse, hospital, user_type_nurse))
        self.assertTrue(Nurse.objects.filter(email=email_nurse).exists())
        # can admin register admin?
        c.post(reverse('registry:user_create'), data=create_admin_dict(email_admin, pw_admin, hospital, user_type_admin))
        self.assertTrue(Administrator.objects.filter(email=email_admin).exists())


    # failure cases
    def test_admin_reg_staff_fail_incomplete(self):
        # admin info
        email_admin = None
        pw_admin = 'qwerty123'
        user_type_admin = "Admin"
        hospital = Hospital.objects.get(name='Matt')

        # doctor info
        email_doc = None
        pw_doc = "qwerty123"
        user_type_doc = "Doc"
        hospitals = Hospital.objects.get(name="Matt")

        # nurse info
        email_nurse = None
        pw_nurse = "qwerty123"
        user_type_nurse = "Nurse"
        # Shares hospital variable already made for admin info

        # can admin register doctor? Hopefully not!
        c.post(reverse('registry:user_create'), data=create_doct_dict(email_doc, pw_doc, hospitals, user_type_doc))
        self.assertFalse(Doctor.objects.filter(email=email_doc).exists())
        # can admin register nurse? Hopefully not!
        c.post(reverse('registry:user_create'), data=create_nurse_dict(email_nurse, pw_nurse, hospital, user_type_nurse))
        self.assertFalse(Nurse.objects.filter(email=email_nurse).exists())
        # can admin register admin? Hopefully not!
        c.post(reverse('registry:user_create'), data=create_admin_dict(email_admin, pw_admin, hospital, user_type_admin))
        self.assertFalse(Administrator.objects.filter(email=email_admin).exists())


class AppointmentTest(TestCase):
    """
    All things to do with Appointments
    Create, update, cancel, view
    Since doctor, nurse, and patient all create an appointment the same way, there only needs to be one general test
    case for all of them.
    """
    # create tests
    def test_user_create_pat_appt(self):
        c.post(reverse('registry:appt_schedule'), data=create_appt_dict())
        appt = Appointment.objects.filter(date = '04/28/2016', time = '12:00', doctor = 'John J Doe', patient = 'Anthony Perez',
                     location = 'Anthony')
        self.assertTrue(appt.exist())

    # update tests
    def test_user_update_pat_appt(self):
        pass

    # cancel tests
    # Note: Nurses cannot cancel appointments
    def test_user_cancel_pat_appt(self):
        pass

    # MUST BE DONE MANUALLY
    # # view tests
    # # Note: Nurses cannot view appointment calendars
    # def test_doc_view_appnt_calendar(self):
    #     pass
    #
    # def test_pat_view_appnt_calendar(self):
    #     pass


## Merge PersonalInformation and MedicalInformation, all users can update their own information
class PersonalInformation(TestCase):
    """
    Update patient personal information
    """
    # success case
    def test_pat_update_info_success(self):
        pass

    # failure cases
    def test_pat_update_info_fail(self):
        pass

class MedicalInformation(TestCase):
    """
    Deals with updating and viewing medical information
    """
    # *** Update Medical Information *** #
    # success cases
    def test_doc_update_pat_med_info_success(self):
        pass
    def test_nurse_update_pat_med_info_success(self):
        pass

    # failure cases
    def test_doc_update_pat_med_info_fail_clear_field(self):
        pass

    def test_doc_update_pat_med_info_cancel(self):
        pass

    def test_nurse_update_pat_med_info_fail_clear_field(self):
        pass

    def test_nurse_update_pat_med_info_cancel(self):
        pass

    # *** View Medical Information *** #
    # success cases; cannot fail
    def test_doc_view_pat_med_info_success(self):
        pass

    def test_nurse_view_pat_med_info_success(self):
        pass


class ExportInfo(TestCase):
    """
    Needs to deal with Success and Failure
    """
    # success case
    def test_export_info_success(self):
        pass

    # failure cases
    def test_export_info_fail_incorrect_sec_qs(self):
        pass

    def test_export_info_fail_clicks_no(self):
        pass

    def test_export_info_fail_cancel(self):
        pass


class Prescription(TestCase):
    """
    Deals with adding and deleting prescriptions
    """
    # *** Adding Prescriptions *** #
    # success case
    def test_doc_add_rx_success(self):
        pass

    # failure cases
    def test_doc_add_rx_fail_incomplete(self):
        pass

    # *** Deleting Prescriptions *** #
    # success case
    def test_doc_del_rx_success(self):
        pass


### Need to add admin capable of doing this as well?
### Test tracker doesn't plan for this though
class Discharge(TestCase):

    # success case
    def test_doc_discharge_pat_success(self):
        pass


class Admit(TestCase):

    # success cases
    def test_doc_admit_pat(self):
        pass

    def test_nurse_admit_pat(self):
        pass

    # failure cases
    def test_doc_admit_pat_fail_incorrect(self):
        pass

    def test_nurse_admit_pat_fail_incorrect(self):
        pass


### Note: pm = Private Message
### Note: dne = recepient does not exist
class PrivateMessage(TestCase):

    """
    Deals with sending and viewing Private Messaging between
    patients, doctors, nurses, and admins.
    """

    # Only need to test User in general, not one for each user type
    # all use the same system, it's its own module.

    # *** Send Private Messages *** #
    # success cases
    def test_pat_send_pm_success(self):
        pass

    def test_doc_send_pm_success(self):
        pass

    def test_nurse_send_pm_success(self):
        pass

    def test_admin_send_pm_success(self):
        pass

    # failure cases #
    # patient fails
    def test_pat_send_pm_fail_dne(self):
        pass

    def test_pat_send_pm_fail_incomplete(self):
        pass

    def test_pat_send_pm_fail_cancel(self):
        pass

    # doctor fails
    def test_doc_send_pm_fail_dne(self):
        pass

    def test_doc_send_pm_fail_incomplete(self):
        pass

    def test_doc_send_pm_fail_cancel(self):
        pass

    # nurse fails
    def test_nurse_send_pm_fail_dne(self):
        pass

    def test_nurse_send_pm_fail_incomplete(self):
        pass

    def test_nurse_send_pm_fail_cancel(self):
        pass

    # admin fails
    def test_admin_send_pm_fail_dne(self):
        pass

    def test_admin_send_pm_fail_incomplete(self):
        pass

    def test_admin_send_pm_fail_cancel(self):
        pass

    # *** View Private Messages *** #
    # success cases; no failures for viewing
    def test_pat_view_pm_success(self):
        pass

    def test_doc_view_pm_success(self):
        pass

    def test_nurse_view_pm_success(self):
        pass

    def test_admin_view_pm_success(self):
        pass

class MedicalResults(TestCase):
    # *** Upload *** #
    # success case
    def test_doc_upload_med_res_success(self):
        pass

    # failure cases
    def test_doc_upload_med_res_fail_incomplete(self):
        pass

    # *** Release *** #
    # success case
    def test_doc_release_med_res__success(self):
        pass


class Transfer(TestCase):

    # Combine into Doctor or Administrator

    # success case
    def test_doc_transfer_pat_success(self):
        pass
    def test_admin_transfer_pat_success(self):
        pass

    # failure case
    def test_doc_transfer_pat_fail_same_hosp(self):
        pass
    def test_doc_transfer_pat_fail_no_doctor(self):
        pass
    def test_admin_transfer_pat_fail_same_hosp(self):
        pass
    def test_admin_transfer_pat_fail_no_doctor(self):
        pass