import os
import yaml

CONFIG_DIR = os.getenv('CONFIG_DIRECTORY_NAME', 'config')
CONF = {}
for file in os.listdir(CONFIG_DIR):
    if '.yml' in file:
        with open(f'{CONFIG_DIR}/{file}', 'r') as config_stream:
            CONF.update(yaml.safe_load(config_stream))

# Kubernetes liveness and readiness check endpoints
KUBERNETES_LIVENESS_CHECK = CONF.get('kubernetes_liveness_check', '/healthz')
KUBERNETES_READINESS_CHECK = CONF.get('kubernetes_readiness_check', '/readyz')

# Page URLs
SIGN_IN_URL = '/sign-in'
SIGN_OUT_URL = '/sign-out'
MAIN_HOME_URL = '/'
HOME_URL = '/<app_name>/'

# App Endpoints
APP_URL = '/app'