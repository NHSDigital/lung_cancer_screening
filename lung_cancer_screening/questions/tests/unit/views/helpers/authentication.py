from ....factories.user_factory import UserFactory

def login_user(client):
    current_user = UserFactory()
    client.force_login(current_user)

    return current_user
