import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from dropbox.files import WriteMode

APP_KEY = "bqdz9ndmbqvo5ma"
DROPBOX_PATH = "/events.json"
LOCAL_PATH = "events.json"


class Dbx:
    def __init__(self):
        self.dbx = None

    def is_logged(self):
        return self.dbx is not None

    def login(self):
        auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, use_pkce=True, token_access_type='offline')
        authorize_url = auth_flow.start()
        print("1. Vá até: " + authorize_url)
        print("2. Aperte em \"autorizar\" (você pode precisar se logar antes).")
        print("3. Copie o código de autorização")
        auth_code = input("Cole o código aqui: ").strip()

        try:
            oauth_result = auth_flow.finish(auth_code)
        except Exception as e:
            print('Error: %s' % (e,))
            exit(1)

        with dropbox.Dropbox(oauth2_refresh_token=oauth_result.refresh_token, app_key=APP_KEY) as _dbx:
            self.dbx = _dbx
            self.dbx.users_get_current_account()
            print("Login no seu dropbox efetuado com sucesso!")

    def download_file(self):
        self.dbx.files_download_to_file(LOCAL_PATH, DROPBOX_PATH, rev=None)

    def upload_file(self):

        try:
            with open(LOCAL_PATH, 'rb') as f:
                meta = self.dbx.files_upload(f.read(), DROPBOX_PATH, mode=WriteMode("overwrite"))
                return meta

        except Exception as e:
            print('Error uploading file to Dropbox: ' + str(e))
