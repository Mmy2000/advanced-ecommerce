import jwt

def decode_jwt_token(token):
    try:
        # Decode the JWT token
        decoded_token = jwt.decode(token, options={"verify_signature": False})

        # Print decoded token
        print("Decoded Token:")
        print(decoded_token)

        # Check if 'scope' claim is present
        if 'scope' in decoded_token:
            # Extract the scopes from the token
            scopes = decoded_token['scope'].split()
            print("Scopes:", scopes)
            # Check if the token has the required scope
            if 'admin' in scopes:
                print("User has admin privileges.")
            else:
                print("User does not have admin privileges.")
        else:
            print("No 'scope' claim found in the token.")

    except jwt.ExpiredSignatureError:
        print("Token has expired.")
    except jwt.InvalidTokenError:
        print("Invalid token.")

# Example JWT token (replace with your actual token)
jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

# Decode and check the JWT token
decode_jwt_token(jwt_token)
