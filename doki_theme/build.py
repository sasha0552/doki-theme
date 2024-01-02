#!/usr/bin/env python3

from argparse import ArgumentParser
from json import load
from os import makedirs, path
from re import sub
from sys import stderr
from typing import Dict
from zipfile import ZipFile

from utils.doki.archive import copy_binary_to_archive, copy_bytes_to_archive, copy_text_to_archive, render_svg_to_archive
from utils.doki.image import build_inactive_tab_image, build_active_tab_image
from utils.color import css_to_rgb, shade_css_color

def build_base(replacements: Dict[str, str], output_path: str, *, background: str, theme_name: str) -> None:
  with ZipFile(output_path, "w") as archive:
    # Copy files
    copy_text_to_archive(archive, "template/doki_theme_base/css/scrollbar.css", "css/scrollbar.css", replacements=replacements)
    copy_text_to_archive(archive, "template/doki_theme_base/css/selection.css", "css/selection.css", replacements=replacements)
    copy_text_to_archive(archive, "template/doki_theme_base/css/tab.css", "css/tab.css", replacements=replacements)
    copy_text_to_archive(archive, "template/doki_theme_base/html/tab.html", "html/tab.html", replacements=replacements)
    copy_text_to_archive(archive, "template/doki_theme_base/manifest.json", "manifest.json", replacements=replacements)

    # Copy background
    if background is not None and theme_name is not None:
      if path.exists(background):
        copy_binary_to_archive(archive, background, f"images/backgrounds/{theme_name}.png")
      else:
        print(f"Background {background} is not exists!", file=stderr)

    # Render icon
    render_svg_to_archive(archive, "template/doki_theme_base/images/icon.svg", "images/doki-theme-logo@16.png", replacements=replacements, size=16)
    render_svg_to_archive(archive, "template/doki_theme_base/images/icon.svg", "images/doki-theme-logo@32.png", replacements=replacements, size=32)
    render_svg_to_archive(archive, "template/doki_theme_base/images/icon.svg", "images/doki-theme-logo@64.png", replacements=replacements, size=64)

def build_chrome(replacements: Dict[str, str], output_path: str) -> None:
  with ZipFile(output_path, "w") as archive:
    # Copy files
    copy_text_to_archive(archive, "template/doki_theme_chrome/manifest.json", "manifest.json", replacements=replacements)

    # Render tab images
    copy_bytes_to_archive(archive, build_active_tab_image(replacements["highlightColor"], replacements["accentColor"]), "images/tab_inactive.png")
    copy_bytes_to_archive(archive, build_inactive_tab_image(replacements["baseBackground"]), "images/tab_highlight.png")

    # Render icon
    render_svg_to_archive(archive, "template/doki_theme_chrome/images/icon.svg", "images/doki-theme-logo@16.png", replacements=replacements, size=16)
    render_svg_to_archive(archive, "template/doki_theme_chrome/images/icon.svg", "images/doki-theme-logo@32.png", replacements=replacements, size=32)
    render_svg_to_archive(archive, "template/doki_theme_chrome/images/icon.svg", "images/doki-theme-logo@64.png", replacements=replacements, size=64)

def build_firefox(replacements: Dict[str, str], output_path: str) -> None:
  with ZipFile(output_path, "w") as archive:
    # Copy files
    copy_text_to_archive(archive, "template/doki_theme_firefox/manifest.json", "manifest.json", replacements=replacements)

    # Render icon
    render_svg_to_archive(archive, "template/doki_theme_firefox/images/icon.svg", "images/doki-theme-logo@16.png", replacements=replacements, size=16)
    render_svg_to_archive(archive, "template/doki_theme_firefox/images/icon.svg", "images/doki-theme-logo@32.png", replacements=replacements, size=32)
    render_svg_to_archive(archive, "template/doki_theme_firefox/images/icon.svg", "images/doki-theme-logo@64.png", replacements=replacements, size=64)

def build(manifest: str, type: str, output: str):
  # Read manifest as json
  with open(manifest, "r") as file:
    manifest = load(file)

  # Create replacements dictionary
  replacements = {}

  # Add every color as replacement source
  for key, value in manifest["colors"].items():
    replacements[key] = value

  # Same, but rgb variant instead of css
  for key, value in manifest["colors"].items():
    # Extract red, green, and blue
    (r, g, b) = css_to_rgb(value)

    # Assign replacement
    replacements["_rgb_" + key] = f"[{r}, {g}, {b}]"

  # Add shaded accent color, if accent color is present
  if "accentColor" in manifest["colors"]:
    replacements["_accentColorShade"] = shade_css_color(manifest["colors"]["accentColor"], -0.01)

  # Add default contrast color, if not present
  if "iconContrastColor" not in manifest["colors"]:
    replacements["iconContrastColor"] = "#fff"

  # Theme name
  theme_name = manifest["displayName"].lower() + "_" + ("dark" if manifest["dark"] else "light")

  # Remove invalid symbols
  theme_name = sub(r"[^a-z0-9_]", "", theme_name)

  # Background name
  background_name = manifest["stickers"]["default"]["name"][:-4]

  # Output path
  output_path = path.join(output, f"doki_theme_{theme_name}_{type}.zip")

  # Background path
  background_path = path.join("upstream", "doki-theme-assets", "backgrounds", f"{background_name}.png")

  # Create output directory
  makedirs(output, exist_ok=True)

  # Add background name to replacements
  replacements["_backgroundName"] = background_name

  # Build theme based on type
  if type == "base":
    build_base(replacements, output_path, background=background_path, theme_name=background_name)
  elif type == "chrome":
    build_chrome(replacements, output_path)
  elif type == "firefox":
    build_firefox(replacements, output_path)

def main():
  # Argument parser setup
  parser = ArgumentParser()
  parser.add_argument("-m", "--manifest", type=str, required=True, help="theme definition")
  parser.add_argument("-t", "--type", choices=["base", "chrome", "firefox"], required=True, help="output type")
  parser.add_argument("-o", "--output", type=str, default="out", help="output directory")

  # Command line arguments
  args = parser.parse_args()

  # Build theme
  build(args.manifest, args.type, args.output)

if __name__ == "__main__":
  main()
