from rest_framework import serializers
from baimanush_backend.photos.models import Photos, Images

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'

class PhotosDetailSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    images = ImagesSerializer(many=True, source='images_set')

    class Meta:
        model = Photos
        fields = '__all__'

    def get_category(self, obj):
        if obj.category:
            return obj.category.name
        return ''

class PhotoslistSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    class Meta:
        model = Photos
        fields = '__all__'
    
    def get_category(self, obj):
        if obj.category:
            return obj.category.slug
        return ''