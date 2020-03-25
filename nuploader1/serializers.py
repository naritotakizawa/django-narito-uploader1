from rest_framework import serializers
from .models import Composite


class CompositeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Composite
        fields = ('pk', 'name', 'is_dir', 'src', 'parent', 'zip_depth')
