# Document to Markdown Converter - Specification

## Overview
A simple Python CLI application that converts DOCX and PDF documents to markdown format using the docling library.

## Requirements

### Functional Requirements
1. Read input file paths from `input/config.ini`
2. Process all uncommented entries in the config file
3. Convert DOCX and PDF files to markdown format
4. Extract and save images to `output/<docname>_images/` subdirectories
5. Save markdown files to `output/<docname>.md` with proper image links
6. Automatically patch PDFs missing MediaBox metadata with A4 defaults (595 x 842 points)
7. Retry conversion with patched PDF on MediaBox errors
8. Save patched PDFs to output directory for inspection
9. Handle multiple files in batch mode

### Non-Functional Requirements
- CLI-only interface (no GUI)
- Error handling for missing files and conversion failures
- Clear console output showing conversion progress

## Tech Stack

- **Language**: Python 3.x
- **Conversion Library**: [docling](https://github.com/docling-project/docling) - for DOCX and PDF to markdown conversion
- **PDF Processing**: PyPDF2 - for patching PDFs with missing MediaBox metadata
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
│   ├── *.docx              # Source DOCX documents
│   └── *.pdf               # Source PDF documents
├── output/
│   ├── *.md                # Generated markdown files
│   ├── *_images/           # Extracted images per document
│   └── *_patched.pdf       # Patched PDFs (with fixed MediaBox)
├── convert_documents.py    # Main converter script
└── pyproject.toml          # Project dependencies
```

## Milestones

### M1: MVP - Basic DOCX Conversion (v1.0)
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

**Success Criteria**: All uncommented DOCX files in config.ini are converted to markdown with properly linked images in their respective subdirectories.

### M2: PDF Support with MediaBox Patching (v2.0)
**Goal**: Add PDF conversion with automatic repair for malformed PDFs missing MediaBox metadata

**Deliverables**:
- [ ] Add PyPDF2 dependency to pyproject.toml
- [ ] Rename convert_docx.py to convert_documents.py
- [ ] Update script entry point in pyproject.toml
- [ ] Create `patch_pdf_mediabox()` function to fix PDFs missing page dimensions
- [ ] Implement retry logic: try conversion → detect MediaBox error → patch PDF → retry
- [ ] Save patched PDFs to output directory with `_patched.pdf` suffix
- [ ] Update documentation and docstrings for multi-format support

**Success Criteria**: All PDF files (including those with missing MediaBox) are successfully converted to markdown. Patched PDFs are saved to output directory for inspection.
