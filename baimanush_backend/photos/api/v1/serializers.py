from rest_framework import serializers
from baimanush_backend.photos.models import Photos, Images

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'

class PhotosDetailSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, source='images_set')

    class Meta:
        model = Photos
        fields = '__all__'

class PhotoslistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photos
        fields = '__all__'