import json
from alchemize import JsonMappedModel, JsonTransmuter, Attr
from alchemize.mapping import get_key_paths, get_normalized_map

from aumbry.contract import AbstractSource
from aumbry.sources import SourceTypes
from aumbry.utils.data import nested_dict_set


class Parameter(JsonMappedModel):
    __mapping__ = {
        'Name': Attr('name', str),
        'Type': Attr('type', str),
        'Value': Attr('_value', str),
        'KeyId': Attr('key_id', str),
        'Overwrite': Attr('overwrite', bool),
    }

    def __init__(self, type=None, name=None, value=None, key_id=None):
        self.type = type
        self.name = name
        self._value = value
        self.key_id = key_id
        self.overwrite = True

    @property
    def value(self):
        try:
            return json.loads(self._value)
        except ValueError:
            return self._value


class Metadata(JsonMappedModel):
    __mapping__ = {
        'HTTPStatusCode': Attr('status_code', int),
        'RequestId': Attr('request_id', str),
    }


class ParamsResponse(JsonMappedModel):
    __mapping__ = {
        'Parameters': Attr('parameters', [Parameter]),
        'ResponseMetadata': Attr('metadata', Metadata),
        'NextToken': Attr('next_token', str),
    }


class ParameterStoreSource(AbstractSource):
    extras_name = SourceTypes.parameter_store

    @property
    def imports(self):
        return ['boto3']

    @property
    def environment_var_prefix(self):
        return 'PARAMETER_STORE'

    def fetch_ssm_params(self, ssm, all_names):
        parameters = []

        # Chunk names into groups of 10 (max allowed by AWS)
        chunked_names = [
            all_names[i:i+10]
            for i in range(0, len(all_names), 10)
        ]

        for names in chunked_names:
            resp = JsonTransmuter.transmute_from(
                ssm.get_parameters(
                    Names=names,
                    WithDecryption=True
                ),
                ParamsResponse
            )

            parameters.extend(resp.parameters)

        return parameters

    def params_to_dict(self, params, prefix):
        result = {}
        cleaned = [
            (param.name.rsplit(prefix)[1].lstrip('/'), param.value)
            for param in params
        ]

        for name, value, in cleaned:
            level_names = name.split('/')
            nested_dict_set(result, level_names, value)

        return result

    def dict_to_params(self, input_dict, prefix, source, params):
        mapping = get_normalized_map(source)

        for key, val in input_dict.items():
            path = '{}/{}'.format(prefix, key)

            if isinstance(val, dict) and mapping.get(key).type != dict:
                self.dict_to_params(
                    val,
                    path,
                    mapping.get(key).type,
                    params,
                )

            else:
                if isinstance(val, list) or isinstance(val, dict):
                    val = json.dumps(val)

                params.append(
                    Parameter(
                        type='SecureString',
                        name=path,
                        value=val
                    )
                )

        return params

    def fetch_config_data(self, cfg_class):
        import boto3

        region = self.vars['PARAMETER_STORE_AWS_REGION']
        prefix = self.vars['PARAMETER_STORE_PREFIX']

        access_id = self.vars.get('PARAMETER_STORE_AWS_ACCESS_ID')
        access_secret = self.vars.get('PARAMETER_STORE_AWS_ACCESS_SECRET')
        session_token = self.vars.get('PARAMETER_STORE_AWS_SESSION_TOKEN')

        ssm = boto3.client(
            'ssm',
            region_name=region,
            aws_access_key_id=access_id,
            aws_secret_access_key=access_secret,
            aws_session_token=session_token
        )

        names = get_key_paths(cfg_class, prefix=prefix)

        param_dict = self.params_to_dict(
            self.fetch_ssm_params(ssm, names),
            prefix
        )

        return param_dict

    def save_config_data(self, data, handler, cfg):
        import boto3

        region = self.vars['PARAMETER_STORE_AWS_REGION']
        prefix = self.vars['PARAMETER_STORE_PREFIX']

        access_id = self.vars.get('PARAMETER_STORE_AWS_ACCESS_ID')
        access_secret = self.vars.get('PARAMETER_STORE_AWS_ACCESS_SECRET')
        key_id = self.vars.get('PARAMETER_STORE_AWS_KMS_KEY_ID')

        params = self.dict_to_params(data, prefix, cfg, [])

        ssm = boto3.client(
            'ssm',
            region_name=region,
            aws_access_key_id=access_id,
            aws_secret_access_key=access_secret
        )

        for param in params:
            param.key_id = key_id

            # Because Boto3...
            req_kwargs = JsonTransmuter.transmute_to(
                param,
                to_string=False,
                coerce_values=False
            )
            ssm.put_parameter(**req_kwargs)
