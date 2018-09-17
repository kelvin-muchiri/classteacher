from rest_framework import serializers

from subjects.models import Subject

class SubjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Subject
		fields = (
			'name',
			'code'
		)

		extra_kwargs = {
			'name': {
				'error_messages': {
					'blank': 'This field is required'
				}
			},
		}

class SubjectInlineSerializer(serializers.ModelSerializer):
	class Meta:
		model = Subject
		fields = (
			'name',
			'code'
		)