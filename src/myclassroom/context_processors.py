def classroom(request):
    previous_url = request.META.get('HTTP_REFERER')
    if previous_url is None:
        previous_url = "/"

    return {"previous_url": previous_url}
