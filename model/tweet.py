import uuid
from model.user import User


class Tweet:

    def __init__(self, body: str, author: User):
        self.id = str(uuid.uuid4())
        self.body = body
        self.author = author

    def update(self, new_body):
        self.body = new_body

    def delete(self):
        pass
