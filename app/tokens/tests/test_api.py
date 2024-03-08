from fastapi.testclient import TestClient
from jose import jwt

from app.config import settings
from app.main import application
from app.tests import BaseTest
from .. import models

client = TestClient(application)


class TestEndpoints(BaseTest):

    def test_create(self):
        response = client.post('/tokens', json={'steamid': 'steamid'})
        token = models.Token.filter(steamid=response.json().get('steamid'))[0]
        rtoken = models.RefreshToken.filter(steamid=response.json().get('steamid'))[0]
        assert token is not None
        assert rtoken is not None
        assert token.token == response.json().get('token')
        assert token.nonce == response.json().get('token_nonce')
        assert rtoken.token == response.json().get('refresh_token')
        assert rtoken.nonce == response.json().get('refresh_token_nonce')
        assert token.steamid == rtoken.steamid

    def test_get(self):
        model = models.Token.create(steamid='steamid')
        response = client.get('/tokens', headers={'Authorization': f'Bearer {model.token}'})
        assert response.json().get('id') is None
        assert response.json().get('steamid') == model.steamid

    def test_get_invalid_token(self):
        response = client.get('/tokens', headers={'Authorization': 'Bearer invalid'})
        assert response.status_code == 400
        assert 'jwterror' in response.text.lower()

    def test_get_unauthorized(self):
        model = models.Token.create(steamid='steamid')
        model.delete()
        response = client.get('/tokens', headers={'Authorization': f'Bearer {model.token}'})
        assert response.status_code == 401
        assert 'unauthorized' in response.text.lower()

    def test_refresh_token(self):
        created = client.post('/tokens', json={'steamid': 1})
        response = client.patch(
            '/',
            headers={'Authorization': f'Bearer {created.json().get('refresh_token')}'},
        )
        assert created.json().get('steamid') == response.json().get('steamid')
        assert created.json().get('token') == response.json().get('token')
        assert created.json().get('token_nonce') == response.json().get('nonce')

    def test_refresh_token_unauthorized(self):
        r1 = client.patch(
                '/tokens',
                headers={'Authorization': 'Bearer invalid'},
            )
        assert r1.status_code == 400

        fake_token = jwt.encode(
            {'steamid': 1, 'nonce': 12345},
            settings.secret_key,
            settings.tokens_algorithm,
        )
        r2 = client.patch(
                '/tokens',
                headers={'Authorization': f'Bearer {fake_token}'},
            )
        assert r2.status_code == 401

    def test_delete(self):
        created = client.post('/tokens', json={'steamid': 'steamid'})
        response = client.delete(
            '/tokens',
            headers={'Authorization': f'Bearer {created.json().get('token')}'}
        )
        assert len(models.Token.filter(steamid=created.json().get('steamid'))) == 0
        assert response.json() is None

    def test_delete_unauthorized(self):
        response = client.delete(
                '/tokens',
                headers={'Authorization': 'Bearer invalid'},
            )
        assert response.status_code == 400

        fake_token = jwt.encode(
            {'steamid': 1, 'nonce': 12345},
            settings.secret_key,
            settings.tokens_algorithm,
        )
        response = client.delete(
                '/tokens',
                headers={'Authorization': f'Bearer {fake_token}'},
            )
        assert response.status_code == 401
