import vedro
from contexts.api import golden_response, testing_response
from d42 import from_native
from helpers.helpers import prepare_cities_secret

from vedro_replay import Request, replay


class Scenario(vedro.Scenario):
    subject = "do request: {request.method} {request.path} (comment='{request.comment}')"

    @replay("requests/cities_secret.http")
    def __init__(self, request: Request):
        self.request = request

    def given_api_key(self):
        self.api_key = 'replay'

    def given_prepared_request(self):
        self.request.add_header('X-Api-Key', self.api_key)

    async def given_golden_response(self):
        self.golden_response = await golden_response(self.request, prepare_cities_secret)

    async def when_user_sends_request(self):
        self.testing_response = await testing_response(self.request, prepare_cities_secret)

    def then_it_should_return_same_status(self):
        assert self.testing_response.status == self.golden_response.status

    def and_it_should_return_same_headers(self):
        assert self.testing_response.headers == from_native(self.golden_response.headers)

    def and_it_should_return_same_body(self):
        assert self.testing_response.body == from_native(self.golden_response.body)
