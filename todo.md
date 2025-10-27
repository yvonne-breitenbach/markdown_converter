# TODO - Milestone 1: MVP

## Setup Tasks
- [ ] Create pyproject.toml with project metadata and docling dependency
- [ ] Create virtual environment using `uv venv venv`
- [ ] Install dependencies using `uv pip install -e .`

## Core Implementation
- [ ] Create `convert_docx.py` main script file
- [ ] Implement config.ini parser to read file entries
- [ ] Filter out commented lines (starting with #) from config
- [ ] Implement docx to markdown conversion using docling
- [ ] Implement image extraction and saving to `output/<docname>_images/`
- [ ] Ensure markdown files reference images with correct relative paths
- [ ] Save markdown output to `output/<docname>.md`

## Error Handling & Logging
- [ ] Add error handling for missing input files
- [ ] Add error handling for invalid config.ini format
- [ ] Add error handling for docling conversion failures
- [ ] Implement console logging for conversion progress
- [ ] Add success/failure messages for each file processed

## Testing & Validation
- [ ] Test conversion with "Verbraucherfreundlichkeit V2.docx"
- [ ] Verify markdown output is properly formatted
- [ ] Verify images are extracted to correct subdirectory
- [ ] Verify image links work in markdown file
- [ ] Test with multiple uncommented files in config.ini
- [ ] Verify error handling works with non-existent files

## Completion Criteria
- [ ] All uncommented files in config.ini convert successfully
- [ ] Images are properly extracted and linked
- [ ] Clear error messages appear for any failures
- [ ] Code follows PEP 8 style guidelines
