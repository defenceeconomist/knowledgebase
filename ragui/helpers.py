import yaml
def load_conf_file(config_file):
   with open(config_file, "r") as f:
       config = yaml.safe_load(f)
       
   return config
