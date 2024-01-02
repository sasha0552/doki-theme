#!/usr/bin/env python3

import argparse
import glob
import os

from build import build

def main():
  # Argument parser setup
  parser = argparse.ArgumentParser()
  parser.add_argument("-o", "--output", type=str, default="out", help="output directory")

  # Command line arguments
  args = parser.parse_args()

  # Build themes
  for manifest in glob.glob(os.path.join("upstream", "doki-theme-master", "definitions", "**", "*.definition.json"), recursive=True):
    for template in [ os.path.join("template", "doki_theme_base"), os.path.join("template", "doki_theme_chrome"), os.path.join("template", "doki_theme_firefox") ]:
      # Build theme
      build(template, args.output, manifest)

if __name__ == "__main__":
  main()
