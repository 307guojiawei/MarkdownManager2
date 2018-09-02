import re
import os
import tempfile

class Config:
    def __init__(self):
        self.path = str(os.path.dirname(os.path.realpath(__file__)))
        self.properties = Properties(os.path.join(self.path, '../config.properties'))
        self.properties.put("ProjectRoot",str(self.path)+"/../")

    def __new__(cls, *args, **kwargs):
        if not hasattr(Config, "_instance"):
            if not hasattr(Config, "_instance"):
                Config._instance = object.__new__(cls)
        return Config._instance


class Properties:
    def __init__(self, file_name):
        self.file_name = file_name
        self.properties = {}
        try:
            fopen = open(self.file_name, 'r')
            for line in fopen:
                line = line.strip()
                if line.find('=') > 0 and not line.startswith('#'):
                    strs = line.split('=')
                    self.properties[strs[0].strip()] = strs[1].strip()
        except Exception as e:
            raise e
        else:
            fopen.close()

    def has_key(self, key):
        return key in self.properties

    def get(self, key, default_value=''):
        if key in self.properties:
            return self.properties[key]
        return default_value

    def put(self, key, value):
        self.properties[key] = value
        self.flush()

    def flush(self):
        with open(self.file_name,"w") as f:
            for key,value in self.properties.items():
                buf = str(key)+"="+str(value)+"\n"
                f.write(buf)
