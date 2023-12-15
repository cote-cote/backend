import requests
from fastapi import Depends

from app.domains.oauth import OauthProvider, UserInfo, get_client_id, get_client_secret


class GithubOauthProvider(OauthProvider):

    def __init__(
            self,
            client_id: str = Depends(get_client_id),
            client_secret: str = Depends(get_client_secret)
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_base_url = "https://api.github.com"

    def get_access_token(self, auth_code):
        response = requests.post(
            url="https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": auth_code
            }
        )
        result = response.json()
        access_token = result["access_token"]

        return access_token

    def get_user_info(self, access_token: str) -> UserInfo:
        response = requests.get(
            url=f"{self.api_base_url}/user",
            headers={
                "Authorization": f"Bearer {access_token}",
                "X-GitHub-Api-Version": "2022-11-28"
            }
        )
        result = response.json()
        user_name = result["name"]

        response = requests.get(
            url=f"{self.api_base_url}/user/emails",
            headers={
                "Authorization": f"Bearer {access_token}",
                "X-GitHub-Api-Version": "2022-11-28"
            }
        )
        result = response.json()
        email = result[0]['email']

        return UserInfo(
            user_id="dummy_id",
            user_name=user_name,
            user_email=email,
            user_token="dummy_token",
            access_token=access_token
        )
