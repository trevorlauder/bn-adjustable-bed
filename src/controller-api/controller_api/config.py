import reyaml


def get_config(file: str = "config/config.yml"):
    with open(file) as f:
        return reyaml.load(f.read())
