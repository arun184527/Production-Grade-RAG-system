from pyngrok import ngrok
ngrok.set_auth_token("3B9hFgwSDqc8LMunankr2f6wXUd_6M4sEFTq7afX7NqSYZ74")
public_url = ngrok.connect(8000)
print("Public URL:", public_url)