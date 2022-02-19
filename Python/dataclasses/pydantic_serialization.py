from pydantic import BaseModel


class GitlabUser(BaseModel):
    id: int
    username: str


class GitlabMr(BaseModel):
    id: int
    squash: bool
    web_url: str
    title: str
    author: GitlabUser


mr = GitlabMr(
    id=1,
    squash=True,
    web_url="http://foo",
    title="title",
    author=GitlabUser(id=42, username="Joe"),
)
# print(mr.json())

mr2 = GitlabMr.parse_raw(
    '{"id": 1, "squash": true, "web_url": "http://foo", "title": "title", "author": {"id": 42, "username": "Joe"}}'
)
print(repr(mr2))
