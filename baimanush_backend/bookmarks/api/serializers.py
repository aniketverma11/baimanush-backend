from rest_framework import serializers

from baimanush_backend.articles.models import Post
from baimanush_backend.videos.models import Video
from baimanush_backend.photos.models import Photos

from baimanush_backend.bookmarks.models import BookMarks

from baimanush_backend.articles.api.v1.serializers import PostListSerializer
from baimanush_backend.videos.api.v1.serializers import VideoListSerializer
from baimanush_backend.photos.api.v1.serializers import PhotoslistSerializer


class BookmarkCreateSerializer(serializers.Serializer):
    articles = serializers.ListField(child=serializers.CharField(required=False))
    videos = serializers.ListField(child=serializers.CharField(required=False))
    photos = serializers.ListField(child=serializers.CharField(required=False))

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user

        # Extract UUIDs from validated data
        articles_uuids = validated_data.pop("articles", [])
        videos_uuids = validated_data.pop("videos", [])
        photos_uuids = validated_data.pop("photos", [])

        # Initialize lists for the new items
        articles_data = Post.objects.filter(slug__in=articles_uuids) if articles_uuids else []
        videos_data = Video.objects.filter(slug__in=videos_uuids) if videos_uuids else []
        photos_data = Photos.objects.filter(slug__in=photos_uuids) if photos_uuids else []

        # Get or create the user's bookmarks
        bookmarks, created = BookMarks.objects.get_or_create(created_by=user)

        # Add new articles to the existing ManyToMany field
        if articles_data:
            bookmarks.articles.add(*articles_data)
        
        # Add new videos to the existing ManyToMany field
        if videos_data:
            bookmarks.videos.add(*videos_data)
        
        # Add new photos to the existing ManyToMany field
        if photos_data:
            bookmarks.photos.add(*photos_data)

        return bookmarks



class BookmarkGetSerializer(serializers.ModelSerializer):
    articles = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()

    class Meta:
        model = BookMarks
        fields = ["articles", "videos", "photos"]

    def get_articles(self, obj):
        request = self.context.get("request")
        return PostListSerializer(obj.articles ,many=True, context={"request": request}).data
    
    def get_videos(self, obj):
        request = self.context.get("request")
        return VideoListSerializer(obj.videos ,many=True, context={"request": request}).data
    
    def get_photos(self, obj):
        request = self.context.get("request")
        return PhotoslistSerializer(obj.photos ,many=True, context={"request": request}).data

        

class BookMarkUpdateSerializer(serializers.Serializer):
    slug = serializers.CharField()
    type = serializers.CharField()

    def create(self, validated_data):
        slug = validated_data.pop("slug", "")
        type = validated_data.pop("type", "")
        request = self.context.get("request")
        bookmarks = BookMarks.objects.filter(created_by=request.user).first()

        if not slug:
            raise serializers.ValidationError("Slug is required")

        if not type:
            raise serializers.ValidationError("Post Type is Requied. like -> video, photos, article")


        if type == "videos":
            video = Video.objects.filter(slug=slug).first()
            bookmarks.videos.remove(video)
        
        if type == "photos":
            photo = Photos.objects.filter(slug=slug).first()
            bookmarks.photos.remove(photo)
        
        if type == "articles":
            article = Photos.objects.filter(slug=slug).first()
            bookmarks.articles.remove(article)

            

        return bookmarks