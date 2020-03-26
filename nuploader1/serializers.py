from rest_framework import serializers
from .models import Composite


class SimpleCompositeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Composite
        fields = ('pk', 'name', 'is_dir', 'zip_depth', 'parent')


class SimpleCompositeRelation(serializers.RelatedField):

    def to_representation(self, value):
        return SimpleCompositeSerializer(value).data

    def to_internal_value(self, data):
        return self.get_queryset().get(pk=data)

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        # https://github.com/encode/django-rest-framework/issues/5141
        return dict([
            (
                item.pk,
                self.display_value(item)
            )
            for item in queryset
        ])


class CompositeSerializer(serializers.ModelSerializer):
    parent = SimpleCompositeRelation(queryset=Composite.objects.filter(is_dir=True), required=False, allow_null=True)
    composite_set = SimpleCompositeSerializer(read_only=True, many=True)

    class Meta:
        model = Composite
        fields = ('pk', 'name', 'is_dir', 'src', 'parent', 'zip_depth', 'composite_set')
