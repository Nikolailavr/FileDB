from django.http import JsonResponse


class GracefulShutdownMiddleware:
    shutdown_flag = False
    post_flag = False

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not GracefulShutdownMiddleware.shutdown_flag:
            GracefulShutdownMiddleware.post_flag = True
            response = self.get_response(request)
            GracefulShutdownMiddleware.post_flag = False
        else:
            print('Your command was canceled. SUBD is already offline')
            response = JsonResponse(
                data={'warning': 'Your command was canceled. SUBD is already offline'},
                status=204
            )
        return response

    def process_exception(self, request, exception):
        return JsonResponse(
            data={'error': exception},
            status=500
        )
