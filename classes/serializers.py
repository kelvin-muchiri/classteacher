from rest_framework import serializers
from rest_framework.validators import UniqueValidator


from classes.models import Class

from users.serializers import UserInlineSerializer


class ClassSerializer(serializers.ModelSerializer):
	class Meta:
		model = Class
		fields = (
			'name',
			'description',
			'class_teacher'
		)

		extra_kwargs = {
			'name': {
				'validators': [UniqueValidator(
					queryset=Class.objects.all(),
					message='A class with this name already exists'
				)],
				'error_messages': {
					'blank': 'This field is required'
				}
			}
		}


class ClassInlineSerializer(serializers.ModelSerializer):
	class_teacher = UserInlineSerializer(read_only=True)

	class Meta:
		model = Class
		fields = (
			'name',
			'description',
			'class_teacher'
		)