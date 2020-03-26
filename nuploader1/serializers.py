from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import Composite


class SimpleCompositeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Composite
        fields = ('pk', 'name', 'is_dir', 'zip_depth', 'parent')


class SimpleCompositeRelation(serializers.RelatedField):
    default_error_messages = {
        'does_not_exist': _('Invalid pk "{pk_value}" - object does not exist.'),
        'incorrect_type': _('Incorrect type. Expected pk value, received {data_type}.'),
    }

    def to_representation(self, value):
        return SimpleCompositeSerializer(value).data

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(pk=data)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', pk_value=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)

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

    def get_attr(self, name, attrs):
        value = attrs.get(name)
        if value is None and self.instance:
            value = getattr(self.instance, name)
        return value

    def validate(self, attrs):
        parent = self.get_attr('parent', attrs)
        name = self.get_attr('name', attrs)
        is_dir = self.get_attr('is_dir', attrs)
        src = self.get_attr('src', attrs)

        if (self.instance and parent) and (parent.pk == self.instance.pk):
            raise serializers.ValidationError('親ディレクトリが自分です')

        # 同名ファイル・ディレクトリがないかチェック
        same_names = Composite.objects.filter(parent=parent, name=name)
        if self.instance:  # 更新の場合は、自分が同名ファイルとして出てくるので、それは除く
            same_names = same_names.exclude(pk=self.instance.pk)
        if same_names.exists():
            raise serializers.ValidationError('同じ名前のファイル・ディレクトリが既に存在します')

        if not is_dir and not src:  # 基本的にはこない
            raise serializers.ValidationError('ファイルの時は、ファイルを添付してください')

        if is_dir and src:  # 基本的にはこない
            raise serializers.ValidationError('ディレクトリの時は、ファイルを添付しないでください')

        return attrs
