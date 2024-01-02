import requests
from fastapi import Depends

from app.port.outbound.oauth import OauthPort, UserInfo
from app.configs import Settings, get_settings


class GithubOauthAdapter(OauthPort):
    def __init__(self, settings: Settings = Depends(get_settings)):
        super().__init__(settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET)
        self.api_base_url = "https://api.github.com"

    def get_oauth_access_code(self, auth_code: str) -> str:
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
            name=user_name,
            email=email,
            access_token=access_token
        )
