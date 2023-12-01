# forms.py
from django import forms
from .models import Language, User, Answer

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'nacionality', 'email', 'language']
        
    language = forms.ChoiceField(choices=User.LANGUAGES_CHOICES, widget=forms.Select(attrs={'class': 'select'}))
        
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4, "cols": 50, "placeholder": "Responda aquí"})    
        }
        # error_messages = {
        #     'text': {
        #         'required': "Este campo es obligatorio"
        #     },
        # }
        
    def clean_text(self):
        text = self.cleaned_data.get("text")
        
        # if len(text) < 20 or len(text) > 50:
        #     raise forms.ValidationError("La respuesta debe tener entre 20 y 50 caracteres.")
        num_words = len(text.split(" "))
        if num_words < 20 or num_words > 50:
            self.fields['text'].widget.attrs['class'] = 'textarea-error'
            raise forms.ValidationError(f"La respuesta debe tener entre 20 y 50 palabras. Número de palabras: {num_words}")
        else:
            self.fields['text'].widget.attrs['class'] = ''
        
        return text
