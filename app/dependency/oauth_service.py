from enum import Enum

from fastapi import Depends

from app.application.domain.service.github_oauth_sign_in import GithubOauthSignInService


class OauthProvider(str, Enum):
    GITHUB: str = "github"


def get_oauth_sign_in_service(
        oauth_provider_name: str,
        github_oauth_sign_in_service: GithubOauthSignInService = Depends()
):
    if oauth_provider_name == OauthProvider.GITHUB.value:
        return github_oauth_sign_in_service
    else:
        raise Exception("Unsupported oauth provider has been selected!")
