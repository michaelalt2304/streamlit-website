import os

creds_ls = os.listdir('creds')

creds_ls.remove('application_default_credentials.json')

creds_path = './creds/' + creds_ls[0]


INSTANCE_CONNECTION_NAME = "project-2-test-with-new-creds:us-central1:root"
PROJECT_NAME = INSTANCE_CONNECTION_NAME.rsplit(':')[0]
print(PROJECT_NAME)