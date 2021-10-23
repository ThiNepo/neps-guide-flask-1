from factory import create_app

app = create_app()

if __name__ == "__main__":
    import socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 0))
    port = sock.getsockname()[1]
    sock.close()

    app.run(debug=True, port=9309)
