from copy import deepcopy
from logging import Filter

import ujson
from pythonjsonlogger.json import JsonFormatter

from stobox_dependencies.settings.conf import Env
from stobox_dependencies.settings.conf import settings
from stobox_dependencies.settings.router import request_id_var
from stobox_dependencies.settings.router import session_id_var
from stobox_dependencies.settings.router import user_ref_var


class TracingFilter(Filter):
    def filter(self, record):
        if isinstance(record.msg, dict):
            record.msg['session_id'] = session_id_var.get()
            record.msg['request_id'] = request_id_var.get()
            record.msg['user_ref'] = user_ref_var.get()
        return True


class BaseJsonFormatter(JsonFormatter):
    SECURE_PARAMETERS = ('secret',)

    def add_fields(self, log_record, record, message_dict):
        super(BaseJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['level'] = record.levelname
        log_record['logger'] = record.name
        if isinstance(record.msg, dict):
            log_record['json'] = self._filter_json(deepcopy(record.msg.get('json', {})))
            log_record['text'] = self._filter_text(deepcopy(record.msg.get('text', '')))

    def _filter_json(self, json_log: dict) -> dict:
        if json_log and isinstance(json_log, dict):
            for key, value in json_log.copy().items():
                if key in self.SECURE_PARAMETERS:
                    json_log[key] = '***'

                if isinstance(value, dict):
                    json_log[key] = self._filter_json(value)
        return json_log

    def _filter_text(self, json_log: str) -> str:
        if isinstance(json_log, str):
            try:
                log = ujson.loads(json_log or '{}')
            except ujson.JSONDecodeError:
                log = json_log
        else:
            log = json_log

        filtered_log = self._filter_json(log)
        return ujson.dumps(log or filtered_log)


log_level = settings.LOG_LEVEL

LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': BaseJsonFormatter,
        },
        'local': {
            '()': 'logging.Formatter',
        },
    },
    'filters': {
        'tracing': {
            '()': TracingFilter,
        },
    },
    'handlers': {
        'default': {
            'formatter': 'local' if settings.ENV == Env.LOCAL else 'json',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'filters': ['tracing'],
        },
    },
    'loggers': {
        'uvicorn': {'handlers': ['default'], 'level': log_level},
        'gunicorn': {'handlers': ['default'], 'level': log_level},
        'gunicorn.access': {'handlers': ['default'], 'level': log_level},
        'gunicorn.error': {'handlers': ['default'], 'level': log_level},
    },
    'root': {'handlers': ['default'], 'level': log_level},
}
