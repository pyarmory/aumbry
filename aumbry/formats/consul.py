import time
from six.moves.urllib.parse import urljoin

from aumbry.formats import yml
from aumbry.errors import LoadError


class ConsulHandler(yml.YamlHandler):
    extras_name = 'consul'

    @property
    def imports(self):
        return ['yaml', 'requests']

    @property
    def environment_var_prefix(self):
        return 'CONSUL'

    def fetch_config_data(self):
        import requests

        consul_uri = self.vars['CONSUL_URI']
        consul_key = self.vars['CONSUL_KEY']
        timeout = self.vars.get('CONSUL_TIMEOUT', 10)
        retries = self.vars.get('CONSUL_RETRY_MAX', 1)
        interval = self.vars.get('CONSUL_RETRY_INTERVAL', 10)

        full_uri = urljoin(consul_uri, '/v1/kv/{}'.format(consul_key))

        tries = 0
        while tries <= retries:
            tries += 1
            resp = requests.get(full_uri, timeout=timeout)
            if resp.status_code == 200:
                return resp.content
            elif resp.status_code == 404:
                raise LoadError(
                    'Consul returned 404 when fetching {}'.format(full_uri)
                )

            time.sleep(interval)

        # If we've made it this far... boom!
        msg = ('Hit max retry attempts. Consul returned {} when '
               'fetching {}').format(resp.status_code, full_uri)
        raise LoadError(msg)
