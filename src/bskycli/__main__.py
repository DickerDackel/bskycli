from atproto import Client

from bskycli.auth import get_credentials


def main():
    user, password = get_credentials()

    client = Client()
    client.login(user, password)

    post = client.send_post('This is a scripting test.  Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.')

    print(post.uri)
    print(post.cid)


if __name__ == "__main__":
    main()
