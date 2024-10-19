
from apps.home.serializers import DisplayArticleListSerializer
from apps.article.models import Article
from apps.home.utils import nonogram_solver

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
import random
import json


class DispalyArticleListAPIView(generics.ListAPIView):
    serializer_class = DisplayArticleListSerializer
    def get_queryset(self):
        queryset = Article.objects.order_by("-date_added")[0:5]
        # query_len = len(queryset) 
        # k = 5 if query_len >= 5 else query_len
        # indexes = random.sample(range(len(queryset)), k=k)
        # queryset = [queryset[q] for q in indexes]
        return queryset
    

@api_view(['POST'])
def nonogram_solver_API_view(request):
    row = json.loads(request.data.get("row"))
    column = json.loads(request.data.get("column"))
    table = nonogram_solver(row, column)
    return Response(table)


def dictionary_word_API_view():
    return


    






    