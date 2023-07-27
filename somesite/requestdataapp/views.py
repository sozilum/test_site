from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core.files.storage import FileSystemStorage

from .forms import UserBioForm, UploadFileForm

def some_base_func(request: HttpRequest) -> HttpResponse:
    a = request.GET.get('a', '')
    b = request.GET.get('b', '')
    result = a + b
    context = {
        'a': a,
        'b': b,
        'result': result,
    }
    return render(request, 'requestdataapp/request-query-params.html', context= context)


def user_form(request: HttpRequest) -> HttpResponse:
    context = {
        'form': UserBioForm(),
    }
    return render(request, 'requestdataapp/user-bio-form.html', context= context)


def handle_upload_file(requset: HttpRequest) -> HttpResponse:
    
    if requset.method == 'POST':
        form = UploadFileForm(requset.POST, requset.FILES)
        if form.is_valid():
            myfile = form.cleaned_data['file']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            print('saved file', myfile)
    
    else:
        form = UploadFileForm()
    
    context = {'form': form,}
    return render(requset, 'requestdataapp/file-upload.html', context= context)