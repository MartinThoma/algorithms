import yaml  # pip install pyyaml is required

with open("example.yaml") as fp:
    data = fp.read()
yaml.unsafe_load(data)
