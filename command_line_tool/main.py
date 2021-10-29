from requests import Session

URL = "https://guide-flask.herokuapp.com"

session = Session()

username = input("username: ")
password = input("password: ")

response = session.post(
    f"{URL}/auth/login", json={"password": password, "username": username}
)

if response.status_code == 200:
    token = response.json()["access_token"]
    session.headers = {"Authorization": f"Bearer {token}"}

    response = session.get(f"{URL}/posts/")

    for post in response.json():
        print(post["text"])
        print("-----------")

    while True:
        print("")
        text = input("Share with the community:\n")

        response = session.post(f"{URL}/posts/", json={"author_id": 1, "text": text})

        print(response.status_code)
