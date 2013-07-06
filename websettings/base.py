from django.conf import settings
from django.utils.importlib import import_module

from websettings.backends import backend_module


class SettingStoreMetaClass(type):
    def __new__(cls, *args, **kwargs):
        super_new = super(SettingStoreMetaClass, cls).__new__
        new_class = super_new(cls, *args, **kwargs)

        mod_path = settings.WEBSETTINGS_MODULE
        mod = import_module(mod_path)
        new_class.settings = {}

        for setting in dir(mod):
            if setting == setting.upper():
                setting_value = getattr(mod, setting)
                new_class.settings[setting] = setting_value

        return new_class


class SettingStore(object):
    __metaclass__ = SettingStoreMetaClass

    def __getattr__(self, item):
        if item not in self.settings.keys():
            raise AttributeError
        try:
            attr = backend_module.getsetting(item)
        except AttributeError:
            attr = self.settings[item]
        return attr

    def __setattr__(self, key, value):
        if key not in self.settings.keys():
            raise AttributeError
        backend_module.setsetting(key, value)
