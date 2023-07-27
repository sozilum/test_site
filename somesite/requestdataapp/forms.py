from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError
from django import forms

#Тут создаються классы которые отображают информацию как шаблоны для html страниц
class UserBioForm(forms.Form):
    name = forms.CharField(max_length= 100)
    age = forms.IntegerField(label= 'Your age', min_value= 1, max_value= 100)
    bio = forms.CharField(label= 'Biography', widget= forms.Textarea)

def validate_file_name(file: InMemoryUploadedFile) -> None:
    if file.name and 'virus' in file.name:
        raise ValidationError('Имя файла не должно быть вирус')

class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name])