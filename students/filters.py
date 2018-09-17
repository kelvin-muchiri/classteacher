from django_filters import rest_framework as filters

from common.utilities import (
    BooleanFieldFilter,
    CommonFieldsFilterset
)

from students.models import (
    Student,
)


class StudentFilter(CommonFieldsFilterset):
    first_name = filters.CharFilter(field_name='first_name', lookup_expr='iexact')
    last_name = filters.CharFilter(field_name='last_name', lookup_expr='iexact')

    class Meta(object):
        model = Student
        fields = (
            'first_name',
            'last_name',
            'admission_number',
            'student_class',
            'subjects',
        )