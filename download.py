import sys
import dropbox
import requests

def refresh_access_token(app_key, app_secret, refresh_token):
    url = "https://api.dropboxapi.com/oauth2/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": app_key,
        "client_secret": app_secret,
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        return access_token
    else:
        print(f"Error refreshing access token: {response.text}")
        return None

# Replace these with your app key, app secret, and refresh token
app_key = sys.argv[1]
app_secret = sys.argv[2]
refresh_token = sys.argv[3]

access_token = get_access_token_from_refresh_token(refresh_token, app_key, app_secret)

if access_token is None or not access_token:
    raise ValueError("Token is empty or None.")

dbx = dropbox.Dropbox(access_token)

# Replace 'YOUR_FOLDER_PATH' with the path to your Dropbox folder
folder_path = '/Apps/Inoreader/OPML_Backup'
result = dbx.files_list_folder(folder_path)

# Extract the latest file
latest_file = max(result.entries, key=lambda x: x.server_modified)

# Download the latest file
file_path = latest_file.path_display
_, res = dbx.files_download(file_path)

# Save the file locally
with open('subscriptions.xml', 'wb') as f:
    f.write(res.content)
