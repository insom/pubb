# Pubb

Little! Python! ActivityPub!

This is a small Flask ActivityPub server which will only expose one username on a given domain, and which accepts every follow request it gets. Then you can use some of its library to send ActivityPub messages (there's an example of DMing with an image, which was a use-case I wrote this for).

Inspired by https://github.com/sfomuseum/go-activitypub and https://shkspr.mobi/blog/2024/04/the-fediverse-of-things/ but actually using the PHP from https://shkspr.mobi/blog/2024/02/activitypub-server-in-a-single-file/ as more of a reference than the Go code.

I found that most ActivityPub libraries are pretty abstract and I wanted something that was scrappy and understandable, like Terence Eden's single PHP file. But also not in PHP.

## Generate an RSA key pair

```bash
openssl genrsa > private.key
openssl rsa -pubout < private.key > public.key
```

## Configure

```bash
cat > config.ini <<EOF
USERNAME='something'
HOSTNAME='something.somethingelse'
ICON='https://somewhere/summut.png'
EOF
```

## Run

```bash
flask run -h 0.0.0.0
```
