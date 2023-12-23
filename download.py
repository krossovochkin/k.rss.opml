import sys
import dropbox

DROPBOX_TOKEN = sys.argv[1]

if DROPBOX_TOKEN is None or not DROPBOX_TOKEN.strip():
    raise ValueError("Token is empty or None.")

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
