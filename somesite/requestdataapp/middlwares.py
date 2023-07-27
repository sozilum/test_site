from time import time
from typing import Any
from django.http import HttpRequest

def set_useragent_on_requset_middlware(get_response):
    
    print('init_call')
    
    def middlware(request: HttpRequest):
        
        print('before_get_responce')

        request.user_agent = request.META['HTTP_USER_AGENT']

        responce = get_response(request)

        print('after_get_responce')

        return responce

    return middlware


class CountRequestsMiddlwate:
    def __init__(self, get_response) -> None:
        self.__get_responce = get_response
        self.__request_count = 0
        self.__responses = 0
        self.__exceptions_count = 0
        
    
    def __call__(self, request: HttpRequest):
        self.__request_count += 1
        print('request_count', self.__request_count)
        response = self.__get_responce(request)
        self.__responses += 1
        print('responses', self.__responses)
        return response
    
    
    def process_exception(self, request: HttpRequest, exception: Exception):
        self.__exceptions_count += 1
        print('got', self.__exceptions_count, 'excexptions so far')


class throttling_middlware:
    def __init__(self, response) -> None:
        self.__get_reponse = response
        self.__user = {}

    def __call__(self, request: HttpRequest) -> Any:

        result = self.check_ip(request)

        if result:
            response = self.__get_reponse(request)
            return response
        
        else:
            return None
        
        
    def check_ip(self, request:HttpRequest):

        user_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if user_ip:
            ip = user_ip.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        if ip in self.__user:
            total_time = time() - self.__user[ip]
            self.__user.update({ip:time()})

            if total_time <= 0.1:
                return False
            
            else:
                return True

        else:
            self.__user.update({ip:time()})
            return True 
