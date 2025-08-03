Created:

# Create a private key
openssl genrsa -out key.pem 2048

# create self-signed certificate (valid for 365 days)
openssl req -new -x509 -key key.pem -out cert.pem -days 365