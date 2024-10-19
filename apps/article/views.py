
from apps.article.serializers import ArticleListSerializer, ArticleRetrieveSerializer, ArticleCreateSerializer, ArticleUpdateSerializer, ArticleCategorySerializer
from apps.article.models import Article, ArticleCategory
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class ArticleCategoryListAPIView(generics.ListAPIView):
    queryset = ArticleCategory.objects.order_by("id")
    serializer_class = ArticleCategorySerializer

    

class ArticleListAPIView(generics.ListAPIView):

    serializer_class = ArticleListSerializer

    def get_queryset(self):
        category_id = self.request.query_params.get("category_id", None)
        if category_id:
            return Article.objects.filter(category = category_id)
        else:
            return Article.objects.all()
    
class ArticleRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleRetrieveSerializer
    def get_object(self):
        return self.queryset.get(url_name = self.kwargs["url_name"])

class ArticleCreationAPIView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleCreateSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        title = request.data.get("title")
        url_name = request.data.get("url_name")
        category = request.data.get("category")
        content = request.data.get("content")
        cover_img = request.FILES.getlist("cover")
        pdf = request.FILES.getlist("pdf")
        data = {
            "title": title,
            "category": category,
            "url_name": url_name,
            "content": content,
            "user": request.user.id,
        }
        if cover_img:
            data.update({"cover_img": cover_img[0]})
        if pdf:
            data.update({"pdf": pdf[0]})
        serializer = ArticleCreateSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
        return Response(serializer.data)

class ArticleUpdateAPIView(generics.UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleUpdateSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        id = request.data.get("id")
        url_name = request.data.get("url_name")
        title = request.data.get("title")
        category = request.data.get("category")
        content = request.data.get("content")
        cover_imgs = request.FILES.getlist("cover")
        pdf = request.FILES.getlist("pdf")
        data = {
            "title": title,
            "category": category,
            "url_name": url_name,
            "content": content,
            "user": request.user.id,
        }
        if cover_imgs:
            data.update({"cover_img": cover_imgs[0]})
        if pdf:
            data.update({"pdf": pdf[0]})
        instance = Article.objects.get(id = id)
        serializer = ArticleCreateSerializer(instance, data = data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)







    