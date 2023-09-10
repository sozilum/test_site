from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import Group
from rest_framework.request import Request
from rest_framework.views import APIView
from .serializers import GroupSerializer

@api_view()
def hello_world_api(request:Request) -> Response:
    return Response({'message':'hello world api'})

#Работает как и обычные view из django
# class GroupListView(APIView):
#     def get(self, request: Request) ->Response:
#         groups = Group.objects.all()
#         serializer = GroupSerializer(groups, many=True)
#         return Response({'groups': serializer.data})
    
#Тоже самое что и ListCreateAPIView
# class GroupListView(ListModelMixin ,GenericAPIView):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     def get(self, request: Request) ->Response:
#         return self.list(request)

    
class GroupListView(ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer