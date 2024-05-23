import vedro
from contexts.api import golden_response, testing_response
from d42 import from_native
from helpers.helpers import prepare_cities_byid

from vedro_replay import Request, replay, JsonResponse


class Scenario(vedro.Scenario):
    subject = "do request: {request.method} {request.path} (comment='{request.comment}')"

    @replay("requests/cities_byid.http")
    def __init__(self, request: Request):
        self.request = request

    def given_data_request(self):
        self.data_request = Request(method='POST', url='/cities', json_body={
            "id": 8,
            "name": "Томск",
            "code": "tomsk",
        })

    async def given_data_golden_api(self):
        await golden_response(self.data_request, JsonResponse.from_response)

    async def given_data_testing_api(self):
        await testing_response(self.data_request, JsonResponse.from_response)

    async def given_golden_response(self):
        self.golden_response = await golden_response(self.request, prepare_cities_byid)

    async def when_user_sends_request(self):
        self.testing_response = await testing_response(self.request, prepare_cities_byid)

    def then_it_should_return_same_status(self):
        assert self.testing_response.status == self.golden_response.status

    def and_it_should_return_same_headers(self):
        assert self.testing_response.headers == from_native(self.golden_response.headers)

    def and_it_should_return_same_body(self):
        assert self.testing_response.body == from_native(self.golden_response.body)
