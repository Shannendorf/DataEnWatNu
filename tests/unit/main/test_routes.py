from tests.helpers.request_helpers import send_get


class TestIndex:
    def test_index(self, client):
        # GIVEN a client
        # WHEN the user visits the index page
        # THEN the user is redirected to the start page
        resp = send_get(client, "/")
        assert resp.status_code == 302