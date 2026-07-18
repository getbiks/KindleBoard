import yaml

class Config:

    def __init__(self):
        with open("config.yaml", "r") as f:
            self.data = yaml.safe_load(f)

    def get(self, *keys, default=None):
        value = self.data

        for key in keys:
            if key not in value:
                return default
            value = value[key]

        return value

config = Config()
