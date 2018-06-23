"""Adapted from https://stackoverflow.com/a/21912744/812183"""
from __future__ import absolute_import
from __future__ import unicode_literals

from collections import OrderedDict

import yaml

MAP_TYPE = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG


def load_map(loader, node):
    loader.flatten_mapping(node)
    return OrderedDict(loader.construct_pairs(node))


class OrderedLoader(getattr(yaml, 'CSafeLoader', yaml.SafeLoader)):
    pass


OrderedLoader.add_constructor(MAP_TYPE, load_map)


def dump_map(dumper, data):
    return dumper.represent_mapping(MAP_TYPE, data.items())


class OrderedDumper(getattr(yaml, 'CSafeDumper', yaml.SafeDumper)):
    pass


OrderedDumper.add_representer(OrderedDict, dump_map)


def ordered_load(stream):
    """yaml.load which respects order for dictionaries in the yaml file.

    :param stream: string or streamlike object.
    """
    return yaml.load(stream, Loader=OrderedLoader)


def ordered_dump(obj, **kwargs):
    """yaml.dump which respects order for dictionaries in the yaml object.

    :param obj: Yaml dumpable object
    """
    return yaml.dump(obj, Dumper=OrderedDumper, **kwargs)
