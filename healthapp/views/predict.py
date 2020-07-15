import os
import pickle

import pandas as pd
import numpy as np

from django.shortcuts import render, redirect, get_object_or_404

from healthapp.forms import MainSymptomForm, RelatedSymptomForm
from healthapp.models import Disease, Doctor


def index(request):
    if request.user.is_authenticated:
        if request.user.is_doctor:
            return redirect('doctors:dashboard')
        else:
            return redirect('patients:dashboard')
    return render(
        request,
        'healthapp/index.html'
    )


'''
Get the main symptom from common symptoms and return related symptoms
'''


def main_symptom(request):
    module_dir = os.path.dirname(__file__)  # get current directory
    filename = 'related.csv'
    rel_file = os.path.join(module_dir, filename)
    # load the related.csv file to a dataframe
    df = pd.read_csv(rel_file)
    # load the session variable to store users symptosms
    symptoms = request.session.get('symptoms', list())
    if request.method == 'GET':
        form = MainSymptomForm(request.GET)
        if form.is_valid():
            symptom = form.cleaned_data['symptom'] # get the main symptom from form
            symptoms.append(symptom) # Apppend the main symptom to users symptoms
            displayed = request.session.get('displayed', list()) # load the session variable to store already displayed symptoms
            displayed.append(symptom) # Append displayed symptom
            request.session['symptoms'] = symptoms
            rel_list = df[df['symptom'] == symptom]['related'].to_list() # store related symptoms to a list
            displayed.extend(rel_list)
            request.session['displayed'] = displayed
            request.session['related'] = rel_list # store the related list to a session variable
            return redirect('related')
    else:
        request.session['symptoms'] = list() # initialise session variables
        request.session['related'] = list()
        form = MainSymptomForm()
    return render(request,
                  'healthapp/form.html',
                  {'form': form}
                  )


def process_symptoms(request):
    module_dir = os.path.dirname(__file__)  # get current directory
    filename = 'related.csv'
    rel_file = os.path.join(module_dir, filename)
    df = pd.read_csv(rel_file)
    symptoms = request.session.get('symptoms', list())
    related = request.session.get('related', list())
    if request.method == 'GET':
        form = RelatedSymptomForm(request.GET, request=request)

        if form.is_valid():
            if 'next' in request.GET: # If user clicks "next"
                symptom_list = form.cleaned_data['symptoms']
                symptoms.extend(symptom_list)
                displayed = request.session.get('displayed', list())
                rel_set = set()
                # find related symptoms of each symptom in users symptoms
                for each in symptom_list:
                    lst = df[df['symptom'] == each]['related'].to_list()
                    for item in lst:
                        if item not in displayed:
                            rel_set.add(item)
                            displayed.append(item)
                request.session['displayed'] = displayed
                rel_list = list(rel_set)
                request.session['related'] = rel_list
                request.session['symptoms'] = symptoms
                if rel_list:
                    return redirect('related')
                return redirect('result') # if there is no related symptoms redirect to result for prediction
            elif 'check' in request.GET: # if user clicks "submit and check"
                symptom = form.cleaned_data['symptoms']
                symptoms.extend(symptom)
                request.session['symptoms'] = symptoms # get all users symptoms
                return redirect('result')


    else:
        form = RelatedSymptomForm(request=request)

    return render(
        request,
        'healthapp/related.html',
        {'form': form, 'symptoms': symptoms}
    )


def predict_another(request): # clear session variables for new prediction
    request.session.pop('symptoms', None)
    request.session.pop('displayed', None)
    request.session.pop('related', 'None')
    return redirect('main')


def result_view(request):
    # Initialise symptom dictionary
    symptoms_dict = {'itching': 0,
                     'skin_rash': 1,
                     'nodal_skin_eruptions': 2,
                     'continuous_sneezing': 3,
                     'shivering': 4,
                     'chills': 5,
                     'joint_pain': 6,
                     'stomach_pain': 7,
                     'acidity': 8,
                     'ulcers_on_tongue': 9,
                     'muscle_wasting': 10,
                     'vomiting': 11,
                     'burning_micturition': 12,
                     'spotting_ urination': 13,
                     'fatigue': 14,
                     'weight_gain': 15,
                     'anxiety': 16,
                     'cold_hands_and_feets': 17,
                     'mood_swings': 18,
                     'weight_loss': 19,
                     'restlessness': 20,
                     'lethargy': 21,
                     'patches_in_throat': 22,
                     'irregular_sugar_level': 23,
                     'cough': 24,
                     'high_fever': 25,
                     'sunken_eyes': 26,
                     'breathlessness': 27,
                     'sweating': 28,
                     'dehydration': 29,
                     'indigestion': 30,
                     'headache': 31,
                     'yellowish_skin': 32,
                     'dark_urine': 33,
                     'nausea': 34,
                     'loss_of_appetite': 35,
                     'pain_behind_the_eyes': 36,
                     'back_pain': 37,
                     'constipation': 38,
                     'abdominal_pain': 39,
                     'diarrhoea': 40,
                     'mild_fever': 41,
                     'yellow_urine': 42,
                     'yellowing_of_eyes': 43,
                     'acute_liver_failure': 44,
                     'swelling_of_stomach': 45,
                     'swelled_lymph_nodes': 46,
                     'malaise': 47,
                     'blurred_and_distorted_vision': 48,
                     'phlegm': 49,
                     'throat_irritation': 50,
                     'redness_of_eyes': 51,
                     'sinus_pressure': 52,
                     'runny_nose': 53,
                     'congestion': 54,
                     'chest_pain': 55,
                     'weakness_in_limbs': 56,
                     'fast_heart_rate': 57,
                     'pain_during_bowel_movements': 58,
                     'pain_in_anal_region': 59,
                     'bloody_stool': 60,
                     'irritation_in_anus': 61,
                     'neck_pain': 62,
                     'dizziness': 63,
                     'cramps': 64,
                     'bruising': 65,
                     'obesity': 66,
                     'swollen_legs': 67,
                     'swollen_blood_vessels': 68,
                     'puffy_face_and_eyes': 69,
                     'enlarged_thyroid': 70,
                     'brittle_nails': 71,
                     'swollen_extremeties': 72,
                     'excessive_hunger': 73,
                     'extra_marital_contacts': 74,
                     'drying_and_tingling_lips': 75,
                     'slurred_speech': 76,
                     'knee_pain': 77,
                     'hip_joint_pain': 78,
                     'muscle_weakness': 79,
                     'stiff_neck': 80,
                     'swelling_joints': 81,
                     'movement_stiffness': 82,
                     'spinning_movements': 83,
                     'loss_of_balance': 84,
                     'unsteadiness': 85,
                     'weakness_of_one_body_side': 86,
                     'loss_of_smell': 87,
                     'bladder_discomfort': 88,
                     'foul_smell_of urine': 89,
                     'continuous_feel_of_urine': 90,
                     'passage_of_gases': 91,
                     'internal_itching': 92,
                     'toxic_look_(typhos)': 93,
                     'depression': 94,
                     'irritability': 95,
                     'muscle_pain': 96,
                     'altered_sensorium': 97,
                     'red_spots_over_body': 98,
                     'belly_pain': 99,
                     'abnormal_menstruation': 100,
                     'dischromic _patches': 101,
                     'watering_from_eyes': 102,
                     'increased_appetite': 103,
                     'polyuria': 104,
                     'family_history': 105,
                     'mucoid_sputum': 106,
                     'rusty_sputum': 107,
                     'lack_of_concentration': 108,
                     'visual_disturbances': 109,
                     'receiving_blood_transfusion': 110,
                     'receiving_unsterile_injections': 111,
                     'coma': 112,
                     'stomach_bleeding': 113,
                     'distention_of_abdomen': 114,
                     'history_of_alcohol_consumption': 115,
                     'fluid_overload': 116,
                     'blood_in_sputum': 117,
                     'prominent_veins_on_calf': 118,
                     'palpitations': 119,
                     'painful_walking': 120,
                     'pus_filled_pimples': 121,
                     'blackheads': 122,
                     'scurring': 123,
                     'skin_peeling': 124,
                     'silver_like_dusting': 125,
                     'small_dents_in_nails': 126,
                     'inflammatory_nails': 127,
                     'blister': 128,
                     'red_sore_around_nose': 129,
                     'yellow_crust_ooze': 130}
    # Initialize input vector
    input_vector = np.zeros(len(symptoms_dict))
    symptoms = request.session.get('symptoms')
    # Add users symptoms to input vector
    for symptom in symptoms:
        input_vector[symptoms_dict[symptom]] = 1
    # load saved model using pickle
    module_dir = os.path.dirname(__file__)  # get current directory
    filename = 'finalized_model.sav'
    model_file_path = os.path.join(module_dir, filename)
    model_file = open(model_file_path, 'rb')
    loaded_model = pickle.load(model_file)
    # predict the output and store in the output
    out = loaded_model.predict([input_vector])
    disease = out[0]
    try:
        disease_obj = get_object_or_404(Disease, name=disease)
        departments = disease_obj.department.all()
        treatments = disease_obj.treatments.split('&&')
        remedies = disease_obj.remedies.split('&&')
        doctors = []
        for dep in departments:
            doctors.extend(list(Doctor.objects.filter(department = dep)))
    except:
        doctors=[]
        treatments=""
        remedies=""

    return render(request,
                  'healthapp/result.html',
                  {'out': disease, 'doctors':doctors, 'treatments': treatments, 'remedies': remedies}
                 )
