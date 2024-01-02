#!/usr/bin/env python3

import argparse
import cairosvg
import glob
import importlib.util
import jinja2
import json
import os
import re
import shutil
import tempfile
import typing

from utils.color import css_to_rgb, css_to_hsl, shade_css_color
from utils.json import jsonify

def render_binary(path: str, **options: typing.Dict[str, typing.Any]) -> None:
  if path.endswith(".py"):
    # Create module spec
    spec = importlib.util.spec_from_file_location("temporary", path)

    # Load the module
    module = importlib.util.module_from_spec(spec)

    # Execute module
    spec.loader.exec_module(module)

    # Populate global variables
    for (key, value) in options.items():
      module.__dict__[key] = value

    # Call the render function
    rendered = module.render()

    # Write the resulting bytes
    with open(path[:-3], "wb") as file:
      file.write(rendered)

def render_jinja2(path: str, **options: typing.Dict[str, typing.Any]) -> None:
  if path.endswith(".jinja2"):
    # Read input file
    with open(path, "r") as file:
      template = jinja2.Template(file.read())

    # Render template
    rendered = template.render(**options)

    # Write output file
    with open(path[:-7], "w") as file:
      file.write(rendered)

def render_svg(path: str, *, sizes: typing.List[int] = [ 16, 32, 64 ]) -> None:
  if path.endswith(".svg"):
    for size in sizes:
      # Create new path like filename@16.png
      new_path = f"{path[:-4]}@{size}.png"

      # Render svg
      cairosvg.svg2png(url=path, output_width=size, output_height=size, write_to=new_path)

def build(source_path: str, target_path: str, manifest_path: str) -> None:
  with open(manifest_path, "r") as file:
    manifest = json.load(file)

  with tempfile.TemporaryDirectory() as tmp_dir:
    # Remove temporary directory
    shutil.rmtree(tmp_dir)

    # Copy template directory
    shutil.copytree(source_path, tmp_dir)

    # Render binary files
    for path in glob.glob(os.path.join(tmp_dir, "**", "*.py"), recursive=True):
      # Render binary
      render_binary(path, css_to_rgb=css_to_rgb, css_to_hsl=css_to_hsl, jsonify=jsonify, manifest=manifest, shade_css_color=shade_css_color)

      # Remove source file
      os.remove(path)

    # Render template files
    for path in glob.glob(os.path.join(tmp_dir, "**", "*.jinja2"), recursive=True):
      # Render template
      render_jinja2(path, css_to_rgb=css_to_rgb, css_to_hsl=css_to_hsl, jsonify=jsonify, manifest=manifest, shade_css_color=shade_css_color)

      # Remove source file
      os.remove(path)

    # Render svg files
    for path in glob.glob(os.path.join(tmp_dir, "**", "*.svg"), recursive=True):
      # Render svg
      render_svg(path)

      # Remove source file
      os.remove(path)

    # Remove __pycache__ directories
    for path in glob.glob(os.path.join(tmp_dir, "**", "__pycache__"), recursive=True):
      # Remove directory
      shutil.rmtree(path)

    # Theme name
    theme_name = manifest["displayName"].lower() + "_" + ("dark" if manifest["dark"] else "light")

    # Theme type
    theme_type = ("base" if source_path.endswith("doki_theme_base") else
                  "chrome" if source_path.endswith("doki_theme_chrome") else
                  "firefox" if source_path.endswith("doki_theme_firefox") else
                  "unknown")

    # Remove invalid symbols
    theme_name = re.sub(r"[^a-z0-9_]", "", theme_name)

    # Create output path
    output_path = os.path.join(target_path, f"doki_theme_{theme_name}_{theme_type}")

    # Create archive
    shutil.make_archive(output_path, "zip", tmp_dir)

def main():
  # Argument parser setup
  parser = argparse.ArgumentParser()
  parser.add_argument("-m", "--manifest", type=str, required=True, help="theme definition")
  parser.add_argument("-t", "--type", choices=["base", "chrome", "firefox"], required=True, help="output type")
  parser.add_argument("-o", "--output", type=str, default="out", help="output directory")

  # Command line arguments
  args = parser.parse_args()

  # Get template directory
  template = (os.path.join("template", "doki_theme_base") if args.type == "base" else
              os.path.join("template", "doki_theme_chrome") if args.type == "chrome" else
              os.path.join("template", "doki_theme_firefox") if args.type == "firefox" else
              os.path.join("template", "invalid"))

  # Build theme
  build(template, args.output, args.manifest)

if __name__ == "__main__":
  main()
