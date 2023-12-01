from os import name
from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator, BaseValidator

class NumWordsValidator(BaseValidator):
    message = "El texto debe tener entre 20 a 50 palabras"
    
    def compare(self, value, model_instance):
        num_words = len(value.split(" "))
        return num_words < 20 or num_words > 50

# Create your models here.
class User(models.Model):
    
    LANGUAGES_CHOICES = [
        ('sp', 'Español'),
        ('en', 'Inglés'),
    ]

    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True, null=True)
    language = models.CharField(max_length=255, choices=LANGUAGES_CHOICES, default='sp')
    nacionality = models.CharField(max_length=255)
    email = models.EmailField()
    report = models.FileField(upload_to='app_mbti/datos/informes', null=True)
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f"{self.name},{self.evsi},{self.svsn},{self.tvsf},{self.jvsp}"
    
class Question(models.Model):
    title = models.CharField(max_length=255, default="")
    question = models.TextField()
    order = models.PositiveIntegerField()
    
class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(default="")
    audio = models.FileField(upload_to="app_mbti/audios", null=True)
    
class Result(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    evsi = models.CharField(max_length=255, null=True)
    svsn = models.CharField(max_length=255, null=True)
    tvsf = models.CharField(max_length=255, null=True)
    jvsp = models.CharField(max_length=255, null=True)
    result = models.CharField(max_length=255, null=True)
    detail = models.TextField(null=True)

class Language(models.Model):
    language = models.CharField(max_length=255)
    
    #index.html
    index_title = models.CharField(max_length=255)
    index_language = models.CharField(max_length=255)
    index_name_placeholder = models.CharField(max_length=255)
    index_nacionality_placeholder = models.CharField(max_length=255)
    index_email_placeholder = models.CharField(max_length=255)
    index_start_button = models.CharField(max_length=255)
    
    #aceptar.html
    aceptar_title = models.CharField(max_length=255)
    aceptar_paragraph = models.TextField()
    aceptar_terms = models.CharField(max_length=255)
    aceptar_accept_button = models.CharField(max_length=255)
    aceptar_last_button = models.CharField(max_length=255)
    
    #terminos.html
    terminos_title = models.CharField(max_length=255)
    terminos_paragraph = models.TextField()
    terminos_reject_button = models.CharField(max_length=255)
    terminos_accept_button = models.CharField(max_length=255)
    
    #preguntas.html
    preguntas_answer_placeholder = models.CharField(max_length=255)
    preguntas_microphone = models.CharField(max_length=255)
    preguntas_last_button = models.CharField(max_length=255)
    preguntas_next_button = models.CharField(max_length=255)
    preguntas_finish_button = models.CharField(max_length=255)
    
    #Dicotomias Preguntas
    preguntas = models.ManyToManyField(Question, null=True)  
    
    #resultado.html
    resultado_title = models.CharField(max_length=255)
    resultado_report = models.CharField(max_length=255)
    resultado_last_button = models.CharField(max_length=255)
    resultado_next_button = models.CharField(max_length=255)
    
    #Dicotomías
    resultado_extroversion = models.CharField(max_length=255, null=True)
    resultado_introversion = models.CharField(max_length=255, null=True)
    resultado_sensacion = models.CharField(max_length=255, null=True)
    resultado_intuicion = models.CharField(max_length=255, null=True)  
    resultado_pensamiento = models.CharField(max_length=255, null=True)
    resultado_sentimiento = models.CharField(max_length=255, null=True)
    resultado_juicio = models.CharField(max_length=255, null=True)
    resultado_percepcion = models.CharField(max_length=255, null=True)
    
    #fin.html
    fin_title = models.CharField(max_length=255)
    fin_thanks = models.CharField(max_length=255)
    fin_last_button = models.CharField(max_length=255)
    
class LanguageResult(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    result = models.CharField(max_length=255)
    detail = models.TextField()
    order = models.PositiveIntegerField(default=0)
    
class Weight(models.Model):
    name = models.CharField(max_length=255)
    weights_file = models.FileField(upload_to="app_mbti/pesos")
    mean_std = models.FileField(upload_to="app_mbti/mean_std")
    
    def get_absolute_url(self):
        return reverse('app-mbti-weight', args=[str(self.id)])