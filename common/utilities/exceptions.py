from rest_framework.views import exception_handler
 
 
def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
 
    if response is not None:
        response_data_items = response.data
        response.data = {}
        errors = []
        rejected_fields = ['non_field_errors', 'detail']

        for field, value in response_data_items.items():
            error_obj = {}
            
            if field not in rejected_fields:
                error_obj['pointer'] = field
            else:
                error_obj['pointer'] = "non_field_errors"

            error_obj['message'] = " ".join(value)
            errors .append(error_obj)
 
        response.data['errors'] = errors

    return response