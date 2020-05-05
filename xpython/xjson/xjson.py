"""
Extended JSON library including schema validation and date handling.
"""

import datetime
import json
import logging

from jsonschema import validate
import numpy as np

from common import misc


_log = logging.getLogger(__name__)


def hooks(o):
    """
    Hook that permits converting a datetime object ot its stringified version
    for serialization.
    """
    if isinstance(o, datetime.datetime):
        return o.strftime(misc.DT_STR)
    if isinstance(o, (
        np.int_, np.intc, np.intp, np.int8,
        np.int16, np.int32, np.int64, np.uint8,
        np.uint16, np.uint32, np.uint64
    )):
        return int(o)
    if isinstance(o, (np.float_, np.float16, np.float32, np.float64)):
        return float(o)
    if isinstance(o, (np.ndarray,)):
        return o.tolist()


def dumps(filepath, object, indent=2, hooks=None):
    """
    Extended version for json.dumps that includes custom hooks for supporting
    serializing complex objects.
    """
    with open(filepath, 'w') as f:
        f.write(json.dumps(object, indent=indent, default=hooks))


def loads(filepath, schemapath=None):
    """
    This function loads a JSON file validating its contents against a given schema.
    For the validation, the library "jsonschema" is used.
    """

    with open(filepath, 'r') as file:
        json_object = json.load(file)

    if schemapath:
        _log.info(f"Validating <{filepath}> with <{schemapath}>")
        with open(schemapath, 'r') as file:
            json_schema = json.load(file)
        validate(instance=json_object, schema=json_schema)

    return json_object
