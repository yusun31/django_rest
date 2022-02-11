from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
# Views 내에 선언된 함수 -> 인자로 HttpRequest라는 객체를 Django가 전달
def post_list(request):
    my_name = '장고웹프레임워크'
    http_method = request.method
    return HttpResponse('''
        <h2> Welcome {name}</h2>
        <p> Http Method : {method} </p>
        <p> Http Encoding : {encod} </p>
        <p> Http Path : {my_path} </p>
    '''.format(name=my_name, method=http_method, encod=request.encoding, my_path=request.path))
