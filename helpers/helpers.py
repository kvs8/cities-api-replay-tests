from vedro_replay import JsonResponse, MultipartResponse, Response, filter_response


def basic_headers_exclude():
    return []


def basic_body_exclude():
    return []


def prepare_cities(response) -> Response:
    exclude_headers = basic_headers_exclude() + []
    exclude_body = basic_body_exclude() + []
    return filter_response(JsonResponse.from_response(response), exclude_headers, exclude_body)


def prepare_cities_secret(response) -> Response:
    exclude_headers = basic_headers_exclude() + []
    exclude_body = basic_body_exclude() + ['meta.timestamp']
    return filter_response(JsonResponse.from_response(response), exclude_headers, exclude_body)


def prepare_cities_byid(response) -> Response:
    exclude_headers = basic_headers_exclude() + []
    exclude_body = basic_body_exclude() + []
    return filter_response(JsonResponse.from_response(response), exclude_headers, exclude_body)
