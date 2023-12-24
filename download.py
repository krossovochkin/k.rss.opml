import sys
import dropbox

def get_access_token_from_refresh_token(refresh_token, app_key, app_secret):
    auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

    try:
        new_access_token = auth_flow.refresh_access_token(refresh_token)
        return new_access_token.access_token
    except dropbox.exceptions.AuthError as e:
        print(f"Error refreshing access token: {e}")
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
