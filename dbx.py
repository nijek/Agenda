from tkinter import ttk
import tkinter as tk
import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from dropbox.files import WriteMode
from Tools import open_centered_window
import webbrowser
APP_KEY = "bqdz9ndmbqvo5ma"
DROPBOX_PATH = "/events.json"
LOCAL_PATH = "events.json"

class Dbx:
    def __init__(self):
        self.dbx = None
        self.dbx_window = None

    def finish_auth(self, text_box, auth_flow):

        auth_code = text_box.get("1.0", 'end-1c').strip()
        try:
            oauth_result = auth_flow.finish(auth_code)
        except Exception as e:
            print('Erro: %s' % (e,))
            exit("failure")

        with dropbox.Dropbox(oauth2_refresh_token=oauth_result.refresh_token, app_key=APP_KEY) as _dbx:
            self.dbx = _dbx
            self.dbx.users_get_current_account()
            ok_window = open_centered_window("Login bem sucedido", 350, 100)
            ttk.Label(ok_window, text="Login no dropbox efetuado com sucesso").pack(pady=10)
            ttk.Button(ok_window, text="Ok",
                       command=lambda: [ok_window.destroy(), self.dbx_window.destroy()]).pack(pady=10)
            ok_window.lift()
            ok_window.attributes('-topmost', True)
            ok_window.mainloop()
            print("Login no seu dropbox efetuado com sucesso!")
    def is_logged(self):
        return self.dbx is not None

    def login(self):
        auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, use_pkce=True, token_access_type='offline')
        authorize_url = auth_flow.start()
        self.dbx_window = open_centered_window("Login no Dropbox", 550, 250)
        text = "1. Clique no botão Abrir Dropbox\n2. Na página que abrir aperte em \"autorizar\" " \
             "(você pode precisar se logar antes).\n3. Copie o código de autorização e cole na caixa abaixo\n"
        ttk.Label(self.dbx_window, text=text).pack(pady=10)
        ttk.Button(self.dbx_window, text="Abrir Dropbox no seu navegador",
                   command=lambda: webbrowser.open(authorize_url, new=2)).pack(pady=10)
        auth_box = tk.Text(self.dbx_window, height=2, width=30)
        auth_box.pack(pady=10)
        ttk.Button(self.dbx_window, text="Enviar código",
                   command=lambda: self.finish_auth(auth_box, auth_flow)).pack(pady=10)
        self.dbx_window.lift()
        self.dbx_window.attributes('-topmost', True)
        self.dbx_window.attributes('-topmost', False)
        self.dbx_window.mainloop()

    def download_file(self):
        self.dbx.files_download_to_file(LOCAL_PATH, DROPBOX_PATH, rev=None)

    def upload_file(self):

        try:
            with open(LOCAL_PATH, 'rb') as f:
                meta = self.dbx.files_upload(f.read(), DROPBOX_PATH, mode=WriteMode("overwrite"))
                return meta

        except Exception as e:
            print('Error uploading file to Dropbox: ' + str(e))
