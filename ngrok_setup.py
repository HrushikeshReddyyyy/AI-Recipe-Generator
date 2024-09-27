from pyngrok import ngrok

ngrok.set_auth_token('Replace with your ngrok auth token')

public_url = ngrok.connect(8501)  
print(f"Streamlit app running at: {public_url}")
