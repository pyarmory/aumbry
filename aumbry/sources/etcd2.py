import base64
import time
from six.moves.urllib.parse import urljoin

from aumbry.contract import AbstractSource
from aumbry.errors import LoadError, SaveError
from aumbry.sources import SourceTypes
from aumbry.utils.data import b64decode_if_possible


class Etcd2Source(AbstractSource):
    extras_name = SourceTypes.etcd2

    def _build_uri(self, base, key):
        return urljoin(base, '/v2/keys/{}'.format(key))

    @property
    def imports(self):
        return ['requests']

    @property
    def environment_var_prefix(self):
        return 'ETCD2'

    def fetch_config_data(self):
        import requests

        base_uri = self.vars['ETCD2_URI']
        etcd_key = self.vars['ETCD2_KEY']
        timeout = self.vars.get('ETCD2_TIMEOUT', 10)
        retries = self.vars.get('ETCD2_RETRY_MAX', 1)
        interval = self.vars.get('ETCD2_RETRY_INTERVAL', 10)

        full_uri = self._build_uri(base_uri, etcd_key)

        tries = 0
        while tries <= retries:
            tries += 1
            resp = requests.get(full_uri, timeout=timeout)
            if resp.status_code == 200:
                node = resp.json().get('node', {})
                data = node.get('value')
                return b64decode_if_possible(data)
            elif resp.status_code >= 400 and resp.status_code <= 499:
                raise LoadError(
                    'Etcd returned {} when fetching {}'.format(
                        resp.status_code,
                        full_uri
                    )
                )

            time.sleep(interval)

        # If we've made it this far... boom!
        msg = ('Hit max retry attempts. Etcd returned {} when '
               'fetching {}').format(resp.status_code, full_uri)
        raise LoadError(msg)

    def save_config_data(self, data, handler):
        import requests

        base_uri = self.vars['ETCD2_URI']
        etcd_key = self.vars['ETCD2_KEY']
        full_uri = self._build_uri(base_uri, etcd_key)

        to_save = base64.b64encode(data.encode('utf-8'))
        resp = requests.put(full_uri, data={'value': to_save})

        if resp.status_code != 201:
            raise SaveError(
                'Etcd returned {} when attempting to save {}'.format(
                    resp.status_code,
                    full_uri
                )
            )

        return resp.json()
