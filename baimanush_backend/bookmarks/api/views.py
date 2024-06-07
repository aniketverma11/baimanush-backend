
from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework import status

from utils.response import cached_response
from rest_framework.permissions import IsAuthenticated, AllowAny


from baimanush_backend.bookmarks.models import BookMarks
from baimanush_backend.bookmarks.api.serializers import BookmarkCreateSerializer, BookmarkGetSerializer, BookMarkUpdateSerializer


class BookmarksViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = BookMarks.objects.filter(is_active=True, is_deleted=False)
    serializer_class = BookmarkGetSerializer

    def create(self, request):
        data = request.data
        serializer = BookmarkCreateSerializer(data=data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return cached_response(
                request=request,
                status=status.HTTP_201_CREATED,
                response_status="success",
                message="",
                data={},
                meta={},
            )
        return cached_response(
            request=request,
            status=status.HTTP_400_BAD_REQUEST,
            response_status="failed",
            message="",
            data=serializer.data,
            meta={},
        )


    def list(self, request):
        objs = self.queryset.filter(created_by=request.user)
        print(objs)
        serializer = self.serializer_class(objs, many=True, context={"request": request})
        return cached_response(
            request=request,
            status=status.HTTP_200_OK,
            response_status="success",
            message="",
            data=serializer.data,
            meta={},
        )
    
    def update(self, request):
        data = request.data
        serializer = BookMarkUpdateSerializer(data=data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return cached_response(
                request=request,
                status=status.HTTP_205_RESET_CONTENT,
                response_status="success",
                message="",
                data={},
                meta={},
            )
        
        return cached_response(
            request=request,
            status=status.HTTP_400_BAD_REQUEST,
            response_status="failed",
            message="",
            data={},
            meta={},
        )