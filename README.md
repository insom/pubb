# Pubb

Little! Python! ActivityPub!

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
