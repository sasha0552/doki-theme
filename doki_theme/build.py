#!/usr/bin/env python3

from argparse import ArgumentParser
from json import load
from re import compile
from typing import List, Tuple
from zipfile import ZipFile

from utils.doki.archive import copy_text_to_archive, copy_bytes_to_archive, render_svg_to_archive
from utils.doki.image import build_inactive_tab_image, build_active_tab_image
from utils.color import shade_css_color

def build_base(replacements: List[Tuple[str, str]], output_path: str) -> None:
  with ZipFile(output_path, "w") as archive:
    # Copy files
    copy_text_to_archive(archive, "template/doki_theme_base/css/scrollbar.css", "css/scrollbar.css", replacements=replacements)
    copy_text_to_archive(archive, "template/doki_theme_base/css/selection.css", "css/selection.css", replacements=replacements)
    copy_text_to_archive(archive, "template/doki_theme_base/css/tab.css", "css/tab.css", replacements=replacements)
    copy_text_to_archive(archive, "template/doki_theme_base/html/tab.html", "html/tab.html", replacements=replacements)
    copy_text_to_archive(archive, "template/doki_theme_base/manifest.json", "manifest.json", replacements=replacements)

    # Copy background
    # TODO

    # Render icon
    render_svg_to_archive(archive, "template/doki_theme_base/images/icon.svg", "images/doki-theme-logo@16.png", replacements=replacements, size=16)
    render_svg_to_archive(archive, "template/doki_theme_base/images/icon.svg", "images/doki-theme-logo@32.png", replacements=replacements, size=32)
    render_svg_to_archive(archive, "template/doki_theme_base/images/icon.svg", "images/doki-theme-logo@64.png", replacements=replacements, size=64)

def build_chrome(replacements: List[Tuple[str, str]], output_path: str) -> None:
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

def build_firefox(replacements: List[Tuple[str, str]], output_path: str) -> None:
  with ZipFile(output_path, "w") as archive:
    # Copy files
    copy_text_to_archive(archive, "template/doki_theme_firefox/manifest.json", "manifest.json", replacements=replacements)

    # Render icon
    render_svg_to_archive(archive, "template/doki_theme_firefox/images/icon.svg", "images/doki-theme-logo@16.png", replacements=replacements, size=16)
    render_svg_to_archive(archive, "template/doki_theme_firefox/images/icon.svg", "images/doki-theme-logo@32.png", replacements=replacements, size=32)
    render_svg_to_archive(archive, "template/doki_theme_firefox/images/icon.svg", "images/doki-theme-logo@64.png", replacements=replacements, size=64)

def main():
  # Argument parser setup
  parser = ArgumentParser()
  parser.add_argument("-m", "--manifest", type=str, required=True, help="theme defination")
  parser.add_argument("-t", "--type", choices=["base", "chrome", "firefox"], required=True, help="output type")
  parser.add_argument("-o", "--output", type=str, required=True, help="output path")

  # Command line arguments
  args = parser.parse_args()

  # Read manifest as json
  with open(args.manifest, "r") as file:
    manifest = load(file)

  # Create replacements array
  replacements = []

  # Add every color as replacement source
  for key, value in manifest["colors"].items():
    replacements.append((compile(f"&{key}&"), value))

  # Add shaded accent color, if accent color is present
  if "accentColor" in manifest["colors"]:
    replacements.append((r"&_accentColorShade&", shade_css_color(manifest["colors"]["accentColor"], -0.01)))

  # Add default contrast color, if not present
  if "iconContrastColor" not in manifest["colors"]:
    replacements.append((r"&iconContrastColor&", "#fff"))

  # Build theme based on type
  if args.type == "base":
    build_base(replacements, args.output)
  elif args.type == "chrome":
    build_chrome(replacements, args.output)
  elif args.type == "firefox":
    build_firefox(replacements, args.output)

if __name__ == "__main__":
  main()
