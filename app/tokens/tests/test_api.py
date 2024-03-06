from fastapi.testclient import TestClient

from app.main import application
from app.tests import BaseTest
from .. import models

client = TestClient(application)


class TestEndpoints(BaseTest):

    def test_create(self):
        response = client.post('/', json={'user_id': 1})
        token = models.Token.filter(response.json().get('user_id'))[0]
        rtoken = models.RefreshToken.filter(response.json().get('user_id'))[0]
        assert token is not None
        assert rtoken is not None
        assert token.token == response.json().get('token')
        assert token.nonce == response.json().get('token_nonce')
        assert rtoken.token == response.json().get('refresh_token')
        assert rtoken.nonce == response.json().get('refresh_token_nonce')
        assert token.user_id == rtoken.user_id

    def test_get(self):
        model = models.Token.create(user_id=1)
        response = client.get('/', headers={'Authorization': f'Bearer {model.token}'})
        assert response.json().get('id') is None
        assert response.json().get('user_id') == model.user_id

    def test_get_invalid_token(self):
        response = client.get('/', headers={'Authorization': 'Bearer invalid'})
        assert response.status_code == 400
        assert 'jwterror' in response.text.lower()

    def test_get_unauthorized(self):
        model = models.Token.create(user_id=1)
        model.delete()
        response = client.get('/', headers={'Authorization': f'Bearer {model.token}'})
        assert response.status_code == 401
        assert 'unauthorized' in response.text.lower()

    def test_refresh_token(self):
        created = client.post('/', json={'user_id': 1})
        response = client.patch(
            '/',
            headers={'Authorization': f'Bearer {created.json().get('refresh_token')}'},
        )
        assert created.json().get('user_id') == response.json().get('user_id')
        assert created.json().get('token') == response.json().get('token')
        assert created.json().get('token_nonce') == response.json().get('nonce')

    def test_refresh_token_unauthorized(self):
        response = client.patch(
                '/',
                headers={'Authorization': 'Bearer invalid'},
            )
        assert response.status_code == 400

        fake_token = (
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
            'eyJ1c2VyX2lkIjoxLCJub25jZSI6MTM2Nzc2MjQyNDh9.'
            '5WEaZ76aqCAXRA6BjNDtzSNVOy1kigaP-vIqKvaTyLo'
        )
        response = client.patch(
                '/',
                headers={'Authorization': f'Bearer {fake_token}'},
            )
        assert response.status_code == 401

    def test_delete(self):
        created = client.post('/', json={'user_id': 1})
        response = client.delete(
            '/',
            headers={'Authorization': f'Bearer {created.json().get('token')}'}
        )
        assert len(models.Token.filter(created.json().get('user_id'))) == 0
        assert response.json() is None

    def test_delete_unauthorized(self):
        response = client.delete(
                '/',
                headers={'Authorization': 'Bearer invalid'},
            )
        assert response.status_code == 400

        fake_token = (
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
            'eyJ1c2VyX2lkIjoxLCJub25jZSI6MTM2Nzc2MjQyNDh9.'
            '5WEaZ76aqCAXRA6BjNDtzSNVOy1kigaP-vIqKvaTyLo'
        )
        response = client.delete(
                '/',
                headers={'Authorization': f'Bearer {fake_token}'},
            )
        assert response.status_code == 401
