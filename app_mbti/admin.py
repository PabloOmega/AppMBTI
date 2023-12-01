from django.contrib import admin
from .models import User, Weight, Question, Answer, Result, Language, LanguageResult
# Register your models here.

admin.site.register(User)
admin.site.register(Weight)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Result)
admin.site.register(Language)
admin.site.register(LanguageResult)