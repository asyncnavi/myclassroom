from django.shortcuts import redirect


def redirect_back(request, alt):
    previous_page = request.META['HTTP_REFERER']
    if previous_page is None:
        return redirect(alt)
    else:
        return redirect(previous_page)
