import httpx


class HttpApiMiddleware:

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        print('before first middleware')
        request.api = httpx
        response = self._get_response(request)
        print('after first middleware')

        return response


class SecondMiddleware:

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        print('before second middleware')
        response = self._get_response(request)
        print('after second middleware')

        return response
