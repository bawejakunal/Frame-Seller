"""
error processing module
"""
import json

HTTP_ERROR = {
    202: 'Accepted',
    301: 'Moved Permanently',
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not Found',
    500: 'Internal Server Error'
}

def error(http_status=500, message=None):
    """
    return http error codes as suggested in best practises

    https://aws.amazon.com/blogs/compute/error-handling-patterns-in-amazon-api-gateway-and-aws-lambda/
    """  

    err = None

    """
    If developer is making foolish mistake
    make them pay for it
    """
    if http_status not in HTTP_ERROR:
        http_status = 500

    #handle redirect 3xx responses
    if http_status == 301:
        err = message
    else:
        err = {
            'http_status_code': http_status,
            'error_type': HTTP_ERROR[http_status],
            'message': message
        }
        err = json.dumps(err)

    raise Exception(err)


def handle_if_error(response):
    """
    handle error stack trace returned by other lambdas
    """
    if 'errorMessage' not in response:
        return response

    err = json.loads(response['errorMessage'])
    return error(int(err['http_status_code']), err['message'])
