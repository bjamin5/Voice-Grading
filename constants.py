import os
import yaml

CONFIG_DIR = os.getenv('CONFIG_DIRECTORY_NAME', 'config')
CONF = {}
for file in os.listdir(CONFIG_DIR):
    if '.yml' in file:
        with open(f'{CONFIG_DIR}/{file}', 'r') as config_stream:
            CONF.update(yaml.safe_load(config_stream))

SECRETS_DIR = CONF.get('SECRETS_DIR', 'secrets')
SECRETS_CONFIG_KEY_NAME = CONF.get('SECRETS_CONFIG_KEY_NAME', 'SECRETS')
CONF[SECRETS_CONFIG_KEY_NAME] = {}
for file in os.listdir(SECRETS_DIR):
    if '.yml' in file:
        with open(f'{SECRETS_DIR}/{file}', 'r') as secret_stream:
            CONF[SECRETS_CONFIG_KEY_NAME].update(yaml.safe_load(secret_stream))

# Kubernetes liveness and readiness check endpoints
KUBERNETES_LIVENESS_CHECK = '/healthz'
KUBERNETES_READINESS_CHECK = '/readyz'

# Messages
SUCCESS_MESSAGE = 'Success'


