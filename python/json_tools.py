#
# Copyright (C) 2018 ETH Zurich and University of Bologna
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# 
# Authors: Germain Haugou, ETH (germain.haugou@iis.ee.ethz.ch)
#

import json
from collections import OrderedDict

def import_config(config):
    return config_object(config)

def import_config_from_file(file_path):
    with open(file_path, 'r') as fd:
        config_dict = json.load(fd, object_pairs_hook=OrderedDict)
        return import_config(config_dict)


class config(object):

    def get_str(self):
        pass

    def get_int(self):
        pass

    def get(self, name):
        pass

    def get_elem(self, index):
        pass

    def get_size(self, index):
        pass

    def get_from_list(self, name_list):
        pass

    def get_tree(self, config):
        if type(config) == list:
            return config_array(config)
        elif type(config) == dict or type(config) == OrderedDict:
            return config_object(config)
        elif type(config) == str:
            return config_string(config)
        elif type(config) == bool:
            return config_bool(config)
        else:
            return config_number(config)

    def dump_to_string(self):
        return json.dumps(self.get_dict(), indent='  ')


class config_object(config):

    def __init__(self, config):
        self.items = OrderedDict()

        for key, value in config.items():
            self.items[key] = self.get_tree(value)

    def get_from_list(self, name_list):
        if len(name_list) == 0:
            return self

        result = None
        name_pos = 0
        for item in name_list:
            if item != "*" and item != "**":
                name = item
                break
            name_pos += 1

        for key, value in self.items.items():
            if name == key:
                result = value.get_from_list(name_list[name_pos + 1:])
                if name_pos == 0 or result is not None:
                    return result
            elif name_list[0] == "*":
                result = value.get_from_list(name_list[1:])
                if result is not None:
                    return result
            elif name_list[0] == "**":
                result = value.get_from_list(name_list)
                if result is not None:
                    return result

        return result

    def set_from_list(self, name_list, value):
        key = name_list.pop(0)
        if len(name_list) == 0:
            self.items[key] = self.get_tree(value)
        else:
            if self.items.get(key) is None:
                self.items[key] = config_object({})
            self.items[key].set_from_list(name_list, value)


    def get(self, name):
        return self.get_from_list(name.split('/'))

    def set(self, name, value):
        self.set_from_list(name.split('/'), value)

    def get_dict(self, serialize=True):
        if serialize:
            result = {}
        else:
            result = OrderedDict()
        for key,value in self.items.items():
            result[key] = value.get_dict(serialize=serialize)
        return result

    def get_items(self):
        return self.items


class config_array(config):

    def __init__(self, config):
        self.elems = []
        for elem in config:
            self.elems.append(self.get_tree(elem))

    def get_from_list(self, name_list):
        if len(name_list) == 0:
            return self
        return None

    def get_size(self):
        return len(self.elems)

    def get_elem(self, index):
        return self.elems[index]

    def get_dict(self, serialize=True):
        result = []
        for elem in self.elems:
            result.append(elem.get_dict(serialize=serialize))
        return result


class config_string(config):

    def __init__(self, config):
        self.value = config

    def get_from_list(self, name_list):
        if len(name_list) == 0:
            return self
        return None

    def get(self):
        return self.value

    def get_dict(self, serialize=True):
        return self.value


class config_number(config):

    def __init__(self, config):
        self.value = config

    def get_from_list(self, name_list):
        if len(name_list) == 0:
            return self
        return None

    def get(self):
        return self.value

    def get_dict(self, serialize=True):
        return self.value


class config_bool(config):

    def __init__(self, config):
        self.value = config

    def get_from_list(self, name_list):
        if len(name_list) == 0:
            return self
        return None

    def get(self):
        return self.value

    def get_dict(self, serialize=True):
        return self.value
