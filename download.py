import os
import dropbox

# Replace 'YOUR_ACCESS_TOKEN' with your actual access token
DROPBOX_TOKEN = os.getenv("DROPBOX_API_KEY")
dbx = dropbox.Dropbox(DROPBOX_TOKEN)

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
