#!/usr/bin/env python3

from argparse import ArgumentParser
from glob import glob

from build import build

def main():
  # Argument parser setup
  parser = ArgumentParser()
  parser.add_argument("-o", "--output", type=str, default="out", help="output directory")

  # Command line arguments
  args = parser.parse_args()

  # Build themes
  for manifest in glob("upstream/doki-theme-master/definitions/**/*.definition.json", recursive=True):
    for type in [ "base", "firefox", "chrome" ]:
      build(manifest, type, args.output)

if __name__ == "__main__":
  main()
