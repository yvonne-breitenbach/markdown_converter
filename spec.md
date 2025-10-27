# DOCX to Markdown Converter - Specification

## Overview
A simple Python CLI application that converts .docx documents to markdown format using the docling library.

## Requirements

### Functional Requirements
1. Read input file paths from `input/config.ini`
2. Process all uncommented entries in the config file
3. Convert each .docx file to markdown format
4. Extract and save images to `output/<docname>_images/` subdirectories
5. Save markdown files to `output/<docname>.md` with proper image links
6. Handle multiple files in batch mode

### Non-Functional Requirements
- CLI-only interface (no GUI)
- Error handling for missing files and conversion failures
- Clear console output showing conversion progress

## Tech Stack

- **Language**: Python 3.x
- **Conversion Library**: [docling](https://github.com/docling-project/docling)
- **Package Manager**: uv
- **Dependencies Management**: pyproject.toml
- **Environment**: Virtual environment (venv)

## Design Guidelines

### Architecture
- Single-responsibility modules (config parser, converter, file handler)
- File-based configuration (INI format)
- Minimal dependencies (docling + standard library)

### Code Style
- Follow PEP 8 conventions
- Type hints where applicable
- Clear function and variable names
- Error handling with informative messages

### Project Structure
```
markdown_converter/
├── venv/                    # Virtual environment
├── input/
│   ├── config.ini          # Configuration file
│   └── *.docx              # Source documents
├── output/
│   ├── *.md                # Generated markdown files
│   └── *_images/           # Extracted images per document
├── convert_docx.py         # Main converter script
└── pyproject.toml          # Project dependencies
```

## Milestone

### M1: MVP - Basic Conversion (v1.0)
**Goal**: Convert docx files to markdown with image extraction

**Deliverables**:
- [ ] pyproject.toml with docling dependency
- [ ] Virtual environment setup using uv
- [ ] Main conversion script that:
  - Parses config.ini
  - Converts all uncommented .docx files
  - Exports markdown with images to output directory
- [ ] Error handling and progress logging
- [ ] Successful conversion of test documents

**Success Criteria**: All uncommented files in config.ini are converted to markdown with properly linked images in their respective subdirectories.
