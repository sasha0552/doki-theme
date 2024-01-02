import os

def render() -> bytes:
  with open(os.path.join("upstream", "doki-theme-assets", "backgrounds", manifest["stickers"]["default"]["name"]), "rb") as file:
    return file.read()
