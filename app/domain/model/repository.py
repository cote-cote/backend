from pydantic import BaseModel


class SourceFile(BaseModel):
    id: int
    name: str
    content: str


class PullRequest(BaseModel):
    id: int
    title: str
    content: str
    files: list[SourceFile] = []


class Repository(BaseModel):
    id: int
    pull_requests: list[PullRequest] = []


class GitHubRepository(Repository):
    pass
