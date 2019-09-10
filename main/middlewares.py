from . import models
from django.conf import settings


def basket_middleware(get_response):
    def middleware(request):
        if 'basket_id' in request.session:
            basket_id = request.session['basket_id']
            basket = models.Basket.objects.get(id=basket_id)
            request.basket = basket
        else:
            request.basket = None
        response = get_response(request)
        return response

    return middleware


class GatedContent(object):
    """
    Prevents specific content directories and types
    from being exposed to non-authenticated users
    """

    def process_request(self, request):
        path = request.path
        user = request.user  # out of the box auth, YMMV

        is_gated = False
        for gated in settings.GATED_CONTENT:
            if path.startswith(gated) or path.endswith(gated):
                is_gated = True
                break
        # Validate the user is an authenticated/valid user

        if is_gated and not user.is_authenticated():
            # Handle redirect
            pass
