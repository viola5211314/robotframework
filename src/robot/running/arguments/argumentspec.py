#  Copyright 2008-2015 Nokia Networks
#  Copyright 2016-     Robot Framework Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import sys

from .argumentmapper import ArgumentMapper
from .argumentresolver import ArgumentResolver
from .typeconverter import TypeConverter


class ArgumentSpec(object):

    def __init__(self, name=None, type='Keyword', positional=None,
                 defaults=None, varargs=None, kwargs=None, kwonlyargs=None,
                 kwonlydefaults=None, annotations=None, supports_named=True):
        self.name = name
        self.type = type
        self.positional = positional or []
        self.defaults = defaults or []
        self.varargs = varargs
        self.kwargs = kwargs
        self.supports_named = supports_named
        self.kwonlyargs = kwonlyargs or []
        self.kwonlydefaults = kwonlydefaults or {}
        self.annotations = annotations or {}

    @property
    def minargs(self):
        return len(self.positional) - len(self.defaults)

    @property
    def maxargs(self):
        return len(self.positional) if not self.varargs else sys.maxsize

    @property
    def reqkwargs(self):
        return set(self.kwonlyargs) - set(self.kwonlydefaults)

    # FIXME: Change ArgumentSpec.defaults to be a mapping and then remove this.
    @property
    def default_values(self):
        return dict(zip(self.positional[self.minargs:], self.defaults))

    def resolve(self, arguments, variables=None, resolve_named=True,
                resolve_variables_until=None, dict_to_kwargs=False):
        resolver = ArgumentResolver(self, resolve_named,
                                    resolve_variables_until, dict_to_kwargs)
        positional, named = resolver.resolve(arguments, variables)
        if self.annotations or self.defaults:
            converter = TypeConverter(self)
            positional, named = converter.convert(positional, named)
        return positional, named

    def map(self, positional, named, replace_defaults=True):
        mapper = ArgumentMapper(self)
        return mapper.map(positional, named, replace_defaults)
