from rest_framework import serializers

from students.models import Student

from classes.serializers import ClassInlineSerializer

class StudentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Student
		fields = (
			'first_name',
			'last_name',
			'date_of_birth',
			'admission_number',
			'student_class',
		)

		extra_kwargs = {
			'first_name': {
				'error_messages': {
					'blank': 'This field is required'
				}
			},
			'last_name': {
				'error_messages': {
					'blank': 'This field is required'
				}
			},
			'student_class': {
				'error_messages': {
					'null': 'This field is required'
				}
			},
			'date_of_birth': {
				'error_messages': {
					'null': 'This field is required'
				}
			},
		}


class StudentInlineSerializer(serializers.ModelSerializer):
	student_class = ClassInlineSerializer(read_only=True)
	
	class Meta:
		model = Student
		fields = (
			'first_name',
			'last_name',
			'date_of_birth',
			'admission_number',
			'student_class',
		)