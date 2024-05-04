# Cyberthon 2024: The Galaxy's Best Smuggler

## Setup details

This challenge mounts the host docker daemon for instancing. If this is not permitted on current challenge infrastructure, please inform me.

Edit the range of ports allowed in `app.py`.

To run the instancer:
```
$ docker build -t instancer .
$ docker run -v "/var/run/docker.sock:/var/run/docker.sock" -p 80:80 instancer
```

The challenge instancer will be available on port 80.