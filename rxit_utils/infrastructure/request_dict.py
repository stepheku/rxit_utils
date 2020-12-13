from pyramid.request import Request
import typing

class RequestDictionary(dict):
    def __getattr__(self, k):
        return self.get(k)

def create(request: Request) -> RequestDictionary:
    data = {
        **request.GET,
        **request.headers,
        **request.POST,
        **request.matchdict,
    }

    return RequestDictionary(data)