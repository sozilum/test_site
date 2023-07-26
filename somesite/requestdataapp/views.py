from django.core.files.base import ContentFile
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core.files.storage import FileSystemStorage

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
    return render(request, 'requestdataapp/user-bio-form.html')


def handle_upload_file(requset: HttpRequest) -> HttpResponse:
    context = {
            'status': True
        }
    if requset.method == 'POST' and requset.FILES.get('myfile') and requset.FILES.get('myfile').size <= 1000:
        myfile = requset.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        print('saved file', myfile)
    
    else:
        context['status'] = False
    return render(requset, 'requestdataapp/file-upload.html', context= context)