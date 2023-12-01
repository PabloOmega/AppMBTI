from unittest.util import unorderable_list_difference
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.apps import apps
from .models import User, Question, Answer, Result, Language, LanguageResult
from .forms import UserForm, QuestionForm
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .api import CommonMethods
import pdfkit
import pandas as pd
import datetime
import os

# Create your views here.
def create_user(request):
    language = Language.objects.get(language = "sp")
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user_created = form.save()
            return redirect('aceptar', user_id=user_created.id)
    else:
        form = UserForm()

    return render(request, 'app_mbti/index.html', {'form': form, 'language': language})

def accept(request, user_id):
    user = get_object_or_404(User, id=user_id)
    language = Language.objects.get(language = user.language)
    return render(request, 'app_mbti/aceptar.html', {'user': user, 'language': language})

def terms(request, user_id):
    user = get_object_or_404(User, id=user_id)
    language = Language.objects.get(language = user.language)
    return render(request, 'app_mbti/terminos.html', {'user': user, 'language': language})
    
def get_question_form(request, user_id, question_id):
    user = get_object_or_404(User, id=user_id)
    #question = get_object_or_404(Question, id=question_id)
    language = Language.objects.get(language = user.language)
    question = language.preguntas.get(order = question_id)
    answer, _ = Answer.objects.get_or_create(user = user, question = question)
    
    #questions = Question.objects.order_by("order")
    questions = language.preguntas.order_by("order")
    
    question_last = questions.get(order = question.order - 1) if question.order > 1 else None
    question_next = questions.get(order = question.order + 1) if question.order < 4 else None

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # if not answer:
            #     answer = form.save(commit=False)
            print(form.cleaned_data["text"])
            answer.text = form.cleaned_data["text"]
            answer.save()
            if question_next:
                return redirect(reverse('get_question_form', args=[user_id, question_next.order]))
            else:
                return redirect(reverse('resultado', args=[user_id]))
    else:
        form = QuestionForm(initial={"text": answer.text})
        
    return render(request, 'app_mbti/preguntas.html', {
        'user': user,
        'question': question,
        'question_last': question_last,
        'question_next': question_next,
        'form': form,
        'language': language
    })

def get_result(request, user_id):
    user = get_object_or_404(User, id = user_id)
    language = Language.objects.get(language = user.language)
    answers = Answer.objects.filter(user = user).order_by("question__order")
    result, _ = Result.objects.get_or_create(user = user)
    results = [0,0,0,0]
    app_config = apps.get_app_config('app_mbti')
    
    for i in range(4):
        if i == 4:
            results[i] = app_config.windows[i].model_output(answers[i].text)
        else:
            results[i] = int(app_config.windows[i].model_output(answers[i].text) < 0.5)
    # result.evsi = outputs[0][results[0]]
    # result.svsn = outputs[1][results[1]]
    # result.tvsf = outputs[2][results[2]]
    # result.jvsp = outputs[3][results[3]]
    
    result.evsi = language.resultado_introversion if results[0] else language.resultado_extroversion
    result.svsn = language.resultado_intuicion if results[0] else language.resultado_sensacion
    result.tvsf = language.resultado_sentimiento if results[0] else language.resultado_pensamiento
    result.jvsp = language.resultado_percepcion if results[0] else language.resultado_juicio
    
    num_result = calculate_result(results)
    # result.result = personalidades[num_result]
    # result.detail = detalle_personalidades[num_result]
    
    language_result = LanguageResult.objects.filter(language__language = user.language, order = num_result).get()
    result.result = language_result.result
    result.detail = language_result.detail
    result.save()
    
    generate_xls()
    generate_user_report(user)

    return render(request, 'app_mbti/resultado.html', {'user': user, 'result': result, 'language': language})

def end(request, user_id):
    user = get_object_or_404(User, id = user_id)
    language = Language.objects.get(language = user.language)
    return render(request, 'app_mbti/fin.html', {'user': user, 'language': language})

def generate_xls():
    
    users = User.objects.all().order_by("-id")
    answer_1 = Answer.objects.filter(question__order = 1).order_by("-user__id")
    answer_2 = Answer.objects.filter(question__order = 2).order_by("-user__id")
    answer_3 = Answer.objects.filter(question__order = 3).order_by("-user__id")
    answer_4 = Answer.objects.filter(question__order = 4).order_by("-user__id")
    results = Result.objects.all().order_by("-user__id")

    data = {
        "Fecha": [user.date for user in users],
        "Nombre": [user.name for user in users],
        "Nacionalidad": [user.nacionality for user in users],
        "Correo": [user.email for user in users],
        "Respuesta 1": [answer.text for answer in answer_1],
        "Respuesta 2": [answer.text for answer in answer_2],
        "Respuesta 3": [answer.text for answer in answer_3],
        "Respuesta 4": [answer.text for answer in answer_4],
        "E vs I": [result.evsi for result in results],
        "S vs N": [result.svsn for result in results],
        "T vs F": [result.tvsf for result in results],
        "J vs P": [result.jvsp for result in results],
        "Resultado": [result.result for result in results],
        "Detalle": [result.detail for result in results],
    }
    
    max_length = len(data["Nombre"])
    
    for i in data:
        data[i] += [None] * (max_length - len(data[i]))

    df = pd.DataFrame(data)
    df["Fecha"] = df["Fecha"].dt.tz_localize(None)    

    df.drop("Detalle", axis=1).to_csv("app_mbti/datos/Datos Históricos.csv", index = False)
    df.drop("Detalle", axis=1).to_excel("app_mbti/datos/Datos Históricos.xlsx", index = False, header = True)
    
def generate_user_report(user):

    answer_1 = Answer.objects.get(question__order = 1, user = user)
    answer_2 = Answer.objects.get(question__order = 2, user = user)
    answer_3 = Answer.objects.get(question__order = 3, user = user)
    answer_4 = Answer.objects.get(question__order = 4, user = user)
    result = Result.objects.get(user = user)    
    
    data = {
        "Fecha": datetime.datetime.now(),
        "Nombre": user.name,
        "Nacionalidad": user.nacionality,
        "Correo": user.email,
        "Respuesta 1": answer_1.text,
        "Respuesta 2": answer_2.text,
        "Respuesta 3": answer_3.text,
        "Respuesta 4": answer_4.text,
        "E vs I": result.evsi,
        "S vs N": result.svsn,
        "T vs F": result.tvsf,
        "J vs P": result.jvsp,
        "Resultado": result.result,
        "Detalle": result.detail,
    }

    pd.set_option('colheader_justify', 'center')   # FOR TABLE <th>
    with open('app_mbti/templates/app_mbti/informes/informe_template.html', 'r') as f: # carga la plantilla del informe
        informe_template = f.read()
        
    with open(f'app_mbti/templates/app_mbti/informes/informe_{user.name}_{user.id}.html', 'w', encoding='utf-8') as f:
        f.write(informe_template.format(table=pd.Series(data).to_frame(name=user.id).to_html(classes='informe')))
        
    generate_pdf(user)
        
def generate_pdf(user):
    user.report.delete()
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    html_file_path = f'app_mbti/templates/app_mbti/informes/informe_{user.name}_{user.id}.html'
    css_file_path = 'app_mbti/static/css/informe.css'
    pdf_file_path = f'app_mbti/datos/informes/informe_{user.name}_{user.id}.pdf'

    options = {
        'page-size': 'A4',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        "enable-local-file-access": "",
        'encoding': 'utf-8',  # Especifica la codificación UTF-8
    }

    pdf = pdfkit.from_file(html_file_path, pdf_file_path, css=css_file_path, options=options, configuration=config)
    
    with open(pdf_file_path, 'rb') as pdf_file:
        user.report.save(f'informe_{user.name}_{user.id}.pdf', pdf_file, save=True)
    
    
def get_report(request, user_id):
    user = get_object_or_404(User, id = user_id)
    with open(user.report.path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        
    report_name = os.path.basename(user.report.name)
    response['Content-Disposition'] = f'attachment; filename="{report_name}"'
    return response

@csrf_exempt
def speech_to_text(request, user_id, question_id):
    user = get_object_or_404(User, id = user_id)
    language = Language.objects.get(language = user.language)
    question = language.preguntas.get(order = question_id)
    answer = Answer.objects.get(user = user, question = question)
    
    if request.method == 'POST':
        audio = request.FILES.get('audio')
        if audio:
            answer.audio.delete()
            answer.audio = audio
            answer.audio.name = f"Audio_{user_id}_{question_id}.webm"
            answer.save()

            return JsonResponse({'status': 'success', 'message': CommonMethods.speech_to_text(answer.audio.path)})
        else:
            return JsonResponse({'status': 'error', 'message': 'No se recibió ningún archivo de audio.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido.'})
    
def calculate_result(results):
    """
    Permite unificar las respuestas de los 4 modelos en una sola respuesta para el frontend
    Parámetros:
        results: respuestas de los 4 modelos 
    Retorno:
        Retorna la respuesta unificada
    """
    result = results[3]
    for i,r in enumerate(results):
        result |= int(r) << (3-i)
    return result    

