from classes.Client import Client

enc_key = "apples" # pre-determined shared key by clients

if __name__ == "__main__":
    print("Starting client...")
    client = Client(enc_key)
    client.start_client() 
