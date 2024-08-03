import secrets

def generate_secret_key(length=32):
  """Generates a cryptographically strong random secret key of the specified length.

  Args:
    length: The desired length of the secret key (default: 32).

  Returns:
    A string representing the generated secret key.
  """

  alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()'
  key = ''.join(secrets.choice(alphabet) for i in range(length))
  return key

# Generate a 64-character secret key
secret_key = generate_secret_key(64)
print(secret_key)
