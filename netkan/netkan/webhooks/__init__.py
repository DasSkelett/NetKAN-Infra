import os
import sys
from pathlib import Path
import boto3
from flask import Flask

from ..notifications import setup_log_handler, catch_all
from .config import current_config
from .errors import errors
from .inflate import inflate
from .spacedock_inflate import spacedock_inflate
from .spacedock_add import spacedock_add
from .github_inflate import github_inflate
from .github_mirror import github_mirror


class NetkanWebhooks(Flask):

    def __init__(self) -> None:
        super().__init__(__name__)

        # Set up Discord logger so we can see errors
        if setup_log_handler():
            sys.excepthook = catch_all

        # Add the hook handlers
        self.register_blueprint(errors)
        self.register_blueprint(inflate)
        self.register_blueprint(spacedock_inflate, url_prefix='/sd')
        self.register_blueprint(spacedock_add, url_prefix='/sd')
        self.register_blueprint(github_inflate, url_prefix='/gh')
        self.register_blueprint(github_mirror, url_prefix='/gh')


def create_app() -> NetkanWebhooks:
    # Set config values for other modules to retrieve
    current_config.setup(
        os.environ.get('SSH_KEY', ''),
        os.environ.get('XKAN_GHSECRET', ''),
        os.environ.get('NETKAN_REMOTE', ''), '/tmp/NetKAN',
        os.environ.get('CKANMETA_REMOTE', ''), '/tmp/CKAN-meta',
        os.environ.get('INFLATION_SQS_QUEUE', ''),
        os.environ.get('ADD_SQS_QUEUE', ''),
        os.environ.get('MIRROR_SQS_QUEUE', '')
    )
    return NetkanWebhooks()
