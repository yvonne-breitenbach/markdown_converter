#!/usr/bin/env python3
"""
DOCX to Markdown Converter

Converts DOCX files to Markdown format using the docling library.
Reads input file paths from config.ini and processes all uncommented entries.
"""

import os
import sys
import configparser
from pathlib import Path
from typing import List, Tuple

from docling.document_converter import DocumentConverter, WordFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PaginatedPipelineOptions
from docling_core.types.doc import ImageRefMode


# Configuration
INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
CONFIG_FILE = INPUT_DIR / "config.ini"


def parse_config() -> List[str]:
    """
    Parse config.ini and extract uncommented file entries.

    Returns:
        List of file paths to process

    Raises:
        FileNotFoundError: If config.ini doesn't exist
        configparser.Error: If config.ini is malformed
    """
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Configuration file not found: {CONFIG_FILE}")

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    files_to_process = []

    if "FILES" not in config:
        raise ValueError("Config file must contain a [FILES] section")

    for key, value in config["FILES"].items():
        # Filter out empty values and commented lines
        if value and not value.strip().startswith("#"):
            files_to_process.append(value.strip().strip('"'))

    return files_to_process


def get_base_name(file_path: str) -> str:
    """
    Extract base name from file path without extension.

    Args:
        file_path: Path to the file

    Returns:
        Base name without extension
    """
    return Path(file_path).stem


def convert_docx_to_markdown(docx_path: Path, output_base_name: str) -> Tuple[bool, str]:
    """
    Convert a DOCX file to Markdown with image extraction.

    Args:
        docx_path: Path to the input DOCX file
        output_base_name: Base name for output files

    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        print(f"\n{'='*60}")
        print(f"Converting: {docx_path.name}")
        print(f"{'='*60}")

        # Ensure output directory exists
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # Configure pipeline options for DOCX with image extraction
        print("Configuring pipeline for image extraction...")
        pipeline_options = PaginatedPipelineOptions()
        pipeline_options.generate_picture_images = True
        pipeline_options.images_scale = 2.0  # Higher resolution images

        # Initialize converter with DOCX format options
        print("Initializing document converter...")
        converter = DocumentConverter(
            format_options={
                InputFormat.DOCX: WordFormatOption(
                    pipeline_options=pipeline_options
                )
            }
        )

        # Convert document
        print("Converting document...")
        result = converter.convert(str(docx_path))

        # Save as markdown with referenced images
        # Docling will create a {basename}_artifacts directory automatically
        print("Exporting to markdown with image extraction...")
        markdown_path = OUTPUT_DIR / f"{output_base_name}.md"

        # Use save_as_markdown to properly export images
        result.document.save_as_markdown(
            str(markdown_path),
            image_mode=ImageRefMode.REFERENCED
        )

        # Handle the nested directory structure created by docling
        # Docling creates: output/output/{basename}_artifacts/
        # We want: output/{basename}_images/
        nested_artifacts_dir = OUTPUT_DIR / "output" / f"{output_base_name}_artifacts"
        images_dir = OUTPUT_DIR / f"{output_base_name}_images"

        if nested_artifacts_dir.exists():
            # Remove old images directory if it exists
            if images_dir.exists():
                import shutil
                shutil.rmtree(images_dir)

            # Move nested artifacts to the correct location
            import shutil
            shutil.move(str(nested_artifacts_dir), str(images_dir))
            print(f"✓ Moved images to: {images_dir.name}")

            # Clean up the extra "output" directory if it's empty
            nested_output_dir = OUTPUT_DIR / "output"
            if nested_output_dir.exists() and not any(nested_output_dir.iterdir()):
                nested_output_dir.rmdir()

        # Update markdown file to use relative paths
        if markdown_path.exists():
            markdown_content = markdown_path.read_text(encoding="utf-8")
            # Replace "output/{basename}_artifacts/" with "{basename}_images/"
            updated_content = markdown_content.replace(
                f"output/{output_base_name}_artifacts/",
                f"{output_base_name}_images/"
            )
            markdown_path.write_text(updated_content, encoding="utf-8")

        print(f"✓ Markdown saved to: {markdown_path}")
        print(f"✓ Images saved to: {images_dir}")

        # Count extracted images
        if images_dir.exists():
            image_files = list(images_dir.glob("**/*.png")) + list(images_dir.glob("**/*.jpg")) + list(images_dir.glob("**/*.jpeg"))
            print(f"✓ Extracted {len(image_files)} image(s)")
        else:
            image_files = []
            print("✓ No images found in this document")

        return True, f"Successfully converted {docx_path.name} with {len(image_files)} image(s)"

    except FileNotFoundError as e:
        return False, f"File not found: {e}"
    except Exception as e:
        return False, f"Conversion failed: {type(e).__name__}: {e}"


def main():
    """Main entry point for the converter."""
    print("\n" + "="*60)
    print("DOCX to Markdown Converter")
    print("="*60)

    try:
        # Parse configuration
        print(f"\nReading configuration from: {CONFIG_FILE}")
        files = parse_config()

        if not files:
            print("\n⚠ No files to process. Check your config.ini file.")
            return 0

        print(f"Found {len(files)} file(s) to process:")
        for i, file in enumerate(files, 1):
            print(f"  {i}. {file}")

        # Process each file
        success_count = 0
        failure_count = 0

        for file_name in files:
            file_path = INPUT_DIR / file_name

            if not file_path.exists():
                print(f"\n✗ Error: File not found - {file_path}")
                failure_count += 1
                continue

            base_name = get_base_name(file_name)
            success, message = convert_docx_to_markdown(file_path, base_name)

            if success:
                success_count += 1
                print(f"✓ {message}")
            else:
                failure_count += 1
                print(f"✗ {message}")

        # Print summary
        print("\n" + "="*60)
        print("Conversion Summary")
        print("="*60)
        print(f"Total files processed: {len(files)}")
        print(f"✓ Successful: {success_count}")
        print(f"✗ Failed: {failure_count}")
        print("="*60 + "\n")

        return 0 if failure_count == 0 else 1

    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        return 1
    except ValueError as e:
        print(f"\n✗ Configuration Error: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected Error: {type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
