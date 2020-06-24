import json
import requests
from django import http
from django.conf import settings
from django.template import engines
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from .SFE_classify_image import sf_classify_image
from .SFE_classify_zip import sf_classify_zip
from .IBM_classify_image import classify_image
from .IBM_classify_zip import classify_zip
from .serializers import MlcmpSerializer
from .models import Mlcmp


# catchall = TemplateView.as_view(template_name='index.html')

@csrf_exempt
def catchall_dev(request, upstream='http://localhost:3000'):
    """
    Proxy HTTP requests to the frontend dev server in development.

    The implementation is very basic e.g. it doesn't handle HTTP headers.

    """
    upstream_url = upstream + request.path
    method = request.META['REQUEST_METHOD'].lower()
    response = getattr(requests, method)(upstream_url, stream=True)
    content_type = response.headers.get('Content-Type')

    if request.META.get('HTTP_UPGRADE', '').lower() == 'websocket':
        return http.HttpResponse(
            content="WebSocket connections aren't supported",
            status=501,
            reason="Not Implemented"
        )

    elif content_type == 'text/html; charset=UTF-8':
        return http.HttpResponse(
            content=engines['django'].from_string(response.text).render(),
            status=response.status_code,
            reason=response.reason,
        )

    else:
        return http.StreamingHttpResponse(
            streaming_content=response.iter_content(2 ** 12),
            content_type=content_type,
            status=response.status_code,
            reason=response.reason,
        )


catchall_prod = TemplateView.as_view(template_name='index.html')

catchall = catchall_dev if settings.DEBUG else catchall_prod


@api_view(['GET', 'POST'])
def mlcmp_list(request):
    if request.method == 'GET':
        data = Mlcmp.objects.all()
        serializer_class = MlcmpSerializer(data, context={'request': request}, many=True)
        # return render(request, "build/index.html")
        return Response(serializer_class.data)

    elif request.method == 'POST':

        serializer = MlcmpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            print(data)

            return Response(status=status.HTTP_201_CREATED)
        print('error', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BulkView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = MlcmpSerializer(data=request.FILES)
        print(request.FILES)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            print("mlcmp saved with zip.")
            mlcmp = Mlcmp.objects.get(id=serializer.data['id'])
            try:
                mlcmp.result = str(classify_zip(serializer.validated_data.get('file'))) +\
                               'SF RESULT : ' + str(sf_classify_zip(serializer.validated_data.get('file')))
                mlcmp.save()
                print('saved!')
            except Exception as err:
                print(f'Unexpected error occurred: {err}')

            if mlcmp.result is not None or mlcmp.result != '':
                return Response(json.dumps(mlcmp.result), status=status.HTTP_201_CREATED)
            else:
                mlcmp.delete()
                return Response(json.dumps('Analysis did not succeed, please try with different data!'),
                                status=status.HTTP_406_NOT_ACCEPTABLE)


class MlcmpView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        posts = Mlcmp.objects.all()
        serializer = MlcmpSerializer(posts, many=True)
        # render(request, "build/index.html")
        return Response(serializer.validated_data)

    def post(self, request, *args, **kwargs):
        posts_serializer = MlcmpSerializer(data=request.FILES)

        if posts_serializer.is_valid(raise_exception=True):
            posts_serializer.save()
            print('serialized data ##############################################')
            print(posts_serializer.validated_data)
            ibm_classification_result = classify_image(posts_serializer.validated_data.get('image'))
            sf_classification_result = sf_classify_image(posts_serializer.validated_data.get('image'))
            mlcmp = Mlcmp.objects.get(id=posts_serializer.data['id'])
            try:
                mlcmp.result = str(ibm_classification_result['images'][0].get('classifiers')[0].get('classes')) + \
                               ' SF RESULT : ' + str(sf_classification_result['probabilities'][0])
                mlcmp.save()
                print('saved!')
            except Exception as err:
                print(f'Unexpected error occurred: {err}')

            if mlcmp.result is not None or mlcmp.result != '':
                return Response(json.dumps(mlcmp.result), status=status.HTTP_201_CREATED)
            else:
                mlcmp.delete()
                return Response(json.dumps('Analysis did not succeed, please try with different data!'),
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            print('error', posts_serializer.errors)
            return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def mlcmp_detail(request, pk):
    try:
        mlcmp = Mlcmp.objects.get(pk=pk)
    except ObjectDoesNotExist(Mlcmp):
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.mtehod == 'PUT':
        serializer = MlcmpSerializer(mlcmp, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        mlcmp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''
class ListMlcmp(generics.ListCreateAPIView):
    queryset = Mlcmp.objects.all()
    serializer_class = MlcmpSerializer


class DetailMlcmp(generics.RetrieveUpdateAPIView):
    queryset = Mlcmp.objects.all()
    serializer_class = MlcmpSerializer
    
'''