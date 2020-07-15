from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.shortcuts import get_object_or_404

from healthapp.models import User, Patient, Doctor, Department, Appointment, Disease


class MainSymptomForm(forms.Form):
    COMMON_SYMPTOMS = [('itching', 'Itching'),
                     ('skin_rash', 'Skin Rash'),
                     ('continuous_sneezing', 'Continuous Sneezing'),
                     ('chills', 'Chills'),
                     ('joint_pain', 'Joint Pain'),
                     ('stomach_pain', 'Stomach Pain'),
                     ('acidity', 'Acidity'),
                     ('vomiting', 'Vomiting'),
                     ('fatigue', 'Fatigue'),
                     ('weight_gain', 'Weight Gain'),
                     ('anxiety', 'Anxiety'),
                     ('cold_hands_and_feets', 'Cold Hands And Feets'),
                     ('mood_swings', 'Mood Swings'),
                     ('weight_loss', 'Weight Loss'),
                     ('restlessness', 'Restlessness'),
                     ('lethargy', 'Lethargy'),
                     ('irregular_sugar_level', 'Irregular Sugar Level'),
                     ('cough', 'Cough'),
                     ('high_fever', 'High Fever'),
                     ('breathlessness', 'Breathlessness'),
                     ('sweating', 'Sweating'),
                     ('indigestion', 'Indigestion'),
                     ('headache', 'Headache'),
                     ('yellowish_skin', 'Yellowish Skin'),
                     ('dark_urine', 'Dark Urine'),
                     ('nausea', 'Nausea'),
                     ('loss_of_appetite', 'Loss Of Appetite'),
                     ('pain_behind_the_eyes', 'Pain Behind The Eyes'),
                     ('back_pain', 'Back Pain'),
                     ('constipation', 'Constipation'),
                     ('abdominal_pain', 'Abdominal Pain'),
                     ('diarrhoea', 'Diarrhoea'),
                     ('mild_fever', 'Mild Fever'),
                     ('yellow_urine', 'Yellow Urine'),
                     ('yellowing_of_eyes', 'Yellowing Of Eyes'),
                     ('acute_liver_failure', 'Acute Liver Failure'),
                     ('swelling_of_stomach', 'Swelling Of Stomach'),
                     ('swelled_lymph_nodes', 'Swelled Lymph Nodes'),
                     ('malaise', 'Malaise'),
                     ('blurred_and_distorted_vision', 'Blurred And Distorted Vision'),
                     ('phlegm', 'Phlegm'),
                     ('throat_irritation', 'Throat Irritation'),
                     ('redness_of_eyes', 'Redness Of Eyes'),
                     ('sinus_pressure', 'Sinus Pressure'),
                     ('runny_nose', 'Runny Nose'),
                     ('congestion', 'Congestion'),
                     ('chest_pain', 'Chest Pain'),
                     ('fast_heart_rate', 'Fast Heart Rate'),
                     ('pain_during_bowel_movements', 'Pain During Bowel Movements'),
                     ('pain_in_anal_region', 'Pain In Anal Region'),
                     ('bloody_stool', 'Bloody Stool'),
                     ('irritation_in_anus', 'Irritation In Anus'),
                     ('neck_pain', 'Neck Pain'),
                     ('dizziness', 'Dizziness'),
                     ('cramps', 'Cramps'),
                     ('bruising', 'Bruising'),
                     ('obesity', 'Obesity'),
                     ('swollen_legs', 'Swollen Legs'),
                     ('puffy_face_and_eyes', 'Puffy Face And Eyes'),
                     ('enlarged_thyroid', 'Enlarged Thyroid'),
                     ('brittle_nails', 'Brittle Nails'),
                     ('swollen_extremeties', 'Swollen Extremeties'),
                     ('excessive_hunger', 'Excessive Hunger'),
                     ('drying_and_tingling_lips', 'Drying And Tingling Lips'),
                     ('slurred_speech', 'Slurred Speech'),
                     ('knee_pain', 'Knee Pain'),
                     ('hip_joint_pain', 'Hip Joint Pain'),
                     ('muscle_weakness', 'Muscle Weakness'),
                     ('stiff_neck', 'Stiff Neck'),
                     ('swelling_joints', 'Swelling Joints'),
                     ('movement_stiffness', 'Movement Stiffness'),
                     ('loss_of_balance', 'Loss Of Balance'),
                     ('unsteadiness', 'Unsteadiness'),
                     ('loss_of_smell', 'Loss Of Smell'),
                     ('bladder_discomfort', 'Bladder Discomfort'),
                     ('continuous_feel_of_urine', 'Continuous Feel Of Urine'),
                     ('passage_of_gases', 'Passage Of Gases'),
                     ('internal_itching', 'Internal Itching'),
                     ('toxic_look_(typhos)', 'Toxic Look (Typhos)'),
                     ('depression', 'Depression'),
                     ('irritability', 'Irritability'),
                     ('muscle_pain', 'Muscle Pain'),
                     ('red_spots_over_body', 'Red Spots Over Body'),
                     ('belly_pain', 'Belly Pain'),
                     ('abnormal_menstruation', 'Abnormal Menstruation'),
                     ('increased_appetite', 'Increased Appetite'),
                     ('polyuria', 'Polyuria'),
                     ('family_history', 'Family History'),
                     ('mucoid_sputum', 'Mucoid Sputum'),
                     ('rusty_sputum', 'Rusty Sputum'),
                     ('lack_of_concentration', 'Lack Of Concentration'),
                     ('visual_disturbances', 'Visual Disturbances'),
                     ('receiving_blood_transfusion', 'Receiving Blood Transfusion'),
                     ('receiving_unsterile_injections', 'Receiving Unsterile Injections'),
                     ('coma', 'Coma'),
                     ('stomach_bleeding', 'Stomach Bleeding'),
                     ('distention_of_abdomen', 'Distention Of Abdomen'),
                     ('history_of_alcohol_consumption', 'History Of Alcohol Consumption'),
                     ('fluid_overload', 'Fluid Overload'),
                     ('blood_in_sputum', 'Blood In Sputum'),
                     ('prominent_veins_on_calf', 'Prominent Veins On Calf'),
                     ('palpitations', 'Palpitations'),
                     ('painful_walking', 'Painful Walking'),
                     ('skin_peeling', 'Skin Peeling'),
                     ('silver_like_dusting', 'Silver Like Dusting'),
                     ('small_dents_in_nails', 'Small Dents In Nails'),
                     ('inflammatory_nails', 'Inflammatory Nails'),
                     ('blister', 'Blister'),
                     ('red_sore_around_nose', 'Red Sore Around Nose'),
                     ('yellow_crust_ooze', 'Yellow Crust Ooze')]
    symptom = forms.ChoiceField(choices=COMMON_SYMPTOMS, label="Select your main symptom: ")


class RelatedSymptomForm(forms.Form):
    def __init__(self, *args, request=None, **kwargs):
        super(RelatedSymptomForm, self).__init__(*args, **kwargs)
        self.request = request
        rel_list = []
        if request is not None:
            rel_list = request.session.get('related', list())
            RELATED = []
            for each in rel_list:
                RELATED.append((each, " ".join(each.split('_')).title()))

        self.fields['symptoms'] = forms.MultipleChoiceField(choices=RELATED,
                                                            widget=forms.CheckboxSelectMultiple(),
                                                            required=False,
                                                            label="Do you have any of these related symptoms")


DISTRICTS = [
    ('', 'Place'),
    ('AL', 'Alappuzha'),
    ('ER', 'Ernakulam'),
    ('ID', 'Idukki'),
    ('KN', 'Kannur'),
    ('KS', 'Kasargod'),
    ('KZ', 'Kozhikode'),
    ('KL', 'Kollam'),
    ('KT', 'Kottayam'),
    ('MA', 'Malappuram'),
    ('PL', 'Palakkad'),
    ('PT', 'Pathanamthitta'),
    ('TV', 'Thiruvnanthapuram'),
    ('TS', 'Thrissur'),
    ('WA', 'Wayanad')
]


class PatientSignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                    'placeholder': 'Password'}))
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    age = forms.IntegerField(min_value=0,
                             widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}))
    GENDER_CHOICES = [
        ('', 'Gender'),
        ('M', 'Male'),
        ('F', 'Female')
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+ve'),
        ('A-', 'A-ve'),
        ('B+', 'B+ve'),
        ('B-', 'B-ve'),
        ('O+', 'O+ve'),
        ('O-', 'O-ve'),
        ('AB+', 'AB+ve'),
        ('AB-', 'AB-ve')
    ]
    blood_group = forms.ChoiceField(choices=BLOOD_GROUP_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    place = forms.ChoiceField(choices=DISTRICTS, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'age', 'gender', 'blood_group', 'place',)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_patient = True
        user.save()
        patient = Patient(user=user)
        patient.age = self.cleaned_data.get('age')
        patient.gender = self.cleaned_data.get('gender')
        patient.blood_group = self.cleaned_data.get('blood_group')
        patient.place = self.cleaned_data.get('place')
        patient.save()
        return user


class DoctorSignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                    'placeholder': 'Password'}))
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    deptlist = Department.objects.all()
    department = forms.ModelChoiceField(queryset=deptlist, empty_label='Department',
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    place = forms.ChoiceField(choices=DISTRICTS, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'department', 'place',)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_doctor = True
        user.save()
        doctor = Doctor(user=user)
        doctor.department = self.cleaned_data.get('department')
        doctor.place = self.cleaned_data.get('place')
        doctor.save()
        return user


class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.disease = kwargs.pop('disease', None)
        super(AppointmentForm, self).__init__(*args, **kwargs)
        doctor_choices =Doctor.objects.all()
        if self.disease:
            disease_obj = get_object_or_404(Disease, name=self.disease)
            departments = disease_obj.department.all()
            doctor_choices = Doctor.objects.filter(department__in = departments)
        self.fields['doctor'].queryset = doctor_choices

    doctor_choices = Doctor.objects.all()
    doctor = forms.ModelChoiceField(queryset=doctor_choices, empty_label='Select a doctor',
                                    widget=forms.Select(attrs={'class': 'form-control'}))
    date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))

    class Meta:
        model = Appointment
        fields = ('doctor', 'date',)

    @transaction.atomic
    def save(self):
        appointment = Appointment()
        appointment.doctor = self.cleaned_data.get('doctor')
        appointment.date = self.cleaned_data.get('date')
        return appointment
