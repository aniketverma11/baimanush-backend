from rest_framework import serializers
from baimanush_backend.photos.models import Photos, Images
from baimanush_backend.categories.api.v1.serializers import CategoryListSerializer, SubcategoryListSerializer
from baimanush_backend.articles.api.v1.serializers import TagSerializer
class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'

class PhotosDetailSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, source='images_set')
    category = CategoryListSerializer()
    sub_categories = SubcategoryListSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Photos
        fields = '__all__'

    def get_category(self, obj):
        if obj.category:
            return obj.category.name
        return ''

class PhotoslistSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()
    sub_categories = SubcategoryListSerializer(many=True)
    tags = TagSerializer(many=True)
    class Meta:
        model = Photos
        fields = '__all__'
    