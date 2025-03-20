import pytest
from django.urls import reverse_lazy


@pytest.mark.django_db
class TestConfiguration:
    my_url = reverse_lazy("configurations:configuration-my")

    def test_create_on_signup(self, auth_client):
        response = auth_client.get(self.my_url)

        assert response.status_code == 200
        assert all(
            [
                field in response.data.keys()
                for field in (
                    "is_remote_allowed",
                    "allowed_distance",
                    "start_location",
                )
            ]
        )

    def test_update(self, auth_client):
        data = {
            "start_location": {
                "type": "Point",
                "coordinates": [
                    61.74205,
                    -32.37926,
                ],
            }
        }
        response = auth_client.patch(self.my_url, data, format="json")

        assert response.status_code == 200
        assert response.data["start_location"] == data["start_location"]
