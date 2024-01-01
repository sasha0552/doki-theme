from cairosvg import svg2png
from re import Pattern
from typing import List, Tuple
from zipfile import ZipFile

from utils.doki.string import replace_placeholders

def copy_text_to_archive(archive: ZipFile, source_path: str, target_path: str, replacements: List[Tuple[Pattern, str]] = []) -> None:
  with open(source_path, "r") as source_file:
    with archive.open(target_path, "w") as destination_file:
      # Read source file content
      content = source_file.read()

      # Replace placeholders
      content = replace_placeholders(content, replacements)

      # Convert content to bytes
      content = content.encode("utf-8")

      # Write content to target file in the archive
      destination_file.write(content)

def copy_bytes_to_archive(archive: ZipFile, source_bytes: bytes, target_path: str) -> None:
  with archive.open(target_path, "w") as destination_file:
    # Write bytes content to target file in the archive
    destination_file.write(source_bytes)

def render_svg_to_archive(archive: ZipFile, source_path: str, target_path: str, replacements: List[Tuple[Pattern, str]] = [], size: int = 128) -> None:
  with open(source_path, "r") as source_file:
    with archive.open(target_path, "w") as destination_file:
      # Read source file content
      content = source_file.read()

      # Replace placeholders
      content = replace_placeholders(content, replacements)

      # Convert content to bytes
      content = content.encode("utf-8")

      # Convert SVG to PNG
      content = svg2png(bytestring=content, output_width=size, output_height=size)

      # Write content to target file in the archive
      destination_file.write(content)
