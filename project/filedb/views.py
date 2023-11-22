from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from .upload_file import UploadedFile
from .models import File
from .serializers import FileSerializer
from .filters import FileFilter


class PingView(APIView):
    def get(self, request):
        return Response(
            data={
                'status': 'pong',
                'timestamp': timezone.now().timestamp()
            },
            status=status.HTTP_200_OK
        )


class FileUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        file = UploadedFile(request.data['file'])
        file_valid = file.is_valid()
        if file_valid.status:
            file = file.save()
            file_serializer = FileSerializer(file)
            return Response(
                file_serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': file_valid.err_message},
                status=status.HTTP_400_BAD_REQUEST
            )


class UploadDataView(CreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer


class QueryDataView(ListAPIView):
    queryset = File.objects.all().order_by('id')
    serializer_class = FileSerializer
    paginator = PageNumberPagination()

    def post(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    def get_queryset(self):
        filters = self.request.data
        extra_filters = {key: value for key, value in filters.items()}
        filter_set = FileFilter(self.request.POST, queryset=self.queryset)
        qs = filter_set.qs
        qs = filter_set.extra_filter(qs, extra_filters)
        paginated_qs = self.paginator.paginate_queryset(qs, self.request)
        return paginated_qs

