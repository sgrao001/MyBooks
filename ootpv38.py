import json
import argparse
from pathlib import Path
import re
import shutil
import os
import sys
import logging
from html import escape
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # CHANGE FROM INFO TO DEBUG
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('conversion.log'),
        logging.StreamHandler()
    ]
)

        

def load_config(config_path="BookMark.json"):
    """Load and validate configuration from JSON file with proper path resolution"""
    try:
        config_file = Path(config_path).resolve()
        
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_file}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Convert any string booleans to actual booleans
        boolean_keys = ['COPY_ENABLE', 'ARW_DISPLAY', 'SLDR_DISPLAY', 'Page0_skip', 'TOC_ENABLE']
        for key in boolean_keys:
            if key in config and isinstance(config[key], str):
                config[key] = config[key].lower() == 'true'
        
        return config
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in config file: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error loading config: {str(e)}")
        sys.exit(1)

def resolve_relative_path(path, base_dir=None):
    """Convert relative paths to absolute paths relative to script directory"""
    if base_dir is None:
        base_dir = Path(__file__).parent
    return (base_dir / path).resolve()

def validate_config():
    """Validate the configuration dictionary"""
    required_keys = ['source_path', 'source_md', 'output_md', 'output_html', 'COPY_ENABLE', 'BkImage',
                    'ARW_DISPLAY', 'ARW_HOVER_WIDTH', 'ARW_VISIBLE_WIDTH', 'SLDR_DISPLAY', 
                    'Hide_page_number',
                    'BkFontColor', 'BkFontSize', 'BkFontSizeMobile390', 'TitleFontSize', 'TitleFontClr', 'BkPage0_FontColor', 
                    'BkPage0_Title', 'BkPage0_Description', 'BkPage0_Tag','Author_name','BkPage0_Keywords', 'BkPage0_head3',
                    'BkListLink_show', 'BkLinkURL', 
                    'ImageWidthDesktop', 'ImageWidthMobile', 'ResizeForMobile', 'Page0_skip',
                    'TOCasList', 
                    'TOC_FontColor' ]  # Updated keys
    
    for key in required_keys:
        if key not in CONFIG:
            raise ValueError(f"Missing required config key: {key}")
    
    # Validate COPY_ENABLE is boolean
    if not isinstance(CONFIG['COPY_ENABLE'], bool):
        raise ValueError("COPY_ENABLE must be a boolean (True/False)")
    # Validate ARW_DISPLAY is boolean
    if not isinstance(CONFIG['ARW_DISPLAY'], bool):
        raise ValueError("ARW_DISPLAY must be a boolean (True/False)")
        # Validate boolean values
    if not isinstance(CONFIG['SLDR_DISPLAY'], bool):
        raise ValueError("SLDR_DISPLAY must be True or False")
        # Validate it's now a boolean
    if not isinstance(CONFIG['Hide_page_number'], bool):
        raise ValueError("Hide_page_number must be True or False")
    if not isinstance(CONFIG['Page0_skip'], bool):
        raise ValueError("Page0_skip must be True or False")
    
    # validate width percentages
    if not 0 <= CONFIG['ARW_HOVER_WIDTH'] <= 100:
        raise ValueError("ARW_HOVER_WIDTH must be between 0 and 100")
    if not 0 <= CONFIG['ARW_VISIBLE_WIDTH'] <= 100:
        raise ValueError("ARW_VISIBLE_WIDTH must be between 0 and 100")
    
    # Validate color formats (simple check)
    if not re.match(r'^#[0-9a-fA-F]{6}$', CONFIG['BkPage0_FontColor']):
        raise ValueError("BkPage0_FontColor must be a valid hex color code")
        
    # Validate font sizes
    if not re.match(r'^\d+(\.\d+)?(px|em|rem|%)$', CONFIG['TitleFontSize']):
        raise ValueError("TitleFontSize must be a valid CSS font size")
    if not re.match(r'^#[0-9a-fA-F]{6}$', CONFIG['TitleFontClr']):
        raise ValueError("TitleFontClr must be a valid CSS font size")
    
    if not re.match(r'^\d+(\.\d+)?(px|em|rem|%)$', CONFIG['BkFontSize']):
        raise ValueError("BkFontSize must be a valid CSS font size")
    # Add validation rule
    if not re.match(r'^\d+(\.\d+)?(px|em|rem|%)$', CONFIG['BkFontSizeMobile390']):
        raise ValueError("BkFontSizeMobile390 must be a valid CSS font size")
    
    # Validate image width values
    if not re.match(r'^\d+(\.\d+)?(px|em|rem|%)$', CONFIG['ImageWidthDesktop']):
        raise ValueError("ImageWidthDesktop must be a valid CSS size value")
    if not re.match(r'^\d+(\.\d+)?(px|em|rem|%)$', CONFIG['ImageWidthMobile']):
        raise ValueError("ImageWidthMobile must be a valid CSS size value")
    if not isinstance(CONFIG['ResizeForMobile'], bool):
        raise ValueError("ResizeForMobile must be a boolean (True/False)") 
    
    # Validate BkListLink_show
    if not isinstance(CONFIG['BkListLink_show'], bool):
        raise ValueError("BkListLink_show must be a boolean (True/False)") 
    
    # Validate BkLinkURL
    if not isinstance(CONFIG['BkLinkURL'], str):
        raise ValueError("BkLinkURL must be a string")
    
    """Validate the configuration dictionary"""
    # Add these to required_keys if needed
    if 'TOC_ENABLE' in CONFIG and not isinstance(CONFIG['TOC_ENABLE'], bool):
        raise ValueError("TOC_ENABLE must be a boolean (True/False)")   
    if 'TOC_POSITION' in CONFIG and not isinstance(CONFIG['TOC_POSITION'], int):
        raise ValueError("TOC_POSITION must be an integer")  
    if 'TOC_TITLE' in CONFIG and not isinstance(CONFIG['TOC_TITLE'], str):
        raise ValueError("TOC_TITLE must be a string")
    if not re.match(r'^#[0-9a-fA-F]{6}$', CONFIG['TOC_FontColor']):
        raise ValueError("TOC_FontColor must be a valid hex color code")
    if not isinstance(CONFIG['TOCasList'], bool):
        raise ValueError("TOCasList must be a boolean (True/False)")    
        # Validate color formats (simple check)
    
    # Validate Strings
    if 'BkPage0_Title' in CONFIG and not isinstance(CONFIG['BkPage0_Title'], str):
        raise ValueError("BkPage0_Title must be a string")
    if 'BkPage0_Description' in CONFIG and not isinstance(CONFIG['BkPage0_Description'], str):
        raise ValueError("BkPage0_Description must be a string")
    if 'BkPage0_Tag' in CONFIG and not isinstance(CONFIG['BkPage0_Tag'], str):
        raise ValueError("BkPage0_Tag must be a string")
    if 'Author_name' in CONFIG and not isinstance(CONFIG['Author_name'], str):
        raise ValueError("Author_name must be a string")
    if 'BkPage0_Keywords' in CONFIG and not isinstance(CONFIG['BkPage0_Keywords'], str):
        raise ValueError("BkPage0_Keywords must be a string")
    if 'BkPage0_head3' in CONFIG and not isinstance(CONFIG['BkPage0_head3'], str):
        raise ValueError("BkPage0_head3 must be a string")
    if 'TOC_TITLE' in CONFIG and not isinstance(CONFIG['TOC_TITLE'], str):
        raise ValueError("TOC_TITLE must be a string")    

    # Validate Path Name
    if 'source_path' in CONFIG:
        value = CONFIG['source_path']
        # Check if it's a string AND if it's a relative path
        if not isinstance(value, str) or os.path.isabs(value):
            raise ValueError("source_path must be a relative path")
        
    # Must be an md filename
    if 'source_md' in CONFIG:
        value = CONFIG['source_md']
        # Check if it's a string AND if it ends with .md
        if not isinstance(value, str) or not value.lower().endswith('.md'):
            raise ValueError("source_md must be a valid .md filename")
    if 'output_md' in CONFIG:
        value = CONFIG['output_md']
        # Check if it's a string AND if it ends with .md
        if not isinstance(value, str) or not value.lower().endswith('.mdx'):
            raise ValueError("output_md must be a valid .mdx filename")
    if 'output_html' in CONFIG:
        value = CONFIG['output_html']
        # Check if it's a string AND if it ends with .md
        if not isinstance(value, str) or not value.lower().endswith('.html'):
            raise ValueError("output_html must be a valid .html filename")
    if 'BkImage' in CONFIG:
        value = CONFIG['BkImage']
        
        # Check if it's a string and ends with either extension
        if not isinstance(value, str) or not value.lower().endswith(('.jpg', '.jpeg')):
            raise ValueError("BkImage must be a .jpg or .jpeg file")


def copy_file(src, dst):
    """Copy a file from src to dst with error handling."""
    try:
        source_path = Path(src).expanduser().resolve()
        dst_path = Path(dst).expanduser().resolve()
        
        if not source_path.exists():
            raise FileNotFoundError(f"Source file '{source_path}' does not exist")
            
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, dst_path)
        logging.info(f"Copied '{source_path}' to '{dst_path}'")
        return True
        
    except Exception as e:
        logging.error(f"Error copying file: {str(e)}")
        return False

# Notes:
# .page is absolutely positioned and centered; only the active page has display: block.
#   - .page-content is the only child of .page that scrolls (overflow-y: auto).
#   - The .page-header is inserted by JavaScript into .page-content as the first child.
#   - The .book-title inside the header is always present; the .book-title on the TOC page is separate.
#   - ::after on .page creates a fixed vignette overlay (glass edge effect).
#   - The slider, arrows, and hover areas are fixed to the viewport.
# This hierarchy reflects the final rendered HTML structure and CSS dependencies.
#body
#├── .progress-container
#│   └── .progress-bar
#├── .page (active page, others hidden)
#│   ├── .page::after (vignette overlay)
#│   ├── .page-content (scrollable container)
#│   │   ├── .page-header (only on content pages)
#│   │   │   ├── .back-to-toc (if TOC exists)
#│   │   │   ├── .book-title (centered)
#│   │   │   └── .page-number
#│   │   │       └── a (🔖 copy link)
#│   │   │           └── .glassbtn (🔖)
#│   │   ├── .book-title (only on TOC page; separate from header)
#│   │   ├── .image-container (if image present)
#│   │   │   ├── img
#│   │   │   ├── .image-caption-popup (hover popup)
#│   │   │   └── .highlight-text (title part, optional)
#│   │   ├── .text-only-container (if no image)
#│   │   │   └── .highlight-text (title part, optional)
#│   │   ├── .content-text (main text)
#│   │   ├── .toc-container (only on TOC page)
#│   │   │   ├── h2 (TOC title)
#│   │   │   ├── .back-to-list (AboutMe button, optional)
#│   │   │   ├── .toc-button-container
#│   │   │   │   ├── .toc-entry (if TOCasList true)
#│   │   │   │   │   └── a.toc-link
#│   │   │   │   └── a.glassbtn.compact-button.toc-link (if TOCasList false)
#│   │   │   └── hr + tip_string (navigation tips)
#│   │   └── .heading-container (only on title page)
#│   │       ├── h1, h2, h3, p (writing period)
#│   │       └── tip_string (navigation tips)
#│   └── (other .page elements for each content page)
#├── .arrow-area.left / .arrow-area.right (fixed hover zones)
#├── .arrow-container.left / .arrow-container.right (fixed arrows)
#│   └── .nav-arrow
#├── .slider-area (hover zone)
#├── .slider-container (fixed at bottom)
#│   ├── .slider-wrapper
#│   │   ├── .slider-track (filled portion)
#│   │   └── input.slider (range input)
#│   └── .slider-info
#│       ├── #current-page (display text)
#│       └── #total-pages
#└── #BubbleText (fixed popup container)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <!-- Update viewport meta tag -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no">
    
    <title>{BkPage0_Title}</title>
    <meta name="description" content="{BkPage0_Description}">
    <meta name="keywords" content="{BkPage0_Keywords}">
    <style>
        :root {{
            --primary-color: #f09e5a;
            --glass-bg: rgba(0, 0, 0, 0.2);
            --glass-shadow: 0 12px 20px rgba(0, 0, 0, 0.4);
            --text-color: {BkFontColor};

            --arrow-visibility: ARW_VISIBILITY;
            --arrow-opacity: ARW_OPACITY;
            --arrow-hover-opacity: ARW_HOVER_OPACITY;
            --arrow-hover-width: {ARW_HOVER_WIDTH}%;
            --ARW_HOVER_HEIGHT: 87vh;
            --ARW_HOVER_HEIGHT_415px: 73vh;
            --ARW_HOVER_TOP: 10vh;

            --content-container-max-width: 95%;

            --page-width: 94vw;
            --page-height: 94vh;
            --page-height-415px: 60vh;

            --tt-1024-height: 91vh;
            --tt-1024-width: 90vw;
            --tt-768-height: 83vh;
            --tt-768-width: 88vw;
            --tt-415-height: 77vh;
            --tt-415-width: 84vw;
            --tt-max-height: var(--tt-1024-height);
            --tt-max-width: var(--tt-1024-width);

            --Lmargin-safe-factor: 0.650;
            --Rmargin-safe-factor: 0.650;
            --Lsafe-margin: calc((var(--arrow-hover-width) + 0.25%) * var(--Lmargin-safe-factor));
            --Rsafe-margin: calc((var(--arrow-hover-width) + 0.25%) * var(--Rmargin-safe-factor));
        }}

        html {{
            touch-action: manipulation;
            -webkit-overflow-scrolling: touch;
            overscroll-behavior: contain;
            overflow-x: hidden;
        }}

        body {{
            background-image: url('{BkImage}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: var(--text-color);
            font-family: Georgia, 'Times New Roman', Times, serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            overflow: hidden;
            touch-action: pan-y;
            -webkit-touch-callout: none;
            -webkit-user-select: none;
            overscroll-behavior: none;
        }}

        a {{
            color: #4fc3f7 !important;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        a:hover {{
            background: rgba(0,0,0,0.6);
            text-decoration: underline;
            color: var(--text-color);
        }}
        a:focus {{
            outline: 2px solid #ffeb3b;
            outline-offset: 2px;
        }}

        .progress-container {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: rgba(0,0,0,0.1);
            z-index: 100;
        }}
        .progress-bar {{
            height: 100%;
            background: #000;
            width: 0%;
            transition: width 0.4s cubic-bezier(0.65, 0, 0.35, 1);
        }}

        .page {{
            width: var(--page-width);
            height: var(--page-height);
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) scale(0.95);
            opacity: 0;
            color: {BkFontColor};
            overflow-y: hidden;
            padding: 20px !important;
            box-sizing: border-box;
            border: 1px solid rgba(255,255,255,0.3);
            border-right: 1.5px solid rgba(255,255,255,0.4);
            border-bottom: 1.5px solid rgba(255,255,255,0.4);
            box-shadow: var(--glass-shadow);
            background: var(--glass-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            -webkit-overflow-scrolling: touch;
            border-radius: 12px;
            transition: all 0.6s cubic-bezier(0.65, 0, 0.35, 1);
            z-index: 1;
            display: none;
            -ms-overflow-style: none;
            scrollbar-width: none;
        }}
        .page::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            background: 
                linear-gradient(to bottom, rgba(255,255,255,0.1), transparent 15%),
                linear-gradient(to top, rgba(255,255,255,0.1), transparent 15%),
                linear-gradient(to right, rgba(255,255,255,0.1), transparent 15%),
                linear-gradient(to left, rgba(255,255,255,0.1), transparent 15%);
            z-index: 2;
        }}
        .page-content {{
            height: 100%;
            width: 100%;
            overflow-y: auto;
            box-sizing: border-box;
            -ms-overflow-style: none;
            scrollbar-width: none;
        }}
        .page-content::-webkit-scrollbar {{
            display: none;
        }}
        #page-0::after {{
            display: none;
        }}

        #page-0 {{
            background: none !important;
            backdrop-filter: none !important;
            -webkit-backdrop-filter: none !important;
            border: none !important;
            box-shadow: none !important;
        }}
        #page-0 h1, #page-0 h2, #page-0 h3 {{
            color: {BkPage0_FontColor} !important;
        }}
        .heading-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            width: 100%;
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
        }}

        .page-content > :first-child {{
            margin-top: 0;
        }}
        .page-content h2:first-of-type {{
            margin-top: 5px;
        }}
        .image-container:first-child,
        .text-only-container:first-child {{
            margin-top: 0;
        }}

        .page-header {{
            position: relative;
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 3;
            margin-bottom: 20px;
        }}
        .book-title {{
            flex: 1;
            text-align: center;
            max-width: 50vw;
            margin: 0 auto;
            word-wrap: break-word;
            font-size: 0.8em;
            order: 2;
            position: static;
            transform: none;
        }}
        .back-to-toc {{
            order: 1;
            transform: scale(1.15, 0.95);
        }}
        .page-number {{
            flex: 0 0 auto;
            margin-top: 5px;
            order: 3;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            background: transparent !important;
            visibility: {pageNumberStyle} !important;
        }}

        .next-page, .prev-page, .back-to-toc, .back-to-list, .slider-container, .glassbtn {{
            color: var(--text-color);
            text-decoration: none;
            font-size: 1em;
            font-family: Arial;
            padding: 5px 15px;
            margin: 5px;
            background: rgba(0, 0, 0, 0.075) !important;
            box-sizing: border-box;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(5px);
            -webkit-overflow-scrolling: touch;
            border-radius: 20px;
            border-bottom: 1px solid rgba(255,255,255,0.4);
            border-right: 1px solid rgba(255,255,255,0.4);
            border-top: none;
            border-left: none;
            box-shadow: 0 5px 14px rgba(0,0,0,0.5),
                        0 2px 4px rgba(0,0,0,0.3),
                        0 0 0 1.5px rgba(255,255,255,0.4) inset;
            transition: all 0.3s ease;
            position: relative;
            z-index: 9999;
            pointer-events: auto !important;
            cursor: pointer !important;
        }}
        .back-to-toc, .page-number, .page-number a, .glassbtn {{
            vertical-align: middle;
            line-height: 1.2;
        }}
        .next-page:hover, .prev-page:hover, .back-to-toc:hover, .back-to-list:hover, .glassbtn:hover {{
            background: rgba(0, 0, 0, 0.55) !important;
            box-shadow: 0 5px 14px rgba(0,0,0,0.7),
                        0 2px 4px rgba(0,0,0,0.6),
                        0 0 0 1.5px rgba(255,255,255,0.6) inset,
                        0 0 0 2px rgba(255,255,255,0.4) inset;
            border-top: 1px solid rgba(255,255,255,0.4);
            border-left: 1px solid rgba(255,255,255,0.4);
            border-bottom: none;
            border-right: none;
            text-decoration: underline;
        }}
        .slider-container:hover {{
            background: rgba(0, 0, 0, 0.3) !important;
            text-decoration: none;
        }}
        a:has(.glassbtn) {{
            text-decoration: none;
            background: transparent;
        }}

        .arrow-container {{
            position: fixed;
            height: var(--ARW_HOVER_HEIGHT);
            top: var(--ARW_HOVER_TOP);
            width: {ARW_HOVER_WIDTH}%;
            background: rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            z-index: 10;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            cursor: pointer;
            opacity: var(--arrow-opacity);
            transition: all 0.3s ease;
            pointer-events: auto;
        }}
        .arrow-container[data-visible="true"] {{
            width: {ARW_VISIBLE_WIDTH}% !important;
        }}
        .arrow-container.right {{
            right: 0px;
        }}
        .arrow-container:hover {{
            opacity: var(--arrow-hover-opacity);
        }}
        .nav-arrow {{
            width: 15px;
            height: 15px;
            border: solid {BkFontColor};
            border-width: 0 3px 3px 0;
            display: inline-block;
            visibility: var(--arrow-visibility);
        }}
        .nav-arrow.left {{
            transform: rotate(135deg);
        }}
        .nav-arrow.right {{
            transform: rotate(-45deg);
        }}
        .arrow-area {{
            position: fixed;
            height: var(--ARW_HOVER_HEIGHT);
            top: var(--ARW_HOVER_TOP);
            width: {ARW_HOVER_WIDTH}%;
            z-index: 9;
            display: flex;
            pointer-events: auto;
            -webkit-tap-highlight-color: transparent;
        }}
        .arrow-area.right {{
            right: 0;
        }}
        .arrow-area.left:hover ~ .arrow-container.left,
        .arrow-area.right:hover ~ .arrow-container.right {{
            opacity: var(--arrow-hover-opacity);
        }}

        .slider-container {{
            position: fixed;
            bottom: 10px;
            left: 50%;
            transform: translateX(-50%);
            width: var(--page-width);
            height: 50px;
            z-index: 20;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            transition: all 0.3s cubic-bezier(0.65, 0, 0.35, 1);
            opacity: 0;
            pointer-events: none;
        }}
        .slider-area {{
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 60px;
            z-index: 19;
        }}
        .slider-area:hover ~ .slider-container,
        .slider-container:hover {{
            opacity: 1;
            pointer-events: auto;
        }}
        .slider-wrapper {{
            width: 80%;
            position: relative;
            margin: 0 auto;
        }}
        .slider {{
            width: 100%;
            margin-bottom: 5px;
            -webkit-appearance: none;
            height: 3px;
            background: rgba(96, 96, 96, 0);
            border-radius: 10px;
            outline: none;
            transition: all 0.3s cubic-bezier(0.65, 0, 0.35, 1);
            border: 1px solid darkgray;
        }}
        .slider::-webkit-slider-thumb {{
            -webkit-appearance: none;
            width: 24px;
            height: 16px;
            appearance: none;
            background: rgba(176, 224, 255, 1) !important;
            border: 1px solid darkgray !important;
            border-radius: 50%;
            cursor: pointer;
        }}
        .slider::-moz-range-thumb {{
            width: 24px;
            height: 16px;
            background: rgba(176, 224, 255, 1) !important;
            border: 1px solid darkgray !important;
            border-radius: 50%;
            cursor: pointer;
        }}
        .slider-track {{
            position: absolute;
            height: 4px;
            border-radius: 10px;
            top: 50%;
            transform: translateY(-50%);
            left: 0;
            pointer-events: none;
        }}
        .slider-info {{
            color: #b0e0ff;
            font-size: 0.8em;
            font-family: Georgia, 'Times New Roman', Times, serif;
            margin-bottom: 5px;
        }}
        .slider-info #current-page {{
            color: #b0e0ff;
            font-style: italic;
        }}

        .image-container, .text-only-container {{
            width: 100%;
            max-width: var(--content-container-max-width);
            margin-left: auto;
            margin-right: auto;
            box-sizing: border-box;
        }}
        .image-container {{
            position: relative;
            overflow: visible;
        }}
        .image-container img {{
            position: relative;
            display: block;
            max-width: {ImageWidthDesktop};
            height: auto;
            border-radius: 8px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            shape-outside: margin-box;
            transition: all 0.5s cubic-bezier(0.65, 0, 0.35, 1);
            opacity: 0.95;
            transform: scale(0.98);
            filter: drop-shadow(0 4px 12px rgba(0,0,0,0.6));
        }}
        .image-align-left img {{
            float: left;
            margin-left: 0px;
            margin-right: 20px;
            margin-top: 20px;
            margin-bottom: 40px;
        }}
        .image-align-right img {{
            float: right;
            margin-left: 20px;
            margin-right: 20px;
            margin-top: 20px;
            margin-bottom: 40px;
        }}
        .image-align-center img {{
            float: none;
            display: block;
            margin-top: 20px;
            margin-bottom: 40px;
            left: 50%;
            transform: translateX(-50%) !important;
        }}
        .image-container img:hover {{
            opacity: 1;
            transform: scale(1);
            box-shadow: 0 15px 35px rgba(0,0,0,0.9);
            filter: drop-shadow(0 8px 20px rgba(0,0,0,0.8));
        }}
        .text-only-container {{
            width: 90%;
            margin: 0px auto;
            padding: 0;
        }}
        .image-container + .image-container {{
            margin-top: 10px;
        }}
        .content-text {{
            font-size: inherit;
            text-align: left;
        }}
        .highlight-text {{
            color: {TitleFontClr};
            font-size: 1.2em;
            display: inline-block;
            text-decoration: underline;
            text-decoration-color: {TitleFontClr};
            padding-bottom: 3px;
        }}
        p {{
            margin-bottom: 1.8em;
            text-align: left;
            line-height: 1.7;
            font-size: 1.05em;
        }}
        p.inline {{ display: inline; }}
        p.none {{ display: none; }}
        h1 {{ font-size: 2.8em; color: #fff; font-weight: 700; }}
        h2 {{ font-size: 1.4em; font-weight: 400; color: rgba(255,255,255,0.8); }}
        h3 {{ font-size: 1.3em; font-weight: 300; color: rgba(255,255,255,0.7); }}

        .toc-container {{
            margin-left: var(--Lsafe-margin);
            margin-right: var(--Rsafe-margin);
            padding: 20px;
        }}
        .toc-button-container {{
            width: 100%;
            display: flex;
            flex-wrap: wrap;
            column-gap: 10px;
            row-gap: 12px;
        }}
        .toc-list .toc-button-container {{
            display: block;
        }}
        .compact-button {{
            color: {TOC_FontColor} !important;
            border-radius: 12px;
            transition: all 0.3s ease;
            white-space: nowrap;
            margin: 0 !important;
        }}
        .toc-list .toc-entry {{
            margin: 8px 0;
            padding: 5px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            transition: all 0.3s ease;
        }}
        .toc-list .toc-entry a {{
            color: var(--text-color);
            text-decoration: none;
            display: block;
        }}
        .toc-list .toc-entry:hover {{
            border-bottom-color: var(--primary-color);
        }}
        .toc-list .toc-entry:hover a {{
            color: var(--primary-color);
        }}

        table {{
            width: auto;
            max-width: 100%;
            table-layout: auto;
            word-wrap: break-word;
            border-collapse: collapse;
            font-size: 0.9em;
            min-width: 400px;
            border-radius: 5px;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0,0,0,0.15);
            background: rgba(15,15,15,0.25) !important;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }}
        table a {{
            background: rgba(0,0,0,0.15);
            padding: 2px 6px;
            border-radius: 4px;
            display: inline-block;
        }}
        table a:hover {{
            background: rgba(0,0,0,0.3);
            text-decoration: none;
        }}
        table thead tr {{
            background: transparent !important;
            position: relative;
            overflow: hidden;
        }}
        table th, table td {{
            border-bottom: 1px solid rgba(255,255,255,0.1);
            min-width: 15%;
            max-width: 100%;
            word-break: break-word;
            background: transparent !important;
        }}
        table tbody tr {{
            transition: all 0.2s ease;
            background: rgba(255,255,255,0.05) !important;
        }}
        table tbody tr:last-of-type {{
            border-bottom: 2px solid var(--primary-color);
        }}
        table tbody tr:hover {{
            background-color: rgba(0,0,0,0.3);
        }}
        .table-container {{
            width: 100%;
            overflow-x: auto;
        }}

        .image-caption-popup {{
            position: absolute;
            top: 0;
            max-width: 100%;
            font-size: .8em;
            padding: 0px 10px;
            box-sizing: border-box;
            text-align: center !important;
            pointer-events: auto;
            display: block !important;
            opacity: 0 !important;
            transform: translateY(-20px) scale(0.95) !important;
            transition: all 0.5s cubic-bezier(0.65, 0, 0.35, 1) !important;
            pointer-events: none;
            background: rgba(0,0,0,0.45) !important;
            backdrop-filter: blur(15px) !important;
            -webkit-backdrop-filter: blur(15px) !important;
            border-radius: 8px;
            box-shadow: 0 5px 5px rgba(0,0,0,0.95);
            z-index: 1000;
        }}
        .image-align-left .image-caption-popup {{
            top: 40px;
            right: auto;
        }}
        .image-align-right .image-caption-popup {{
            top: 40px;
            right: 20px;
            left: auto;
        }}
        .image-align-center .image-caption-popup {{
            top: 20px;
            left: 50% !important;
            transform: translateX(-50%) translateY(-20px) scale(0.95) !important;
            padding: 0px 10px;
            box-sizing: border-box !important;
        }}
        .image-container img:hover ~ .image-caption-popup,
        .image-caption-popup:hover {{
            opacity: 1 !important;
            pointer-events: auto !important;
        }}
        body .page .image-container .image-caption-popup {{
            z-index: 1000 !important;
        }}
        body .page .image-container img {{
            z-index: 2 !important;
        }}

        .BubbleText-trigger {{
            color: #4fc3f7;
            font-size: 0.8em;
            font-family: Arial;
            font-weight: normal;
            text-decoration: none;
            font-style: normal;
            margin: 0 10px;
        }}
        .BubbleText-group {{
            display: inline-block;
            margin-left: var(--Lsafe-margin);
            vertical-align: top;
        }}
        .BubbleText-full {{
            height: var(--tt-max-height);
            width: var(--tt-max-width);
        }}
        .BubbleText-group .BubbleText-trigger {{
            display: inline-block !important;
            width: auto !important;
            margin: 0 4px !important;
        }}
        .BubbleText-trigger.BubbleText-full {{
            height: auto;
            width: auto;
        }}
        #BubbleText {{
            position: fixed;
            display: inline-block;
            color: #b0e0ff;
            font-family: Arial;
            font-weight: normal;
            font-size: 0.8em;
            transform: translateY(-20px) scale(0.95) !important;
            transition: all 0.5s cubic-bezier(0.65, 0, 0.35, 1) !important;
            background: rgba(0,0,0,0.42) !important;
            box-sizing: border-box;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(5px);
            -webkit-overflow-scrolling: touch;
            border-radius: 20px;
            border-left: 1px solid rgba(255,255,255,0.4);
            border-right: 1px solid rgba(255,255,255,0.4);
            border-top: none;
            border-bottom: none;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5),
                        0 0 0 1px rgba(255,255,255,0.2) inset;
            padding: 10px !important;
            width: fit-content;
            height: fit-content;
            min-height: 1.5em;
            max-width: var(--tt-max-width);
            max-height: var(--tt-max-height);
            overflow-x: hidden;
            overflow-y: auto;
            word-wrap: break-word;
            overflow-wrap: break-word;
            z-index: 9999;
            white-space: normal;
            opacity: 0;
            visibility: hidden;
            scrollbar-width: thin;
            scrollbar-color: rgba(255,255,255,0.4) rgba(255,255,255,0.1);
        }}
        #BubbleText.show {{
            opacity: 1;
            visibility: visible;
        }}
        #BubbleText.fade {{
            transform: translateY(15px) scale(0.95);
        }}
        #BubbleText.fade.show {{
            transform: translateY(0) scale(1);
        }}
        #BubbleText.bounce {{
            transform: translateY(40px) scale(0.6);
        }}
        #BubbleText.bounce.show {{
            animation: bounceIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }}
        #BubbleText.slide {{
            transform: translateY(60px);
        }}
        #BubbleText.slide.show {{
            transform: translateY(0);
        }}
        #BubbleText.zoom {{
            transform: scale(0.4);
        }}
        #BubbleText.zoom.show {{
            transform: scale(1);
        }}
        #BubbleText.left-text {{ text-align: left; }}
        #BubbleText.right-text {{ text-align: right; }}
        #BubbleText.center-text {{ text-align: center; }}
        @keyframes bounceIn {{
            0% {{ transform: translateY(40px) scale(0.6); }}
            60% {{ transform: translateY(-15px) scale(1.15); }}
            100% {{ transform: translateY(0) scale(1); }}
        }}
        #BubbleText::-webkit-scrollbar {{
            width: 6px;
        }}
        #BubbleText::-webkit-scrollbar-track {{
            background: rgba(255,255,255,0.1);
            border-radius: 3px;
        }}
        #BubbleText::-webkit-scrollbar-thumb {{
            background: rgba(255,255,255,0.4);
            border-radius: 3px;
        }}

        .page.active {{
            opacity: 1;
            transform: translate(-50%, -50%) scale(1);
            z-index: 2;
            display: block;
        }}
        .page.exit {{
            transform: translate(-50%, -50%) scale(0.98);
            opacity: 0;
            display: none;
        }}

        @media (max-width: 768px) {{
            :root {{
                --tt-max-height: var(--tt-768-height) !important;
                --tt-max-width: var(--tt-768-width) !important;
                --content-container-max-width: 93%;
                --Lmargin-safe-factor: 0.65;
                --Rmargin-safe-factor: 0.85;
            }}
            .BubbleText-full {{
                height: var(--tt-max-height);
                width: var(--tt-max-width);
            }}
            body {{
                margin-top: 0px !important;
                height: 75% !important;
                overflow: hidden;
            }}
            @supports (-webkit-touch-callout: none) {{
                .page {{
                    height: -webkit-fill-available !important;
                    margin-top: 0 !important;
                }}
            }}
            a {{ color: #00b0ff !important; }}
            a:focus {{ outline: 2px solid #ffeb3b; outline-offset: 2px; }}
            .text-only-container {{
                width: 100% !important;
                padding: 0 10px !important;
                margin: 15px auto !important;
            }}
            p, h1, h2, h3 {{
                margin-bottom: 1.2em !important;
                line-height: 1.6 !important;
            }}
            .toc-entry {{ margin: 6px 0; }}
            .toc-header-left {{ text-align: left; }}
            .toc-header-row {{ display: flex; align-items: center; justify-content: space-between;}}
            .toc-header-row .book-title {{ flex: 1; text-align: center; margin: 0;}}

            h1 {{ font-size: 2.2em !important; }}
            h2 {{ font-size: 1.3em !important; }}
            h3 {{ font-size: 1.1em !important; }}
            table {{
                min-width: 0 !important;
                width: 100% !important;
                overflow-x: visible !important;
                backdrop-filter: blur(8px);
                background: rgba(15,15,15,0.3) !important;
                font-size: 0.9em !important;
            }}
            table * {{ box-sizing: border-box !important; }}
            table a {{
                padding: 3px 8px;
                background: rgba(0,0,0,0.2);
                margin: 0 auto !important;
            }}
            .table-container {{
                width: calc(100% - 10px) !important;
                overflow-x: visible !important;
            }}
            table th, table td {{
                min-width: 0% !important;
                white-space: normal !important;
                width: auto !important;
                max-width: 100% !important;
            }}
            table thead tr {{ background: rgba(0,0,0,0.4) !important; }}
            table td.important-column {{
                width: 60% !important;
                word-break: break-word !important;
                overflow-wrap: anywhere !important;
            }}
            table td {{
                hyphens: auto !important;
                word-break: break-word !important;
                overflow-wrap: anywhere !important;
            }}
            table a, table button {{
                white-space: normal !important;
                display: inline-block !important;
            }}
        }}

        @media (max-width: 415px) {{
            :root {{
                --tt-max-height: var(--tt-415-height) !important;
                --tt-max-width: var(--tt-415-width) !important;
                --content-container-max-width: 97%;
                --Lmargin-safe-factor: 0.40;
                --Rmargin-safe-factor: 0.80;
            }}
            .BubbleText-full {{
                height: var(--tt-max-height);
                width: var(--tt-max-width);
            }}
            body {{
                margin-top: 0px !important;
                height: 60% !important;
                overflow: hidden;
            }}
            .page {{ height: var(--page-height-415px) !important; }}
            .content-text {{ font-size: var(--mobile-font-size) !important; }}
            .arrow-container, .arrow-area {{ height: var(--ARW_HOVER_HEIGHT_415px); }}
            @supports (-webkit-touch-callout: none) {{
                .page {{
                    height: -webkit-fill-available !important;
                    margin-top: 0 !important;
                }}
            }}
            .compact-button {{
                padding: 3px 8px !important;
                font-size: 0.65em !important;
                display: inline-block
            }}
            {ForceMobileCSS}
            .image-caption-popup.mobile-visible {{
                opacity: 1;
                transform: translateY(0);
            }}
            .table-container {{
                width: 100% !important;
                overflow-x: auto !important;
                -webkit-overflow-scrolling: touch !important;
                display: block;
                margin: 15px 0;
                background: rgba(0,0,0,0.1);
                border-radius: 8px;
                padding: 8px 0;
            }}
            table {{
                display: table !important;
                width: auto !important;
                min-width: 100% !important;
                white-space: nowrap;
                font-size: 0.85em;
            }}
            table th, table td {{
                white-space: nowrap !important;
                min-width: 100px !important;
            }}
            .table-container::-webkit-scrollbar {{
                height: 5px;
            }}
            .table-container::-webkit-scrollbar-thumb {{
                background: rgba(255,255,255,0.3);
                border-radius: 5px;
            }}
        }}


        
    </style>
</head>
<body>
    <!-- Progress Bar -->
    <div class="progress-container">
        <div class="progress-bar" id="progress-bar"></div>
    </div>

    {title_page_html}
"""

FOOTER_TEMPLATE = """
    <!-- Arrow Hover Areas - Always present -->
    <div class="arrow-area left"></div>
    <div class="arrow-area right"></div>
    
    <!-- Arrow Containers - Always present -->
    <div class="arrow-container left" id="left-arrow-container" data-visible="{ARW_DISPLAY}">
    <div class="nav-arrow left"></div>
    </div>
    <div class="arrow-container right" id="right-arrow-container" data-visible="{ARW_DISPLAY}">
        <div class="nav-arrow right"></div>
    </div>

    <!-- Slider Hover Area -->
    <div class="slider-area"></div>
    
    <!-- Slider Container -->
    <div class="slider-container" id="slider-container" style="SLIDER_DISPLAY">
        <div class="slider-wrapper">
            <div class="slider-track" id="slider-track"></div>
            <input type="range" min="0" max="SLIDER_MAX" value="INITIAL_PAGE" class="slider" id="page-slider">
        </div>
        <div class="slider-info">
            <span id="current-page">INITIAL_PAGE</span>/<span id="total-pages">TOTALPAGES</span>
        </div>
    </div>

    <script>
        let currentPage = INITIAL_PAGE;
        const totalPages = TOTALPAGES;
        //================================================================================================
        // DO THIS ONLY IF YOU WANT THE Total PAGES TO COUNT ONLY  CONTENT PAGES - NOT TITLE AND TOC PAGES
        const totalContentPages = getTotalContentPages(); // compute
        document.getElementById('total-pages').textContent = totalContentPages;
        //================================================================================================

        const pages = document.querySelectorAll('.page');
        const page0Skipped = {Page0_skip};

        const slider = document.getElementById('page-slider');
        const sliderTrack = document.getElementById('slider-track');
        const progressBar = document.getElementById('progress-bar');
        const currentPageDisplay = document.getElementById('current-page');
        const totalPagesDisplay = document.getElementById('total-pages');
        const leftArrowContainer = document.getElementById('left-arrow-container');
        const rightArrowContainer = document.getElementById('right-arrow-container');
        const sliderContainer = document.getElementById('slider-container');

        // PRPOGRESS BAR FUNCTIONS START =========================================================================
        // The getContentPageNumber(index) function maps a page index (0‑based, including title and TOC) to a content page number (1‑based), returning 0 for non‑content pages (title or TOC). It works as follows:
        // - If the title page exists (!page0Skipped) and index === 0, it returns 0 (title page, no content number).
        // - If a TOC page exists (hasTOC) and the index matches the TOC’s position (which is 0 if title is skipped, else 1), it returns 0 (TOC page, no content number).
        // - Otherwise, it calculates the offset: offset = (title exists ? 1 : 0) + (TOC exists ? 1 : 0).
        // - The content page number is then index - offset + 1 (1‑based).
        //This function is useful for progress calculations (e.g., showing “Page 3 of 20”) where you want to ignore title and TOC pages.

        function getContentPageNumber(index) {
            const page0Skipped = {Page0_skip};
            const hasTOC = document.getElementById('page-toc') !== null;
            
            // If this is the title page or TOC page, return 0 (no progress)
            if (!page0Skipped && index === 0) return 0;      // title page
            if (hasTOC && index === (page0Skipped ? 0 : 1)) return 0; // TOC page
            
            // Calculate offset: number of non‑content pages before content starts
            let offset = 0;
            if (!page0Skipped) offset++;   // title page exists
            if (hasTOC) offset++;          // TOC page exists
            const contentPage = index - offset + 1;  // 1‑based content page number
            return contentPage;
        }

        // used to update both SLider and progress bar calculations
        function getTotalContentPages() {
            const page0Skipped = {Page0_skip};
            const hasTOC = document.getElementById('page-toc') !== null;
            let contentPages = totalPages;
            if (!page0Skipped) contentPages -= 1;
            if (hasTOC) contentPages -= 1;
            return contentPages;
        }

        // Updates the prpogress bar on top.
        function updateProgress() {
            const displayNum = getSliderDisplay(currentPage);
            let contentPage = 0;
            if (typeof displayNum === 'number') {
                contentPage = displayNum;
            }
            const totalContent = getTotalContentPages();
            let progress = 0;
            if (totalContent > 0 && contentPage > 0) {
                progress = (contentPage / totalContent) * 100;
            }
            progressBar.style.width = `${progress}%`;
        }
        // PROGRESS BAR FUNCTIOND END ===========================================================================

        // SLIDER FUNCTIONS START =========================================================================
        // Map page index to slider display number (-1, 0, 1, 2, ...)
        // Uses getTotalContentPages() from slider bar for count updates

        function getSliderDisplay(index) {
            const page0Skipped = {Page0_skip};
            const hasTOC = document.getElementById('page-toc') !== null;
            
            // Title page
            if (!page0Skipped && index === 0) return "Title";

            // TOC page
            if (hasTOC && index === (page0Skipped ? 0 : 1)) return "TOC";

            // Content pages
            let contentOffset = 0;
            if (!page0Skipped) contentOffset += 1;
            if (hasTOC) contentOffset += 1;
            return index - contentOffset + 1;  // returns number 1,2,3,...
        }

        function updateSlider() {
            slider.value = currentPage;
            const displayNum = getSliderDisplay(currentPage);
            currentPageDisplay.textContent = displayNum;
            updateSliderTrack();
        }
       // SLIDER FUNCTIONS END =========================================================================
 

        // BOOKMARK - COPY URL FUNCTIONS START =========================================================
        // This function copies the URL of the current page (including the fragment identifier #page-...) 
            // to the clipboard. It:
        // - Prevents the default event behavior.
        // - Finds the active page (.page.active) and gets its id.
        // - Builds the full URL: baseUrl + '#' + pageId.
        // - Uses the modern Clipboard API (navigator.clipboard.writeText) to copy the URL.
        // - If the Clipboard API fails or is unavailable, falls back to creating a hidden <textarea>, 
            // selecting its content, and using document.execCommand('copy').
        // - Shows a popup message (via showPopup) indicating success (with the copied URL) or an error.
        // - If no active page is found, it shows an error popup.
        // In short, it lets users copy a direct link to the current page (bookmark) to share or revisit later.

        function copyCurrentPageUrl(event) {
            if (event) {
                event.preventDefault();
                event.stopPropagation();
            }

            const activePage = document.querySelector('.page.active');
            if (!activePage) {
                console.error('No active page found');
                showPopup('Error: No active page');   // ← changed
                return;
            }

            const pageId = activePage.id;
            const baseUrl = window.location.href.split('#')[0];
            const fullUrl = baseUrl + '#' + pageId;

            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(fullUrl).then(() => {
                    showPopup('URL copied to clipboard<br>' + fullUrl);   // ← changed
                }).catch(err => {
                    console.error('Clipboard write failed:', err);
                    showPopup('Copy failed. Use Ctrl+C');   // ← changed
                });
            } else {
                // Fallback for older browsers
                const textarea = document.createElement('textarea');
                textarea.value = fullUrl;
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                showPopup('URL copied to Clipboard<br>' + fullUrl);   // ← changed
            }
        }  
        
         function showPopup(msg) {
            // Use your existing toggleBubbleText to display a centered popup
            toggleBubbleText('', '', 'auto', 'auto', msg, 'yes', 'fade', 'center', 'center-both', [], undefined, null, null, null, undefined);
            // Auto-close after 3 seconds (optional)
            setTimeout(() => {
                const bt = document.getElementById('BubbleText');
                if (bt && bt.classList.contains('show')) {
                    toggleBubbleText('', '', '', '', '', 'no');
                }
            }, 3000);
        }  
        // BOOKMARK COPY-URL FUNCTION======= END ============================================================

        // BOOKMARK COPY-URL LISTENER END ============================================================
        // Listener for ctrl-C or cmd-C to bookmark - <ClipBookMark>
        document.addEventListener('keydown', function(event) {
            // Check for Ctrl+C (Windows/Linux) or Cmd+C (Mac)
            if ((event.ctrlKey || event.metaKey) && event.key === 'c') {
                // Optionally, avoid interfering with normal copy if text is selected
                const selection = window.getSelection().toString();
                if (selection.length === 0) {
                    // No text selected – call your custom copy function
                    copyCurrentPageUrl(event);
                    // Prevent default browser copy (optional, but you might want to keep it)
                    // event.preventDefault();
                }
                // If text is selected, let the default copy happen
            }
        });
        // BOOKMARK COPY-URL LISTENER END ============================================================


                // ==================== BubbleText FUNCTION Start ============================================
        // BubbleText Management
        // Convert a CSS length string to pixels (returns NaN if not possible)

        function toPixels(value, dimension) {
            if (typeof value !== 'string') return NaN;
            value = value.trim();
            if (value.endsWith('px')) return parseFloat(value);
            if (value.endsWith('%')) {
                const percent = parseFloat(value) / 100;
                return dimension === 'width' ? window.innerWidth * percent : window.innerHeight * percent;
            }
            if (value.endsWith('vh')) return (parseFloat(value) / 100) * window.innerHeight;
            if (value.endsWith('vw')) return (parseFloat(value) / 100) * window.innerWidth;
            if (!isNaN(parseFloat(value))) return parseFloat(value);
            return NaN; // calc() or other complex expressions
        }

        // htmlEncodeBubbleTextText (keep your existing version)
        function htmlEncodeBubbleTextText(str) {
            const div = document.createElement('div');
            div.innerHTML = str;
            return div.innerHTML;
        }

        // The toggleBubbleText function manages a custom popup element (with id BubbleText) that appears when the user clicks on certain triggers (.BubbleText-trigger). It supports:
        // - Showing/hiding the popup based on the visible parameter.
        // - Flexible positioning – can place the popup relative to a trigger element, at specific coordinates, centered, or at the bottom of the page.
        // - Smart positioning (“@” mode) – automatically places the popup below the trigger if enough space, otherwise above; can also cap the height to fit the viewport.
        // - Sizing modes – explicit width/height (using block display) or growing box (inline-block with fit-content).
        // - Animations – fade, bounce, slide, zoom.
        // - Text alignment – left, right, center.
        // - Constraints – max‑width/‑height via CSS variables or trigger data attributes, clamping to viewport edges.
        // - Cleanup – on hiding, it removes content and resets styles.
        // - In essence, it is a highly configurable tooltip / modal‑like popup that adapts its position and size to avoid overflow and provide a smooth user experience.
        
        function toggleBubbleText(top, left, height, width, bbbltext, visible, animation = 'fade', textAlign = 'left', position = 'fixed', extraClasses = [], bottom = undefined, maxHeight = null, bottomGap = null, trigger = null, right = undefined) {
            const BubbleText = document.getElementById('BubbleText');

            // If width or height is '@', activate @ mode and clear the respective dimension
            if (width === '@') { top = '@'; width = ''; }
            if (height === '@') { top = '@';height = ''; }

            if (visible === 'yes') {
                // --- Prepare BubbleText for display ---
                BubbleText.className = '';
                extraClasses.forEach(cls => BubbleText.classList.add(cls));
                BubbleText.style.setProperty('position', position, 'important');
                
                // Determine if explicit width/height are provided (non-empty, not 'auto')
                const hasExplicitWidth = (width && width !== 'auto');
                const hasExplicitHeight = (height && height !== 'auto');
                
                if (hasExplicitWidth || hasExplicitHeight) {
                    // Explicit sizing: use block display and set inline width/height
                    BubbleText.style.display = 'block';
                    if (hasExplicitWidth) {
                        BubbleText.style.width = width;
                    } else {
                        BubbleText.style.width = '';
                    }
                    if (hasExplicitHeight) {
                        BubbleText.style.height = height;
                    } else {
                        BubbleText.style.height = '';
                    }
                } else {
                    // Growing box mode: shrink-to-fit, respect CSS min/max
                    BubbleText.style.display = 'inline-block';
                    BubbleText.style.width = '';
                    BubbleText.style.height = '';
                }
                
                // Text alignment
                if (textAlign !== 'left') BubbleText.classList.add(textAlign + '-text');
                
                // Animation
                if (animation !== 'fade') BubbleText.classList.add(animation);
                else BubbleText.classList.add('fade');

                // Read max-width / max-height from trigger (6th and 7th slots)
                const datasetMaxWidth = trigger?.dataset?.maxwidth;
                const datasetMaxHeight = trigger?.dataset?.maxheight;

                BubbleText.innerHTML = bbbltext;

                // Apply max-width / max-height (always limits)
                if (datasetMaxWidth) BubbleText.style.maxWidth = datasetMaxWidth;
                else BubbleText.style.maxWidth = '';
                if (datasetMaxHeight) BubbleText.style.maxHeight = datasetMaxHeight;
                else if (maxHeight !== null) BubbleText.style.maxHeight = maxHeight + 'px';
                else BubbleText.style.maxHeight = '';

                const pos = position.toLowerCase();
                const bottomModes = ['bottom-left', 'bottom-center', 'bottom-right', 'bottom-page'];
                const usesAt = top === '@' || left === '@' || bottom === '@' || right === '@';
                const needsLayout = ['center-height', 'center-width', 'center-both', ...bottomModes].includes(pos) || usesAt;

                if (needsLayout) {
                    BubbleText.style.visibility = 'visible';
                    BubbleText.style.opacity = '0';

                    requestAnimationFrame(() => {
                        requestAnimationFrame(() => {
                            const pageElement = trigger ? trigger.closest('.page') : null;
                            let finalTop = null;
                            let finalLeft = null;
                            let finalBottom = null;
                            let finalRight = null;
                            let positioned = false;

                            // ========== SMART @ MODE (triggered by data-top="@") ==========

                            if (top === '@' && trigger) {
                                console.log('===== SMART @ MODE ACTIVATED =====');
                                // Completely reset inline styles
                                BubbleText.removeAttribute('style');
                                BubbleText.style.cssText = '';
                                
                                // Set base styles (no inline max-height yet; we'll set it dynamically)
                                BubbleText.style.setProperty('width', 'fit-content', 'important');
                                BubbleText.style.setProperty('height', 'fit-content', 'important');
                                BubbleText.style.setProperty('max-width', 'var(--tt-max-width)');
                                // Do NOT set max-height here – will be set later based on available space
                                BubbleText.style.setProperty('overflow-x', 'hidden');
                                BubbleText.style.setProperty('overflow-y', 'auto');
                                BubbleText.style.setProperty('word-wrap', 'break-word');
                                BubbleText.style.setProperty('overflow-wrap', 'break-word');
                                BubbleText.style.setProperty('box-sizing', 'border-box', 'important');
                                BubbleText.style.setProperty('position', 'fixed', 'important');
                                BubbleText.style.setProperty('visibility', 'visible');
                                BubbleText.style.setProperty('opacity', '0');
                                BubbleText.style.setProperty('transition', 'all 0.5s cubic-bezier(0.65, 0, 0.35, 1)');
                                BubbleText.style.setProperty('background', 'rgba(0, 0, 0, 0.45)');
                                BubbleText.style.setProperty('backdrop-filter', 'blur(15px)');
                                BubbleText.style.setProperty('border-radius', '8px');
                                BubbleText.style.setProperty('box-shadow', '0 5px 5px rgba(0, 0, 0, 0.95)');
                                BubbleText.style.setProperty('border', '1px solid rgba(255, 255, 255, 0.2)');
                                BubbleText.style.setProperty('padding', '10px');
                                BubbleText.style.setProperty('font-size', '0.8em');
                                BubbleText.style.setProperty('color', '#b0e0ff');
                                BubbleText.style.setProperty('font-family', 'Arial, sans-serif');
                                BubbleText.style.setProperty('z-index', '9999');
                                BubbleText.style.setProperty('white-space', 'normal');
                                
                                // Force layout to get accurate dimensions
                                const BubbleTextHeightNow = BubbleText.offsetHeight;
                                const BubbleTextWidthNow = BubbleText.offsetWidth;
                                console.log('Computed width:', BubbleTextWidthNow);
                                console.log('Computed height:', BubbleTextHeightNow);
                                
                                const triggerRect = trigger.getBoundingClientRect();
                                const viewportWidth = window.innerWidth;
                                const viewportHeight = window.innerHeight;
                                
                                // ----- Horizontal positioning (align with trigger's left edge, prevent overflow) -----
                                const sideMargin = viewportWidth * 0.05;   // 5vw from edges
                                let leftPos = triggerRect.left;            // start at trigger's left edge
                                if (leftPos + BubbleTextWidthNow + sideMargin > viewportWidth) {
                                    leftPos = viewportWidth - BubbleTextWidthNow - sideMargin;
                                }
                                leftPos = Math.max(sideMargin, leftPos);    // ensure left margin
                                
                                // ----- Vertical positioning (smart flip: below if enough space, else above) -----
                                // Full content fits below → place below with natural height.
                                // Full content doesn’t fit below, but a 3‑line (4.5em) version does → place below with max-height: 4.5em.
                                // Full content fits above → place above with natural height (popup bottom aligned to trigger top – gap).
                                // Else → place above with max-height clamped to available space, and popup’s top aligned to vertMargin (or bottom fixed).

                                // ----- Vertical positioning with multi‑case logic (using top positioning only) -----
                                const gap = 20;
                                const vertMargin = viewportHeight * 0.05;   // 5% of viewport height
                                const threeLineHeight = parseFloat(getComputedStyle(BubbleText).fontSize) * 1.5 * 3; // ≈4.5em in px

                                // Case 1: natural popup fits below
                                const naturalFitsBelow = (triggerRect.bottom + gap + BubbleTextHeightNow + vertMargin) <= viewportHeight;

                                // Case 2: shrunk to 3 lines fits below
                                const shrunkFitsBelow = (triggerRect.bottom + gap + threeLineHeight + vertMargin) <= viewportHeight;

                                // Case 3: natural popup fits above
                                const naturalTop = triggerRect.top - gap - BubbleTextHeightNow;
                                const naturalFitsAbove = (naturalTop - vertMargin) >= 0;

                                if (naturalFitsBelow) {
                                    // Place below with natural height (no max-height limit)
                                    finalTop = triggerRect.bottom + gap;
                                    finalBottom = null;
                                    console.log('Case 1: natural below, finalTop =', finalTop);
                                } 
                                else if (shrunkFitsBelow) {
                                    // Place below, but cap max-height to available space below (prevent overflow)
                                    finalTop = triggerRect.bottom + gap;
                                    finalBottom = null;
                                    const availableBelow = viewportHeight - (triggerRect.bottom + gap + vertMargin);
                                    BubbleText.style.maxHeight = Math.max(0, availableBelow) + 'px';
                                    BubbleText.style.minHeight = '4.5em';   // force at least 3 lines (optional)
                                    console.log('Case 2: shrunk below (maxHeight = available space), finalTop =', finalTop);
                                }
                                else if (naturalFitsAbove) {
                                    // Place above with natural height
                                    finalTop = triggerRect.top - BubbleTextHeightNow + gap;
                                    finalBottom = null;
                                    console.log('Case 3: natural above, finalTop =', finalTop);
                                } 
                                else {
                                    // Place above and clamp height to available space
                                    finalTop = vertMargin + gap;
                                    finalBottom = null;
                                    const maxHeightAbove = triggerRect.top  - vertMargin;
                                    BubbleText.style.maxHeight = Math.max(0, maxHeightAbove) + 'px';
                                    console.log('Case 4: clamped above, finalTop =', finalTop, 'maxHeight =', BubbleText.style.maxHeight);
                                }
                                
                                finalLeft = leftPos;
                                positioned = true;
                                console.log('Final top:', finalTop, 'final bottom:', finalBottom, 'left:', finalLeft);
                            }
                                                        
                            // ========== END SMART @ MODE ==========

                            if (!positioned) {
                                // Vertical centering (center-height or center-both)
                                if (pos === 'center-height' || pos === 'center-both') {
                                    const BubbleTextHeight = BubbleText.getBoundingClientRect().height;
                                    if (pageElement) {
                                        const pageRect = pageElement.getBoundingClientRect();
                                        const cs = getComputedStyle(pageElement);
                                        const paddingTop = parseFloat(cs.paddingTop);
                                        const paddingBottom = parseFloat(cs.paddingBottom);
                                        const contentHeight = pageRect.height - paddingTop - paddingBottom;
                                        const contentTop = pageRect.top + paddingTop;
                                        finalTop = contentTop + (contentHeight / 2) - (BubbleTextHeight / 2);
                                    } else {
                                        finalTop = (window.innerHeight / 2) - (BubbleTextHeight / 2);
                                    }
                                }

                                // Horizontal centering (center-width or center-both)
                                if (pos === 'center-width' || pos === 'center-both') {
                                    const BubbleTextWidthNow = BubbleText.getBoundingClientRect().width;
                                    if (pageElement) {
                                        const pageRect = pageElement.getBoundingClientRect();
                                        const cs = getComputedStyle(pageElement);
                                        const paddingLeft = parseFloat(cs.paddingLeft);
                                        const paddingRight = parseFloat(cs.paddingRight);
                                        const contentWidth = pageRect.width - paddingLeft - paddingRight;
                                        const contentLeft = pageRect.left + paddingLeft;
                                        finalLeft = contentLeft + (contentWidth / 2) - (BubbleTextWidthNow / 2);
                                    } else {
                                        finalLeft = (window.innerWidth / 2) - (BubbleTextWidthNow / 2);
                                    }
                                    if (pos === 'center-width') {
                                        if (bottom !== undefined) BubbleText.style.bottom = bottom;
                                        else if (top !== undefined && top !== '@') BubbleText.style.top = top;
                                    }
                                }

                                // Bottom positioning modes
                                if (bottomModes.includes(pos)) {
                                    let gapPx = 0;
                                    if (bottomGap) {
                                        const gapMatch = bottomGap.match(/^([\d.]+)(vh|px)$/);
                                        if (gapMatch) {
                                            const num = parseFloat(gapMatch[1]);
                                            const unit = gapMatch[2];
                                            if (unit === 'vh') gapPx = (num / 100) * window.innerHeight;
                                            else gapPx = num;
                                        }
                                    }
                                    const BubbleTextHeight = BubbleText.offsetHeight;
                                    let newTop;
                                    if (pageElement) {
                                        const pageRect = pageElement.getBoundingClientRect();
                                        newTop = pageRect.bottom - BubbleTextHeight - gapPx;
                                        newTop = Math.max(pageRect.top + 10, newTop);
                                    } else {
                                        newTop = window.innerHeight - BubbleTextHeight - gapPx;
                                        newTop = Math.max(10, newTop);
                                    }
                                    finalTop = newTop;

                                    const BubbleTextWidthNow = BubbleText.getBoundingClientRect().width;
                                    const innerPadding = 10;
                                    let newLeft = null;

                                    if (pos === 'bottom-left') {
                                        if (pageElement) newLeft = pageRect.left + innerPadding;
                                        else newLeft = innerPadding;
                                    } else if (pos === 'bottom-right') {
                                        if (pageElement) newLeft = pageRect.right - BubbleTextWidthNow - innerPadding;
                                        else newLeft = window.innerWidth - BubbleTextWidthNow - innerPadding;
                                    } else if (pos === 'bottom-center') {
                                        if (pageElement) {
                                            const pageRect = pageElement.getBoundingClientRect();
                                            newLeft = (pageRect.left + pageRect.right) / 2 - BubbleTextWidthNow / 2;
                                            newLeft = Math.max(pageRect.left + innerPadding, Math.min(newLeft, pageRect.right - BubbleTextWidthNow - innerPadding));
                                        } else {
                                            newLeft = (window.innerWidth / 2) - (BubbleTextWidthNow / 2);
                                            newLeft = Math.max(innerPadding, Math.min(newLeft, window.innerWidth - BubbleTextWidthNow - innerPadding));
                                        }
                                    } else if (pos === 'bottom-page') {
                                        if (left !== undefined && left !== '@') newLeft = left;
                                    }
                                    if (newLeft !== null) finalLeft = newLeft;
                                }
                            }

                            // Apply final positions
                            if (finalTop !== null) BubbleText.style.top = (typeof finalTop === 'number' ? finalTop + 'px' : finalTop);
                            if (finalBottom !== null) BubbleText.style.bottom = (typeof finalBottom === 'number' ? finalBottom + 'px' : finalBottom);
                            if (finalLeft !== null) BubbleText.style.left = (typeof finalLeft === 'number' ? finalLeft + 'px' : finalLeft);
                            if (finalRight !== null) BubbleText.style.right = (typeof finalRight === 'number' ? finalRight + 'px' : finalRight);
                            if (finalBottom !== null && finalTop === null) BubbleText.style.top = 'auto';
                            if (finalRight !== null && finalLeft === null) BubbleText.style.left = 'auto';

                            BubbleText.classList.add('show');
                            BubbleText.style.opacity = '';
                        });
                    });
                } else {
                    // Normal positioning (no special modes, no @)
                    if (bottom !== undefined) {
                        BubbleText.style.bottom = bottom;
                        BubbleText.style.top = 'auto';
                    } else if (top !== undefined) {
                        BubbleText.style.top = top;
                        BubbleText.style.bottom = 'auto';
                    }
                    if (right !== undefined) {
                        BubbleText.style.right = right;
                        BubbleText.style.left = 'auto';
                    } else if (left !== undefined) {
                        BubbleText.style.left = left;
                        BubbleText.style.right = 'auto';
                    }
                    BubbleText.classList.add('show');
                }
            } else {
                // Hide BubbleText
                BubbleText.classList.remove('show');
                const onTransitionEnd = () => {
                    BubbleText.className = '';
                    BubbleText.style.cssText = '';
                    BubbleText.innerHTML = '';
                    BubbleText.removeEventListener('transitionend', onTransitionEnd);
                };
                BubbleText.addEventListener('transitionend', onTransitionEnd);
                setTimeout(onTransitionEnd, 500);
            }
        }

       // ==================== BubbleText FUNCTION end ============================================


        // BUBBLETEXT LISTENER START ==================== ============================================
        // This click listener manages the BubbleText popup (tooltip-like overlay). When a user clicks on an element with class BubbleText-trigger, it:
        // - Closes any open popup if clicking outside the popup or on a different trigger.
        // - Gathers configuration from the trigger’s data attributes (data-top, data-left, data-position, data-animation, etc.) and from the trigger’s own CSS classes.
        // - Calculates optimal positioning – handles centering, clamping to viewport or page edges, and a “smart” @ mode that automatically places the popup below or 
        //      above the trigger depending on available space (and can limit height to avoid overflow).
        // - Shows the popup by calling toggleBubbleText(…) with the appropriate parameters.
        // - Handles font loading – waits for fonts to load before showing to avoid layout shifts.
        // - In essence, it’s a custom popup system that adapts its size and position to always stay fully visible within the viewport or its parent page.        
        
        document.addEventListener('click', function(e) {
            try {

                const trigger = e.target.closest('.BubbleText-trigger');
                const BubbleText = document.getElementById('BubbleText');

                // If BubbleText is open and clicking outside, close it
                if (BubbleText.classList.contains('show') && !trigger && !BubbleText.contains(e.target)) {
                    toggleBubbleText('', '', '', '', '', 'no');
                    return;
                }

                if (!trigger) return;

                e.stopPropagation();

                // --- Collect extra classes (exclude alignment classes) ---
                let extraClasses = [];
                trigger.classList.forEach(cls => {
                    if (cls !== 'BubbleText-trigger' && !cls.startsWith('left-justified') && !cls.startsWith('right-justified') && !cls.startsWith('center-justified')) {
                        extraClasses.push(cls);
                    }
                });

                // --- Read data attributes (trim strings) ---
                let top = trigger.dataset.top ? trigger.dataset.top.trim() : undefined;
                let left = trigger.dataset.left ? trigger.dataset.left.trim() : undefined;
                let bottom = trigger.dataset.bottom ? trigger.dataset.bottom.trim() : undefined;
                let right = trigger.dataset.right ? trigger.dataset.right.trim() : undefined;
                let bottomGap = trigger.dataset.bottomGap ? trigger.dataset.bottomGap.trim() : undefined;
                let position = trigger.dataset.position ? trigger.dataset.position.trim() : 'fixed';
                const rawHeight = trigger.dataset.height || 'auto';
                const rawWidth = trigger.dataset.width || 'auto';

                const rect = trigger.getBoundingClientRect();
                const bodyStyles = window.getComputedStyle(document.body);
                const padding = Math.max(24, window.innerWidth * 0.04);
                const extra = 22;

                const addPxIfNumber = (value) => {
                    if (!isNaN(value) && value !== '') return value + 'px';
                    return value;
                };

                if (top !== undefined) top = addPxIfNumber(top);
                if (left !== undefined) left = addPxIfNumber(left);
                if (bottom !== undefined) bottom = addPxIfNumber(bottom);
                if (right !== undefined) right = addPxIfNumber(right);

                let height = addPxIfNumber(rawHeight);
                let width = addPxIfNumber(rawWidth);

                // --- Special positioning handling (center, @, 100% 100%) ---
                if (position !== 'absolute') {
                    let BubbleTextWidth = parseFloat(trigger.dataset.width);
                    let BubbleTextHeight = parseFloat(trigger.dataset.height);
                    let totalBubbleTextWidth = BubbleTextWidth ? BubbleTextWidth + extra : null;
                    let totalBubbleTextHeight = BubbleTextHeight ? BubbleTextHeight + extra : null;

                    if (top === 'center') {
                        if (totalBubbleTextHeight) {
                            let centerTop = (window.innerHeight / 2) - (totalBubbleTextHeight / 2);
                            centerTop = Math.max(padding, Math.min(centerTop, window.innerHeight - totalBubbleTextHeight - padding));
                            top = centerTop + 'px';
                        } else {
                            top = '50%';
                        }
                    }
                    if (left === 'center') {
                        if (totalBubbleTextWidth) {
                            let centerLeft = (window.innerWidth / 2) - (totalBubbleTextWidth / 2);
                            centerLeft = Math.max(padding, Math.min(centerLeft, window.innerWidth - totalBubbleTextWidth - padding));
                            left = centerLeft + 'px';
                        } else {
                            left = '50%';
                        }
                    }
                }

                // --- Clamping for normal positioning ---
                let maxHeight = null;
                const measurementModes = ['bottom-page', 'center-height', 'center-width', 'center-both'];
                if (!measurementModes.includes(position.toLowerCase())) {
                    const pageElement = trigger.closest('.page');

                    if (pageElement) {
                        const pageRect = pageElement.getBoundingClientRect();
                        const innerPadding = 10;

                        let topPx = toPixels(top, 'height');
                        let leftPx = toPixels(left, 'width');
                        let widthPx = toPixels(width, 'width');
                        let heightPx = toPixels(height, 'height');

                        let totalW = !isNaN(widthPx) ? widthPx + extra : null;
                        let totalH = !isNaN(heightPx) ? heightPx + extra : null;

                        // clamp top/left
                        if (!isNaN(topPx) && totalH !== null) {
                            let newTop = topPx;
                            const minTop = pageRect.top + innerPadding;
                            const maxTop = pageRect.bottom - totalH - innerPadding;
                            if (newTop < minTop) newTop = minTop;
                            if (newTop > maxTop) newTop = maxTop;
                            if (newTop !== topPx) {
                                top = newTop + 'px';
                                topPx = newTop;
                            }
                        }
                        if (!isNaN(leftPx) && totalW !== null) {
                            let newLeft = leftPx;
                            const minLeft = pageRect.left + innerPadding;
                            const maxLeft = pageRect.right - totalW - innerPadding;
                            if (newLeft < minLeft) newLeft = minLeft;
                            if (newLeft > maxLeft) newLeft = maxLeft;
                            if (newLeft !== leftPx) {
                                left = newLeft + 'px';
                                leftPx = newLeft;
                            }
                        }
                        // overflow handling
                        if (!isNaN(topPx) && totalH !== null) {
                            const availableHeight = pageRect.bottom - topPx - innerPadding;
                            if (totalH > availableHeight) {
                                maxHeight = availableHeight - extra;
                            }
                        }
                        if (!isNaN(leftPx) && totalW !== null) {
                            const availableWidth = pageRect.right - leftPx - innerPadding;
                            if (totalW > availableWidth) {
                                const newContentWidth = Math.max(0, availableWidth - extra);
                                width = newContentWidth + 'px';
                            }
                        }
                    }
                }

                // --- Prepare remaining parameters ---
                const rawTiptext = trigger.dataset.bbbltext || 'Default BubbleText';
                const animation = trigger.dataset.animation || 'fade';
                const textAlign = trigger.dataset.textalign || 'left';
                const bbbltext = htmlEncodeBubbleTextText(rawTiptext);

                const isCurrentlyOpen = BubbleText.classList.contains('show') && BubbleText.innerHTML.includes(rawTiptext);

                if (isCurrentlyOpen) {
                    toggleBubbleText('', '', '', '', '', 'no');
                } else {
                    const showBubbleText = () => {
                        toggleBubbleText(top, left, height, width, bbbltext, 'yes', animation, textAlign, position, extraClasses, bottom, maxHeight, bottomGap, trigger, right);
                        // Force layout recalculation after the BubbleText is visible
                        requestAnimationFrame(() => {
                            const t = document.getElementById('BubbleText');
                            if (t && t.classList.contains('show')) t.scrollTop;
                        });
                    };
                    if (document.fonts) {
                        document.fonts.ready.then(showBubbleText);
                    } else {
                        showBubbleText();
                    }
                }

            } catch (err) {
                console.error('Error in click listener:', err);
            }
        });

        // ==================== BubbleText INSIDE CLICK close START ====================================
        document.addEventListener('click', function(e) {
            const BubbleText = document.getElementById('BubbleText');
            if (BubbleText.contains(e.target)) {
                e.stopPropagation(); // prevent interfering with other listeners
                toggleBubbleText('', '', '', '', '', 'no');
            }
        });
        // ==================== BubbleText INSIDE CLICK close END ====================================

        // BUBBLETEXT LISTENER END ===================================================================


        // ==================== IMAGE CAPTION LISTENER ===============================================================
        // This code enables mobile‑friendly behavior for image captions:
        // - Captions can be shown/hidden by tapping on them.
        // - Tapping outside any caption closes all open captions.
        // - Touching a caption does not cause the page to scroll (improves usability).

        // FIXED: Image caption handling
        document.addEventListener('DOMContentLoaded', () => {

            // Adds a click listener to each caption popup.
            // When tapped, it toggles the popup’s visibility:
            // If visible → hides it (opacity 0, move up, remove class).
            // If hidden → shows it (opacity 1, reset position, add class).
            // e.stopPropagation() prevents the click from bubbling up to the global click handler (which would close it immediately).

            document.querySelectorAll('.image-caption-popup').forEach(caption => {
                caption.addEventListener('click', (e) => {
                    e.stopPropagation();
                    
                    // Toggle visibility
                    if (caption.style.opacity === '1' || 
                        getComputedStyle(caption).opacity === '1') {
                        caption.style.opacity = '0';
                        caption.style.transform = 'translateY(-10px)';
                        caption.classList.remove('mobile-visible');
                    } else {
                        caption.style.opacity = '1';
                        caption.style.transform = 'translateY(0)';
                        caption.classList.add('mobile-visible');
                    }
                });
            });

            // Close all captions when clicking elsewhere (only on mobile)
            // Listens for clicks anywhere on the page.
            // If the click target is not inside any caption popup (.closest('.image-caption-popup') returns null), it hides all open captions.
            // This ensures that tapping outside a popup closes it.

            document.addEventListener('click', (e) => {
                // Only close if not clicking on a caption
                if (!e.target.closest('.image-caption-popup')) {
                    document.querySelectorAll('.image-caption-popup').forEach(caption => {
                        caption.style.opacity = '0';
                        caption.style.transform = 'translateY(-10px)';
                        caption.classList.remove('mobile-visible');
                    });
                }
            });

            // For each image container, listens for touchstart events.
            // If the touch starts on a caption popup, it calls e.preventDefault() to prevent the browser from scrolling while the user interacts with the popup (e.g., toggling visibility).
            // { passive: false } allows preventDefault() to work.
            // Add touch events for mobile

            document.querySelectorAll('.image-container').forEach(container => {
                container.addEventListener('touchstart', (e) => {
                    // Prevent default to avoid scrolling issues
                    if (e.target.closest('.image-caption-popup')) {
                        e.preventDefault();
                    }
                }, { passive: false });
            });
        });  

        // Force reflow for all right-floated image containers
        // The fixFloatRight function forces a browser reflow (layout recalculation) for all elements with class image-align-right. It does this by:
        // - Reading a layout property (container.offsetHeight) – this forces the browser to compute the current layout.
        // - Temporarily setting display: none and reading offsetHeight again to force another reflow.
        // - Restoring display to its original value (empty string).
        //This sequence forces the browser to recalculate the positions and dimensions of those containers, which can fix rendering bugs where 
            //right‑floated images are not properly wrapped by text (especially after images load asynchronously).
        // The function is triggered:
        // - On the window load event (after all images and resources have loaded).
        // - After a 100ms delay (fallback in case the load event already fired before the listener was attached).
        // - This ensures that right‑floated images display correctly (text wraps around them) even if the initial layout was incorrect due to image loading timing.

        function fixFloatRight() {
            document.querySelectorAll('.image-align-right').forEach(container => {
                // Trigger a reflow by reading a layout property
                container.offsetHeight; 
                // Optionally, add/remove a class to force repaint
                container.style.display = 'none';
                container.offsetHeight; // force reflow
                container.style.display = '';
            });
        }

        // Run after all images are loaded
        window.addEventListener('load', fixFloatRight);
        // Also run after a short delay (fallback)
        setTimeout(fixFloatRight, 100);

        // ==================== IMAGE CAPTION LISTENER END ===========================================================

        // ==================== Navigation LISTENER Begin ==============================================
        // Page Navigation icons anywhere in content
        document.querySelectorAll('.next-page').forEach(el => {
            el.addEventListener('click', (e) => {
                e.preventDefault();
                nextPage();
            });
        });
        document.querySelectorAll('.prev-page').forEach(el => {
            el.addEventListener('click', (e) => {
                e.preventDefault();
                prevPage();
            });
        });
        // ==================== Navigation LISTENER End ================================================  

        // ==================== Page Build Function Start ================================================ 

        // This function activatePageFromHash is used to restore the last viewed page when the page is loaded with a URL fragment (e.g., #page-3). It:
        // Reads the URL’s hash (the part after #).
        // Tries to find a .page element whose id matches the hash (e.g., page-3).
        // If found, it determines the index of that page in the list of all pages.
        // If the page exists and is not already active, it calls goToPage(pageNum) to navigate there.
        // This enables deep linking – sharing a link that opens the book directly at a specific page, not just the first page. It is called during initial page load after the default active page is set, allowing the hash to override the default.
        
        function activatePageFromHash() {
            const hash = window.location.hash;
            if (hash) {
                const targetPage = document.querySelector(hash);
                if (targetPage && targetPage.classList.contains('page')) {
                    const allPages = document.querySelectorAll('.page');
                    let pageNum = -1;
                    for (let i = 0; i < allPages.length; i++) {
                        if (allPages[i].id === hash.substring(1)) {
                            pageNum = i;
                            break;
                        }
                    }
                    if (pageNum !== -1 && pageNum !== currentPage) {
                        goToPage(pageNum);
                    }
                }
            }
        }

        // Calculate proper page number based on Page0_skip and TOC
        // The calculatePageNumber(index) function determines what text to display as the page number in the 
        // page header (e.g., “Title”, an empty string, or a numeric page number). It uses the configuration 
        // flags Page0_skip and whether a TOC page exists to decide the mapping from the page index (0‑based) to the displayed label.
        // - If title page is skipped and TOC exists:
        //      Index 0 → "" (TOC page shows no number), Index 1 → 1, Index 2 → 2, etc.
        // - If title page exists and TOC exists:
        //      Index 0 → "Title", Index 1 → "" (TOC), Index 2 → 1, Index 3 → 2, etc.
        // - If title page is skipped and no TOC:
        //      Index 0 → 1, Index 1 → 2, etc. (direct numbering)
        // - If title page exists and no TOC:
        //      Index 0 → "Title", Index 1 → 1, Index 2 → 2, etc.
        // This function is used when generating the page number in the header (via pageNumber.innerHTML). 
        //      It ensures that the displayed page number matches the expected labeling (e.g., the first content page is “1”, not “2”).

        function calculatePageNumber(index) {
            const page0Skipped = {Page0_skip};
            const hasTOC = document.getElementById('page-toc') !== null;
            
            // Table of contents - TOC
            if (page0Skipped && hasTOC) {
                // Case 1: Both flags true
                return index === 0 ? "" : index;
            } else if (!page0Skipped && hasTOC) {
                // Case 2: Only TOC enabled
                return index === 0 ? "Title" : (index === 1 ? "" : index - 1);
            } else if (page0Skipped && !hasTOC) {
                // Case 3: Only Page0_skip enabled
                return index + 1;
            } else {
                // Case 4: Neither flag set
                return index === 0 ? "Title" : index;
            }
        }

        function updateSliderTrack() {
            const value = slider.value;
            const max = slider.max;
            const percent = (value / max) * 100;
            sliderTrack.style.width = `${percent}%`;
        }

        function goToPage(pageNum) {
            console.log('goToPage called with', pageNum, 'currentPage =', currentPage, 'totalPages =', totalPages);
            if (pageNum < 0 || pageNum > totalPages) return;
            if (pageNum === currentPage) return;   // Avoid unnecessary transition
            
            const currentActive = document.querySelector('.page.active');
            if (currentActive) {
                currentActive.classList.remove('active');
                currentActive.classList.add('exit');
            }
            
            setTimeout(() => {
                if (currentActive) {
                    currentActive.classList.remove('exit');
                }
                currentPage = pageNum;
                pages[currentPage].classList.add('active');
                updateSlider();
                updateProgress();
                
                // Remove any #page-... from the URL bar (keep only base path)
                history.pushState(null, '', window.location.pathname);
            }, 300);
        }

        function nextPage() {
            console.log('nextPage called, currentPage =', currentPage, 'totalPages =', totalPages);
            if (currentPage < totalPages - 1) {
                console.log('Going to page', currentPage + 1);
                goToPage(currentPage + 1);
            } else {
                console.log('Already at last page');
            }
        }

        function prevPage() {
            if (currentPage > 0) {
                // If we're on the first content page and page0 is skipped, don't go back
                if (page0Skipped && currentPage === 0) {
                    return;
                }
                goToPage(currentPage - 1);
            }
        }

        function handleSwipe() {
            const threshold = window.innerWidth * (CONFIG.ARW_HOVER_WIDTH / 100);
            const distance = touchStartX - touchEndX;
            
            if (Math.abs(distance) < threshold) return;
            
            if (distance > 0) {
                nextPage();
            } else {
                prevPage();
            }
        } 

        // ==================== Page Build Function end ================================================

        // ==================== Page Build Listener Start ========================================================

        // Initialize with correct active page
        // Deactivates all pages by removing the active class from every .page element.
        // Sets the active page based on configuration:
            // - If the title page exists and is not skipped (!page0Skipped), it activates the title page (index 0).
            // - Otherwise, it activates the page at INITIAL_PAGE (usually 0, which could be the TOC or first content page).
        // Checks the URL hash (e.g., #page-3) and navigates to that page using activatePageFromHash() (overriding 
            //the initial active page if a hash is present).
        // Adds a click listener to a .back-to-list button (if present) that opens a configured URL ({BkLinkURL}) 
        // add listener for keyboard
        // adds listener for left right arrow
        // adds listener for Back-to-list
        // Enabbles back-to-TOC to work correctly
        // update SLIDER
        // UPDATE PROGRESSBAR
        // Append children to page-header
        // Insert Header to Page-content (Page content is only child of .page creater for .apge::after - whitewash glass effect)
        // in the same tab (_self).
        // In essence, it handles the initial page activation and supports deep linking via URL fragments.

        document.addEventListener('DOMContentLoaded', () => {
            // First deactivate all pages
            pages.forEach(page => page.classList.remove('active'));
            
            // If title page exists and isn't skipped, start there
            if (!page0Skipped && document.getElementById('page-0')) {
                currentPage = 0;
                document.getElementById('page-0').classList.add('active');
            } else {
                // Otherwise start at TOC or first content page
                currentPage = INITIAL_PAGE;
                pages[currentPage].classList.add('active');
            }

            // After setting the initial active page, check URL hash
            activatePageFromHash();
            
            const booklistBtn = document.querySelector('.back-to-list');
            if (booklistBtn) {
                booklistBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    let url = '{BkLinkURL}';
                    if (!url.startsWith('http')) {
                        url = 'https://' + url;
                    }
                    // window.open(url, '_blank');
                    window.open(url, '_self');
                });
            }

            updateSlider();
            updateProgress();
            
            // Add header elements to all pages except the title page (if shown)
            // Determines the starting index (startPage) based on whether the title page is skipped (Page0_skip). If the title page exists (
                // Page0_skip = false), it starts at index 1 (skipping the title page at index 0). If the title page is skipped, 
                // it starts at index 0 (first content page).
            // Loops through all .page elements from startPage to the end, but skips the TOC page if its id is "page-toc".
            // For each content page, it creates a <div class="page-header"> and populates it with three elements:
            // Left side: a back‑to‑TOC button (<a class="back-to-toc">) if a TOC page exists. The button contains the emoji 🗂️.
            // Center: the book title (<div class="book-title">) with text from {BkPage0_Title} (later replaced by Python).
            // Right side: the page number (<div class="page-number">) which includes a clickable bookmark emoji (🔖) 
                // that calls copyCurrentPageUrl(event) when clicked.
            // Inserts the header as the first child of the page’s .page-content container (so it appears at the top of the scrollable area). 
                // If .page-content is not found, it falls back to inserting directly into the .page element.
            // In summary, this code adds a consistent navigation header (with TOC button, book title, and copy‑link + page number) to every 
                //content page, making the user interface functional and uniform across all pages.
            
            const startPage = {Page0_skip} ? 0 : 1;
            for (let i = startPage; i < pages.length; i++) {
                if (pages[i].id === 'page-toc') continue;   
                         
                const header = document.createElement('div');
                header.className = 'page-header';
                
                // Back to TOC button (left side)
                if (document.getElementById('page-toc')) {
                    const backButton = document.createElement('a');
                    backButton.className = 'back-to-toc';
                    backButton.href = '#page-toc';
                    backButton.textContent = '🗂️'; 
                    // 'Contents';
                    header.appendChild(backButton);
                }

                // Book title (center) – create new element
                const titleSpan = document.createElement('div');
                titleSpan.className = 'book-title';
                titleSpan.textContent = '{BkPage0_Title}';   // placeholder – will be replaced by Python
                header.appendChild(titleSpan);
                                        
                // Page number (right side)
                const pageNumber = document.createElement('div');
                pageNumber.className = 'page-number';
                // to remove 🔖 <ClickbookMark> uncomment this
                // pageNumber.textContent = calculatePageNumber(i);
                // and comment this
                pageNumber.innerHTML = '<a href="javascript:void(0)" onclick="copyCurrentPageUrl(event); return false;"><span class="glassbtn">🔖</span></a>' + calculatePageNumber(i);
                header.appendChild(pageNumber);
                
                // Insert header into .page-content (instead of .page)
                const pageContent = pages[i].querySelector('.page-content');
                if (pageContent) {
                    pageContent.insertBefore(header, pageContent.firstChild);
                } else {
                    // Fallback (should not happen)
                    pages[i].insertBefore(header, pages[i].firstChild);
                }
            }
            
            // Touch events for swipe
            let touchStartX = 0;
            let touchEndX = 0;

            //TouchScreen Swipe. TO be tested Later
            document.addEventListener('touchstart', (e) => {
                touchStartX = e.touches[0].clientX;
            }, { passive: true });

            document.addEventListener('touchend', (e) => {
                touchEndX = e.changedTouches[0].clientX;
                handleSwipe();
            }, { passive: true });            
            
            // Keyboard navigation
            document.addEventListener('keydown', (e) => {
                switch(e.key) {
                    case 'ArrowRight':
                    case 'ArrowDown':
                    case 'PageDown':
                        nextPage();
                        break;
                    case 'ArrowLeft':
                    case 'ArrowUp':
                    case 'PageUp':
                        prevPage();
                        break;
                }
            });

            // Update slider track fill
            slider.addEventListener('input', updateSliderTrack);
            updateSliderTrack();
            
            // Connect slider to page navigation
            slider.addEventListener('change', function() {
                goToPage(parseInt(this.value));
            });
            
            //This code listens for clicks on any element with the class toc-link (typically Table of Contents links). When clicked, it:
            //Prevents the default link behavior (so the URL doesn’t change with a #).
            //Extracts the target ID from the link’s href attribute (e.g., #page-3).
            //Finds the corresponding .page element by matching its id.
            //Determines the page index by iterating over all .page elements.
            //Calls goToPage(pageNum) to navigate to that page.
            //Smoothly scrolls the newly active page to the top (using scrollTo({ top: 0, behavior: 'smooth' })).

            document.querySelectorAll('.toc-link').forEach(link => {
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    const targetId = link.getAttribute('href');
                    const targetPage = document.querySelector(targetId);
                    
                    if (targetPage) {
                        const allPages = document.querySelectorAll('.page');
                        let pageNum = 0;
                        for (let i = 0; i < allPages.length; i++) {
                            if (allPages[i].id === targetId.substring(1)) {
                                pageNum = i;
                                break;
                            }
                        }
                        goToPage(pageNum);
                        
                        // Smooth scroll to top of page
                        document.querySelector('.page.active').scrollTo({
                            top: 0,
                            behavior: 'smooth'
                        });
                    }
                });            
            });  

            // Arrow click events for next and previous page 
            leftArrowContainer.addEventListener('click', prevPage);
            rightArrowContainer.addEventListener('click', nextPage);

            // TOC Navigation (handles both list and button styles)
            // This code adds click handlers to all elements with the class .back-to-toc (typically a button or link that returns to the Table of Contents). When clicked, it:
            // - Prevents the default link behavior (so the URL doesn’t change with a #).
            // - Extracts the target ID from the href attribute (e.g., #page-toc).
            // - Finds the corresponding .page element.
            // - Determines the index of that page by iterating over all .page elements.
            // - Calls goToPage(pageNum) to navigate to that page.
            // - Smooth‑scrolls the newly active page to the top (using scrollTo({ top: 0, behavior: 'smooth' })).
            // In short, it enables the “back to TOC” button to work correctly and ensures the TOC page appears at the top after navigation.

            document.querySelectorAll('.back-to-toc').forEach(link => {
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    const targetId = link.getAttribute('href');
                    const targetPage = targetId.startsWith('#') 
                        ? document.querySelector(targetId)
                        : document.getElementById(targetId);
                    
                    if (targetPage) {
                        const allPages = document.querySelectorAll('.page');
                        let pageNum = 0;
                        for (let i = 0; i < allPages.length; i++) {
                            if (allPages[i].id === targetId.replace('#', '')) {
                                pageNum = i;
                                break;
                            }
                        }
                        goToPage(pageNum);
                        
                        // Smooth scroll to top
                        document.querySelector('.page.active').scrollTo({
                            top: 0,
                            behavior: 'smooth'
                        });
                    }
                });
            });
                        

        });

        // ==================== Page Build Listener END ========================================================
                
       // ====================ENCRYPTION FUNCTION  Start ========================================================

        // The next set of functions are for code handling and encryption

        // Generate a random IV for AES-GCM
        function generateIV() {
            return crypto.getRandomValues(new Uint8Array(12));
        }

        // Generate salt for key derivation
        function generateSalt() {
            return crypto.getRandomValues(new Uint8Array(16));
        }

        // Convert string to Uint8Array
        function strToBuf(str) {
            return new TextEncoder().encode(str);
        }

        // Convert Uint8Array to string
        function bufToStr(buf) {
            return new TextDecoder().decode(buf);
        }

        // Derive a key from password and salt using PBKDF2
        async function deriveKey(password, salt) {
            const passBuf = strToBuf(password);
            const keyMaterial = await crypto.subtle.importKey(
                "raw", passBuf, "PBKDF2", false, ["deriveKey"]
            );
            return crypto.subtle.deriveKey(
                {
                name: "PBKDF2",
                salt: salt,
                iterations: 100000,
                hash: "SHA-256"
                },
                keyMaterial,
                { name: "AES-GCM", length: 256 },
                false,
                ["encrypt", "decrypt"]
            );
        }

        // Encrypt plaintext with password
        async function encrypt(plaintext, password) {
            const salt = generateSalt();
            const iv = generateIV();
            const key = await deriveKey(password, salt);
            const encrypted = await crypto.subtle.encrypt(
                { name: "AES-GCM", iv: iv },
                key,
                strToBuf(plaintext)
            );
            // Combine salt, iv, and encrypted data in base64 for storage/transmission
            const combined = new Uint8Array(salt.byteLength + iv.byteLength + encrypted.byteLength);
            combined.set(salt, 0);
            combined.set(iv, salt.byteLength);
            combined.set(new Uint8Array(encrypted), salt.byteLength + iv.byteLength);
            return btoa(String.fromCharCode(...combined));
        }

        // Decrypt encrypted base64 string with password
        async function decrypt(encryptedBase64, password) {
            const combined = Uint8Array.from(atob(encryptedBase64), c => c.charCodeAt(0));
            const salt = combined.slice(0, 16);
            const iv = combined.slice(16, 28);
            const data = combined.slice(28);
            const key = await deriveKey(password, salt);
            const decrypted = await crypto.subtle.decrypt(
                { name: "AES-GCM", iv: iv },
                key,
                data
            );
            return bufToStr(decrypted);
        }    

        // Make this function async and use await
        async function handleRedirect(inputId, correctCode, redirectUrl) {
            const input = document.getElementById(inputId);

            try {
                const password = "your-strong-password";
                
                const decrypted = await decrypt(redirectUrl, password);
                alert("Decrypted: " + decrypted);
                
                // Then the redirect logic
                if (input.value === correctCode) {
                    window.location.href = decrypted;
                } else {
                    alert("Invalid code - (" + input.value + "). Please try with the correct provided code.");
                }
            } catch (error) {
                console.error("Error:", error);
                alert("An error occurred during encryption/decryption");
            }
        }        
       // ====================ENCRYPTION FUNCTION  END ==========================================================
        
    </script>

    <!--
    # The <div id="BubbleText"></div> is the container element for the custom popup (tooltip) system. All the 
    # JavaScript functions that manage popups (toggleBubbleText, the click listeners, etc.) use this div to display 
    # the popup content. Without this element, the popup would have nowhere to appear, and the code would throw 
    # errors (e.g., document.getElementById('BubbleText') would return null). It is required for the popup 
    # functionality to work.
    -->

    <div id="BubbleText"></div>
        
</body>
</html>
"""

tip_string = """ <clickwordC=  |  | 
    \"
    <underline="<bold="Navigation tips ...">"><br>
        <ul>
        <li>For Previous page, click on left margin.</li>
        <li>For Next Page, click on right margin.</li>
        <li>Margins are 15% for your browser width.</li>
        <span style='line-height: 2.4em'>
            <li>Click <span class='glassbtn'> 📚 </span> at top left fof the Table of contents page only. Link to list of books</li>
            <li>Click <span class='glassbtn'> 🗂️ </span> at top left for table of contents</li>
            <li>Click <span class='glassbtn'> 🔖 </span> at top right to copy page bookmark (URL) to clipboard</li>
            <li>Click <span class='glassbtn'> 📸</span> To see image attribution </li>
            <li>Click <span class='glassbtn'> 👆</span> any where you see it, </li>
        </span>
            <ul>
            <li>Opens a webpage with additional information</li>
            <li>Opens a popup box with additional information.</li>
            </ul>
        </li>
        <li>Click on the Popup to make it go away.</li>
        </ul>
    "><br>
    <span style="font-size: .8em; text-align: center;"><paraitalicC=\'( click here for navigation tips )\'></span>
"""

#   CLEAN_UP START =============================================================================================

# a sort of search and replace pre-compiler
def pre_clean(content):
    
    DT = 5.5; DL = 6.5; BOTTOM_GAP= 0   # gap from page bottom in vh
    
    # This deletes from '///' to the end of the line
    content = re.sub(r'///.*$', '', content, flags=re.MULTILINE)
    # This removes everything from //* to *//, across newlines
    content = re.sub(r'//\*.*?\*//', '', content, flags=re.DOTALL)
    # Remove bold formatting (**text** or __text__)
    content = re.sub(r'(\*\*|__)(.*?)\1', r'\2', content)
    # Remove highlight formatting (==text==)
    content = re.sub(r'==(.*?)==', r'\1', content)
    # Remove italics (*text* or _text_)
    #content = re.sub(r'(\*|_)(.*?)\1', r'\2', content) # In the case of *** it becomes *
    content = re.sub(r'\*\*(?!\*)(.*?)\*\*(?!\*)', r'\1', content)
    content = re.sub(r'__(?!_)(.*?)__(?!_)', r'\1', content)

    # Remove emphasis tags (<em>text</em>)
    #content = re.sub(r'<em>(.*?)</em>', r'\1', content, flags=re.DOTALL)

    # convert <tiptext> to tip_string
    content = re.sub(r'<tiptext>', tip_string, content, flags=re.IGNORECASE)

    # convert <NEXTPAGE_ICON> to '<span class="next-page">👉</span>'
    content = re.sub(r'<\s*NEXTPAGE_ICON\s*>', "<span class='next-page'>👉</span>", content, flags=re.IGNORECASE | re.DOTALL)

    # convert <PREVPAGE_ICON> to '<span class="prev-page">👈</span>'
    content = re.sub(r'<\s*PREVPAGE_ICON\s*>', "<span class='prev-page'>👈</span>", content, flags=re.IGNORECASE | re.DOTALL)

    # convert LINKS from URL [text] (url) to <a href="url>test</a>
    content = re.sub(r'\[([^\]]+)\]\s*\(([^)]+)\)', r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>', content, flags=re.MULTILINE | re.DOTALL)

    # Replace <STARTPAGE>, <NEWPAGE>< <ENDPAGE> with <div style="break-after: page;"></div><br>
    content = re.sub( r'<\s*(?:firstpage|newpage|lastpage)\s*>', '<div style="break-after: page;"></div>', content, flags=re.IGNORECASE | re.MULTILINE  | re.DOTALL)

    # replace <CHAPTER="xxx"> with ## xxx also support 'xxx' there must be a space between ## and xxx
    content = re.sub(r'<\s*chapter\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^>]+?))\s*>', r'## \1\2\3', content, flags=re.IGNORECASE | re.DOTALL)

    # replace <IMAGE="xxx"> with ![[xxx]] and also support 'xxx'
    content = re.sub(r'<\s*image\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^>]+?))\s*>', r'![[\1\2\3]]', content, flags=re.IGNORECASE | re.DOTALL)

    #convert <Superscript=xxx> to <sup>xxx</sup> and SUBSCRIPT and BOLD and UNDERLINE and COLOR
    content = re.sub( r'<\s*color\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))\s*>(.*?)<\s*/\s*color\s*>', lambda m: f'<span style="color: {m.group(1) or m.group(2) or m.group(3)};">{m.group(4)}</span>',
                    content, flags=re.IGNORECASE | re.DOTALL )
    content = re.sub( r'<\s*superscript\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))\s*>', lambda m: f'<sup>{m.group(1) or m.group(2) or m.group(3)}</sup>', content, flags=re.IGNORECASE)
    content = re.sub( r'<\s*subscript\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))\s*>', lambda m: f'<sub>{m.group(1) or m.group(2) or m.group(3)}</sub>', content, flags=re.IGNORECASE )
    content = re.sub( r'<\s*bold\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))\s*>', lambda m: f'<b>{m.group(1) or m.group(2) or m.group(3)}</b>', content, flags=re.IGNORECASE )
    content = re.sub( r'<\s*underline\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))\s*>',lambda m: f'<u>{m.group(1) or m.group(2) or m.group(3)}</u>', content, flags=re.IGNORECASE)
    content = re.sub( r'<\s*italic\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))\s*>', lambda m: f'<i>{m.group(1) or m.group(2) or m.group(3)}</i>', content, flags=re.IGNORECASE)

    # Replace <TITLE="xxx"> with <p style="color: #f09e5a;"><span class="highlight-text">Fragility</span></p>xxx</span></p>
    content = content.replace('<br>', '___BR___')
    content = re.sub(r'<\s*title\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^>]+?))\s*>', r'<div style="color: #f09e5a;"><span class="highlight-text">\1\2\3</span></div>', content, flags=re.IGNORECASE | re.DOTALL)
    content = content.replace('___BR___', '<br>')

    #____________________________________________________________________________________________________________________________________________________________________
    # ClickwordInline: converts <ClickwordInline='content'> into a div with both margins

    def replace_clickwordinline(match):

        content_text = match.group(2).strip()     
        # Process any <clickword0> tags inside the content
        def replace_inner_clickword(m):
            a = m.group(1).strip()
            b = m.group(2).strip()
            inner_content = m.group(3) or m.group(4) or m.group(5)
            return f'<BBL-Txt="<ClickMe_icon>", ":[ | | |{a}%| {b}% | | | center-both | left ]{inner_content}">'  
        content_text = re.sub( r'<\s*clickword0\s*=\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(?:"([^"]*)"|\'([^\']*)\'|([^>]+?))\s*>', replace_inner_clickword, content_text, flags=re.IGNORECASE )
        
        # Hardcode both margins (left and right) and an empty class (so you can add later)
        margin = f'margin-left: var(--Lsafe-margin) !important; margin-right: var(--Rsafe-margin) !important; '
        return f'<div style="{margin}" class="">{content_text}</div>'

    # Match <ClickwordInline='...'> or <ClickwordInline="..."> (case-insensitive, optional spaces)
    content = re.sub(r'<\s*ClickwordInline\s*=\s*(["\'])(.*?)\1\s*>', replace_clickwordinline, content, flags=re.IGNORECASE | re.DOTALL)
  
    #________________________________ ParaitalicL - ParaintendtC - ParaitalicB - ParaitalicR_______________________________________________________________
    # THIS IS ABOUT Placing PARAGRAPHS (a DPOSITION REPLACEMENT)

    # converts <ParaitalicL="xxx">, <ParaitalicL='xxx'>, or <ParaitalicL=xxx> to <DPosition=':[left | paraitalicleft ] xxx'>:
    def replace_paraitalicL(match):
        content = match.group(1) or match.group(2) or match.group(3)
        # Escape any double quotes inside the content to avoid breaking the attribute
        content = content.replace('"', '&quot;')
        return f'<DPosition=":[left | paraitalicleft ] {content}">'
    content = re.sub(r'<\s*ParaitalicL\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^>\s]+))\s*>', replace_paraitalicL, content, flags=re.IGNORECASE | re.DOTALL)
    # converts <ParaitalicC="xxx">, <ParaitalicC='xxx'>, or <ParaitalicC=xxx> to <DPosition=':[both | paraitalicleft ] xxx'>:
    def replace_paraitalicC(match):
        content = match.group(1) or match.group(2) or match.group(3)
        # Escape any double quotes inside the content to avoid breaking the attribute
        content = content.replace('"', '&quot;')
        return f'<DPosition=":[center | paraitaliccenter ] {content}">'
    content = re.sub(r'<\s*ParaitalicC\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^>\s]+))\s*>', replace_paraitalicC, content, flags=re.IGNORECASE | re.DOTALL)
    # converts <ParaitalicB="xxx">, <ParaitalicB='xxx'>, or <ParaitalicB=xxx> to <DPosition=':[both | paraitalicleft ] xxx'>:
    def replace_paraitalicB(match):
        content = match.group(1) or match.group(2) or match.group(3)
        # Escape any double quotes inside the content to avoid breaking the attribute
        content = content.replace('"', '&quot;')
        return f'<DPosition=":[both | paraitalicleft ] {content}">'
    content = re.sub(r'<\s*ParaitalicB\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^>\s]+))\s*>', replace_paraitalicB, content, flags=re.IGNORECASE | re.DOTALL)
    # converts <ParaitalicR="xxx">, <ParaitalicR='xxx'>, or <ParaitalicR=xxx> to <DPosition=':[both | paraitalicleft ] xxx'>:
    def replace_paraitalicR(match):
        content = match.group(1) or match.group(2) or match.group(3)
        # Escape any double quotes inside the content to avoid breaking the attribute
        content = content.replace('"', '&quot;')
        return f'<DPosition=":[right | paraitalicleft ] {content}">'
    content = re.sub(r'<\s*ParaitalicR\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^>\s]+))\s*>', replace_paraitalicR, content, flags=re.IGNORECASE | re.DOTALL)  

    #_________________ClickwordL ClickwordC ClickwordR (float left center right)___________________________________________________________________________
    # THIS IS ABOUT PLACING THE CLICKWORD - (a BBL-Txt REPLACEMENT)

    # convert <clickwordL= a | b | "xxx"> to to <BBL-Txt=":[floatleft]<ClickMe_icon>", ":[ | | |a%| b% ]xxx">
    def replace_clickwordL(match):
        a = match.group(1).strip()   # first number
        b = match.group(2).strip()   # second number
        # Capture the content: group3 = double-quoted, group4 = single-quoted, group5 = unquoted (allows spaces)
        content = match.group(3) or match.group(4) or match.group(5)
        return f'<BBL-Txt=":[floatleft]<ClickMe_icon>", ":[ | | |{a}%| {b}% | | |center-both|left]{content}">'
    content = re.sub( r'<\s*clickwordL\s*=\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(?:"([^"]*)"|\'([^\']*)\'|([^>]+?))\s*>', replace_clickwordL, content, flags=re.IGNORECASE )
    # convert <clickwordC= a | b | "xxx"> to to <BBL-Txt=":[floatcenter]<ClickMe_icon>", ":[ | | |a%| b% ]xxx">
    def replace_clickwordC(match):
        a = match.group(1).strip()   # first number
        b = match.group(2).strip()   # second number
        # Capture the content: group3 = double-quoted, group4 = single-quoted, group5 = unquoted (allows spaces)
        content = match.group(3) or match.group(4) or match.group(5)
        return f'<BBL-Txt=":[floatcenter]<ClickMe_icon>", ":[ | | |{a}%| {b}% | | |center-both|left]{content}">'
    content = re.sub( r'<\s*clickwordc\s*=\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(?:"([^"]*)"|\'([^\']*)\'|([^>]+?))\s*>', replace_clickwordC, content, flags=re.IGNORECASE )
    # convert <clickwordR= a | b | "xxx"> to to <BBL-Txt=":[floatcenter]<ClickMe_icon>", ":[ | | |a%| b% ]xxx">
    def replace_clickwordR(match):
        a = match.group(1).strip()   # first number
        b = match.group(2).strip()   # second number
        # Capture the content: group3 = double-quoted, group4 = single-quoted, group5 = unquoted (allows spaces)
        content = match.group(3) or match.group(4) or match.group(5)
        return f'<BBL-Txt=":[floatright]<ClickMe_icon>", ":[ | | |{a}%| {b}% | | |center-both|left]{content}">'
    content = re.sub( r'<\s*clickwordr\s*=\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(?:"([^"]*)"|\'([^\']*)\'|([^>]+?))\s*>', replace_clickwordR, content, flags=re.IGNORECASE )
    # convert <clickword0= a | b | "xxx"> to to <BBL-Txt="<ClickMe_icon>", ":[ | | |a%| b% ]xxx">
    def replace_clickword0(match):
        a = match.group(1).strip()   # first number
        b = match.group(2).strip()   # second number
        # Capture the content: group3 = double-quoted, group4 = single-quoted, group5 = unquoted (allows spaces)
        content = match.group(3) or match.group(4) or match.group(5)
        return f'<BBL-Txt="<ClickMe_icon>", "[ | | |{a}%| {b}% | | |center-both|left]{content}">'
    content = re.sub( r'<\s*clickword0\s*=\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(?:"([^"]*)"|\'([^\']*)\'|([^>]+?))\s*>', replace_clickword0, content, flags=re.IGNORECASE )    
    #______________________________________________________________________________________________________________________________________________________

    # convert ,PageDivider> to <hr style="height: 1px; background-color: rgba(0,0,0,0.7) !important; border: none;">
    content = re.sub(r'<\s*pagedivider\s*>', '<hr style="height: 1.2px; background-color: var(--text-color); opacity: 0.3; border: none;">', content, flags=re.IGNORECASE)

    # convert <ClipBookMark="xxx"> to <a href="javascript:void(0)" onclick="copyCurrentPageUrl(event); return false;"><span class="glassbtn">🔖</span></a> <span class="glassbtnlbl">{(m.group(1) or m.group(2) or m.group(3)).strip()}</span>
    content = re.sub( r'<\s*clipbookmark(?:\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^>]+?)))?\s*>',
        lambda m: ( f'<DPosition=\':[ both | ] <a href="javascript:void(0)" onclick="copyCurrentPageUrl(event); return false;"><span class="glassbtn">🔖</span></a>'
            + (f' <span class="glassbtnlbl">{(m.group(1) or m.group(2) or m.group(3)).strip()}</span>' if m.group(1) or m.group(2) or m.group(3) else '')
            + f'\'>'), content, flags=re.IGNORECASE )

    # convert <IMAGEATR="label","URL"> 
    content = re.sub(
        r'<\s*imageatr\s*=\s*(.*?)\s*[,|]\s*(.*?)\s*>',
        lambda m: '<DPosition=\':[ both | ] <a href="{}" rel="noopener noreferrer"><span class="glassbtn">📸</span></a>&nbsp;<span class="glassbtnlbl";>{}</span>\'>'.format(
            m.group(2).strip(' "\''), m.group(1).strip(' "\'') ), content,flags=re.IGNORECASE | re.DOTALL )
    
    # replace <FOOTER=xxx>
    content = re.sub(r'<\s*FOOTER\s*=\s*(["\']?)([^>\'"]*)\1\s*>', "<DPosition=':[ both | glassbtnlbl ] \\2'>", content, flags=re.IGNORECASE | re.DOTALL)

    # replace <PAGE END MARKER="xxx"> with <p style="text-align: center; font-style: bold;"> xxx</p> ignore space and also support 'xxx'
    content = re.sub(r'<\s*PAGE\s+END\s+MARKER\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^>]+))\s*>', '<br><DPosition=\':[ center | glassbtnlbl ] <div style="text-align: center;">\\1\\2\\3</div>\'>', content, flags=re.IGNORECASE | re.DOTALL)

    #____________________________________________________________________________________________________________________________________________________________________
    def replace_dposition(match):
        param_str = match.group(2).strip() if match.group(2) else ''
        param_str = param_str.replace(',', '|')
        parts = [p.strip() for p in param_str.split('|')]
        # Pad to 2 parts
        while len(parts) < 2:
            parts.append('')
        w_raw = parts[0].lower()          # walign: both, left, right, center
        class_name = parts[1]              # CSS class name (no spaces, or quoted if needed)
        content_text = match.group(3).strip()

        # Margin styles based on walign
        margin = ''
        if w_raw == 'both':
            margin = f'margin-left: var(--Lsafe-margin) !important; margin-right: var(--Rsafe-margin) !important; '
        elif w_raw == 'left':
            margin = f'margin-left: var(--Lsafe-margin) !important; '
        elif w_raw == 'right':
            margin = f'margin-right: var(--Rsafe-margin) !important; '
        elif w_raw == 'center':
            margin = 'margin-left: auto !important; margin-right: auto !important; '

        # Build class attribute
        class_attr = f'class="{class_name}"' if class_name else ''

        # Assemble final div
        return f'<div style="{margin}" {class_attr}>{content_text}</div>'

    # old - content = re.sub(r'<\s*DPosition\s*=\s*(["\']):\[(.*?)\](.*?)\1\s*>',replace_dposition,content,flags=re.IGNORECASE | re.DOTALL)
    content = re.sub(r'<\s*DPosition\s*=\s*(["\']):\[(.*?)\](.*?)\1\s*>', replace_dposition, content, flags=re.IGNORECASE | re.DOTALL)

    #____________________________________________________________________________________________________________________________________________________________________

    # convert <ClickMe_icon> to <span class='glassbtn'>👆</span>
    content = re.sub(r'<\s*ClickMe_icon\s*>', "<span class='glassbtn' style='font-size: 1em;'>👆</span>", content, flags=re.IGNORECASE | re.DOTALL)
    #____________________________________________________________________________________________________________________________________________________________________

    # BBL-Txt - FullWidth BOTTOM, flex height - BBL-Txt

    def parse_BubbleText_params(tip_part, defaults):
        """
        Parse the second argument string and return a dict of data attributes and the cleaned tip text.
        Format: ":[T|L|BG|H|W|MH|MW|loc|tloc]tip" (or using commas)
        All parts are optional. defaults is a dict with keys: 'data-top', 'data-left', 'data-bottom-gap',
        'data-position', 'data-textalign', 'data-height', 'data-width', 'data-maxheight', 'data-maxwidth'.
        """
        params = defaults.copy()
        tip_text = tip_part
        if tip_part.startswith(':[') and ']' in tip_part:
            close_bracket = tip_part.find(']')
            param_str = tip_part[2:close_bracket]          # between ":[" and "]"
            param_str = param_str.replace(',', '|')        # support both separators
            tip_text = tip_part[close_bracket+1:].lstrip()
            parts = [p.strip() for p in param_str.split('|')]
            while len(parts) < 9:
                parts.append('')
            # Map parts to attributes (order: T, L, BG, H, W, MH, MW, loc, tloc)
            if parts[0]: params['data-top'] = parts[0]
            if parts[1]: params['data-left'] = parts[1]
            if parts[2]: params['data-bottom-gap'] = parts[2]
            if parts[3]: params['data-height'] = parts[3]
            if parts[4]: params['data-width'] = parts[4]
            if parts[5]: params['data-maxheight'] = parts[5]
            if parts[6]: params['data-maxwidth'] = parts[6]
            if parts[7]: params['data-position'] = parts[7]
            if parts[8]: params['data-textalign'] = parts[8]
        return params, tip_text

    def build_flexbot_span(match, float_dir):
        word = match.group(1).strip()
        tip_part = match.group(2)
        
        # Defaults for the popup (BubbleText) – no growing‑box CSS here, only data attributes
        defaults = {
            'data-top': '',
            'data-left': '',
            'data-bottom-gap': '0vh',
            'data-position': 'center-both',
            'data-textalign': 'left',
            'data-height': 'auto',           # fallback for max-height if no MH
            'data-width': 'auto',            # fallback for max-width if no MW
            'data-maxheight': 'var(--tt-max-height)',
            'data-maxwidth': 'var(--tt-max-width)',
        }
        params, tip_text = parse_BubbleText_params(tip_part, defaults)
        
        # Simple trigger span styles (no growing box)
        if float_dir == 'right':
            style = f'float: right; margin-right: var(--Rsafe-margin) !important;'
        elif float_dir == 'left':
            style = f'float: left; margin-left: var(--Lsafe-margin) !important;'
        elif float_dir == 'center':
            style = 'display: block; width: fit-content; margin-left: auto; margin-right: auto; text-align: center;'
        elif float_dir == 'both':
            style = f'margin-left: var(--Lsafe-margin) !important; margin-right: var(--Rsafe-margin);'
        else:
            style = 'display: inline; margin: 0;'
        
        attrs = f'style="{style}"' if style else ''
        # Store popup‑related data attributes on the trigger span
        for attr in ['data-top', 'data-left', 'data-bottom-gap', 'data-position', 'data-textalign',
                    'data-height', 'data-width', 'data-maxheight', 'data-maxwidth']:
            if attr in params and params[attr]:
                attrs += f' {attr}="{params[attr]}"'
        attrs += f' data-bbbltext="{tip_text}"'
        
        classes = 'BubbleText-trigger BubbleText-full BubbleText-flex'
        return f'<span {attrs} class="{classes}">{word}</span>'

    content = re.sub( r'<\s*BBL-Txt\s*=\s*(["\'])(.*?)\1\s*,\s*(["\'])(.*?)\3\s*>', r'__TBLEX__\2__TBLEX__\4__TBLEX__', content, flags=re.IGNORECASE | re.DOTALL )
    content = re.sub( r'__TBLEX__\s*:\s*\[floatright\]\s*(.*?)\s*__TBLEX__(.*?)__TBLEX__', lambda m: build_flexbot_span(m, 'right'), content, flags=re.IGNORECASE | re.DOTALL )
    content = re.sub( r'__TBLEX__\s*:\s*\[floatleft\]\s*(.*?)\s*__TBLEX__(.*?)__TBLEX__', lambda m: build_flexbot_span(m, 'left'), content, flags=re.IGNORECASE | re.DOTALL )
    content = re.sub( r'__TBLEX__\s*:\s*\[floatcenter\]\s*(.*?)\s*__TBLEX__(.*?)__TBLEX__', lambda m: build_flexbot_span(m, 'center'), content, flags=re.IGNORECASE | re.DOTALL )
    content = re.sub(r'__TBLEX__\s*:\s*\[floatboth\]\s*(.*?)\s*__TBLEX__(.*?)__TBLEX__', lambda m: build_flexbot_span(m, 'both'), content, flags=re.IGNORECASE | re.DOTALL)
    content = re.sub( r'__TBLEX__([^:].*?)__TBLEX__(.*?)__TBLEX__', lambda m: build_flexbot_span(m, None), content, flags=re.IGNORECASE | re.DOTALL )

    return content

# This makes sure the the propoer repalcements occur in tip_string so the tip-string bubbletext can be formed.
tip_string = pre_clean(tip_string)


def clean_content(content):
    """Clean content while perfectly preserving paragraph content, processing tables, and cleaning markdown"""
    # The clean_content function processes a block of HTML content (converted from markdown) to prepare it for final page assembly. It performs the following steps:

    # - Protects certain inline elements (<p>, <x>, <div>, <span>) by temporarily replacing them with unique placeholders (<!--PARAGRAPH_N-->). 
    #   This prevents modifications inside these tags during later steps.
    # - Converts markdown tables to HTML tables using convert_markdown_table_to_html.
    # - Removes markdown headings (lines containing ##) as they are not needed in the final output.
    # - Restores the protected elements (paragraphs, divs, spans) back to their original state.
    # - Normalizes line breaks between paragraphs: multiple consecutive newlines are replaced with a single <br><br> (two line breaks), while preserving the content inside <p> tags.
    # - Replaces _getMdate("filename") patterns with the actual modification date of the referenced file (using rep_mdate).
    # - Returns a tuple (None, processed_content). The first element (title) is always None because font‑tag extraction was removed (titles are now handled via <TITLE=...> in pre_clean).
    # - The result is clean, well‑formatted HTML ready to be inserted into a page.

    protected_paragraphs = []
    
    def protect_paragraphs(match):
        """Callback to store original paragraphs exactly as they are"""
        protected_paragraphs.append(match.group(0))
        return f"<!--PARAGRAPH_{len(protected_paragraphs)-1}-->"

    # This regular expression substitution finds all occurrences of the following HTML elements (with any attributes) and 
    # their entire content (including nested tags, due to the .*? non‑greedy quantifier and re.DOTALL flag which makes . match newlines):
    # <p ...>...</p>     <x ...>...</x>     <div ...>...</div>     <span ...>...</span>
    # For each match, it calls the protect_paragraphs function, which stores the original matched string in a list (protected_paragraphs) 
    # and returns a unique placeholder like <!--PARAGRAPH_0-->. This placeholder temporarily replaces the original HTML, so that later 
    # processing steps (like line break handling) do not alter the content inside these tags. After other clean‑up operations, the
    # placeholders are replaced back with the original tags. This protects the integrity of these elements during cleaning.
    content = re.sub( r'(<p\b[^>]*>.*?</p>|<x\b[^>]*>.*?</x>|<div\b[^>]*>.*?</div>|<span\b[^>]*>.*?</span>)', protect_paragraphs, content, flags=re.DOTALL )

    # 5. TABLE PROCESSING (Original Logic)
    def process_table(match):
        """Convert markdown tables to HTML tables"""
        return convert_markdown_table_to_html(match.group(0))

    # Find and convert markdown tables (format: | Header | ... |)
    content = re.sub( r'(\n\|[^\n]+\|\n\|[-:|]+\|[\s\S]*?)(?=\n\n|\Z)',  # Table pattern 
        process_table, content )

    # Remove markdown headings (lines containing ##)
    content = re.sub(r'^.*##.*$', '', content, flags=re.MULTILINE)

    # 7. RESTORE PROTECTED PARAGRAPHS (Exactly As They Were)
    for i, para in enumerate(protected_paragraphs):
        content = content.replace(f"<!--PARAGRAPH_{i}-->", para)

    # This code splits the HTML content into pieces, separating complete <p>...</p> elements from everything else. It then 
    # processes the non‑paragraph parts (text outside <p> tags) by replacing sequences of two or more newlines with a single 
    # <br><br>, effectively converting blank lines into line breaks. Paragraphs themselves are left untouched. Finally, it 
    # reassembles the pieces into a single string, ensuring that line breaks are normalized only outside of paragraph tags. 
    # This preserves the structure of existing paragraphs while improving the layout of plain text.

    parts = re.split(r'(<p\b[^>]*>.*?</p>)', content, flags=re.DOTALL)
    processed_parts = []
    
    for part in parts:
        if not part.startswith('<p') or not part.endswith('</p>'):
            # Only process non-paragraph parts
            # Split into paragraphs (separated by 2+ newlines)
            paragraphs = re.split(r'\n{2,}', part.strip())
            # Join with exactly one <br><br> between paragraphs
            processed_part = '<br><br>'.join(p.strip() for p in paragraphs if p.strip())
            processed_parts.append(processed_part)
        else:
            # Leave paragraphs exactly as they are
            processed_parts.append(part)
    
    # Combine all parts
    processed_content = ''.join(processed_parts)

    # 9. REPLACE _getMdate PATTERNS WITH ACTUAL DATES
    processed_content = rep_mdate(processed_content)

    # No title extracted from font tags – always return None for title
    return processed_content.strip()

def collapse_consequtive_blank_lines(html):
    # remove multiple <br>'s or newlines.
    # Normalize line endings first
    # Pattern: closing </div> followed by any whitespace (including newlines) and then two or more <br> tags or three+ newlines
    # Replace with </div> + a single newline + a single <br> (or just two newlines)
    html = html.replace('\r\n', '\n')
    
    # Case 1: Two or more <br> tags after the div
    html = re.sub(r'(</div>)\s*(<br\s*/?>\s*){2,}', r'\1<br>', html, flags=re.IGNORECASE)
    
    # Case 2: Three or more newlines (i.e., two or more blank lines) after the div
    html = re.sub(r'(</div>)\s*\n{3,}', r'\1\n\n', html)
    
    return html

def process_markdown(content):
    # The process_markdown function is the core routine that converts the markdown content (after pre‑processing) 
    # into a list of HTML page strings. It does the following:
    #   - Calls pre_clean(content) – applies a series of regex substitutions to convert custom tags (e.g., <CHAPTER=...>, 
    #       <IMAGE=...>, <ParaitalicL=...>) into standard HTML or intermediate markers.
    #   - Removes everything before the first page break using remove_before_page_break_flexible(content) – ensures the 
    #       content starts at the first <div style="break-after: page;"></div>.
    #   - Optionally generates a TOC page (if TOC_ENABLE is True) by calling generate_toc(content).
    #   - Splits the content at each page‑break div using re.split(r'(?=<div style="break-after: page;"></div>)', content).
    #   - Filters out empty sections (whitespace‑only).
    #   - For each section (page), it:
    #       - Removes the page‑break div itself.
    #       - Converts inline image syntax (![[...]]) with convert_inline_images.
    #       - Cleans the content (removes markdown headings, normalises line breaks, etc.) with clean_content.
    #       - Builds the final page HTML using build_page_html (passing None for image, description, and title).
    #   - Inserts the TOC page at the configured position (TOC_POSITION).
    #   - Returns the list of page HTML strings.
    # This function essentially orchestrates the entire transformation from pre‑processed markdown to a 
    # collection of ready‑to‑assemble pages.

    """ REPLACE HTML TAGS WITH KEYWORDS"""
    content = pre_clean(content)

    """Process markdown content and return list of page HTMLs. Uses <div style="break-after: page;"></div> as page separator."""
    pages = []

    # remove everything before 1st page break
    content = remove_before_first_page_break(content)

    # Generate TOC if enabled
    toc_html = generate_toc(content) if CONFIG['TOC_ENABLE'] else None
    
    try:
        # Split the entire content by the page break div
        page_sections = re.split(r'(?=<div style="break-after: page;"></div>)', content)
        
        # Filter out any empty sections
        page_sections = [section.strip() for section in page_sections if section.strip()]

        # Process each section as a separate page
        for counter, section_content in enumerate(page_sections, 1):
            # Remove the page break div from the start of the content, if it exists
            cleaned_section = re.sub(r'^<div style="break-after: page;"></div>', '', section_content)
            
            # Convert inline images to HTML while preserving their position
            processed_content = convert_inline_images(cleaned_section)            
            cleaned_content = clean_content(processed_content)
            
            # Pass None for image_filename and description to avoid main image container
            page_html = build_page_html(counter, None, None, cleaned_content)            
            if page_html:
                pages.append(page_html)
                
        # Insert TOC at configured position
        if toc_html:
            insert_pos = min(CONFIG['TOC_POSITION'], len(pages))
            pages.insert(insert_pos, toc_html)
            
    except Exception as e:
        logging.error(f"Markdown processing failed: {str(e)}")
        raise
        
    return pages

def remove_before_first_page_break(input_string):
    # The remove_before_first_page_break function strips away everything in a string that appears before 
    # the first occurrence of a page‑break <div> (i.e., <div style="break-after: page;"></div>). It uses a 
    # flexible regular expression to match the div regardless of whitespace or case. If the pattern is found, 
    # it returns the substring starting at that div (including the div itself). If no page break is found, 
    # it returns the original string unchanged. This is used to discard any content (like a header or title) 
    # that might appear before the first explicit page break in the markdown source, ensuring that the book’s 
    # content starts at the first page break. i.e Returns str: The string content starting from the page break div

    # Pattern that matches the div with possible whitespace variations
    pattern = re.compile(r'<div\s+style\s*=\s*["\']break-after:\s*page;["\']\s*>\s*</div>', re.IGNORECASE)
    
    # Search for the pattern in the string
    match = pattern.search(input_string)
    
    if match:
        # Return everything from the start of the match onward
        return input_string[match.start():]
    
    # If the target string is not found, return the original string
    # or empty string depending on your preference
    return input_string  # or return "" if you want empty when not found

#   CLEAN_UP END ===================================================================================================

#   CONVERTIONS FUNCTIONS START ====================================================================================
def convert_markdown_table_to_html(markdown_table):
    """Convert markdown table to HTML with proper URL handling"""
    def convert_urls(text):
        """Convert URLs in text without escaping HTML"""
        # Convert [text](url)
        text = re.sub(
            r'\[([^\]]+)\]\(([^)]+)\)',
            #r'<a href="\2" target="_blank">\1</a>',
            r'<a href="\2">\1</a>',
            text
        )
        # Convert (url)
        text = re.sub(
            r'\(((https?://[^\s)]+))\)',
            #r'<a href="\1" target="_blank">\1</a>',
            r'<a href="\1">\1</a>',
            text
        )
        # Convert plain URLs
        text = re.sub(
            r'(?<!["\'])(https?://[^\s<>]+)(?!["\'])',
            #r'<a href="\1" target="_blank">\1</a>',
            r'<a href="\1">\1</a>',
            text
        )
        return text

    lines = [line.strip() for line in markdown_table.split('\n') if line.strip()]
    
    if len(lines) < 2 or not all(line.startswith('|') for line in lines):
        return escape(markdown_table)  # Not a valid table
    
    # Process header
    headers = [convert_urls(cell.strip()) for cell in lines[0].split('|')[1:-1]]
    header_html = f'<thead><tr>{"".join(f"<th>{h}</th>" for h in headers)}</tr></thead>'
    
    # Process body rows
    body_rows = []
    for line in lines[2:]:
        cells = []
        for cell in line.split('|')[1:-1]:
            cell_content = cell.strip()
            # Convert URLs but don't escape the resulting HTML
            cell_content = convert_urls(cell_content)
            cells.append(cell_content)
        body_rows.append(f'<tr>{"".join(f"<td>{c}</td>" for c in cells)}</tr>')
    
    return f'<div class="table-container"><table>{header_html}<tbody>{"".join(body_rows)}</tbody></table></div>'


def convert_inline_images(content):
    """Fixed parser that handles alignment correctly with px and % size support"""
    # The convert_inline_images function transforms custom image syntax ![[ ... ]] into HTML that displays an 
    # image with an optional caption popup. It parses the pipe‑separated fields inside the brackets:
    #   - Filename (required) – path to the image.
    #   - Description (optional) – text shown in a popup when hovering over the image.
    #   - Size specification (optional) – can be a percentage (e.g., 50%), pixel value (e.g., 300px or 300), 
    #       or dimensions like 400x300.
    #   - Alignment (optional) – left, right, or center; defaults to left.
    # It generates a <div class="image-container"> with an alignment class (e.g., image-align-left). 
    # Inside, it places an <img> tag (with inline width/height from the size spec) and, if a description exists, 
    # a <div class="image-caption-popup"> containing that description. The resulting HTML is ready to be embedded 
    # in a page. This parser is used during markdown processing to handle inline images with advanced options.
    
    def replace_image(match):
        image_match = match.group(0)
        
        # Extract everything between [[ and ]]
        inner_match = re.search(r'!\[\[(.*?)\]\]', image_match)
        if not inner_match:
            return image_match
            
        # Split by pipe and clean up parts
        parts = [part.strip() for part in inner_match.group(1).split('|')]
        image_filename = parts[0]
        
        # Get parameters by position
        description = parts[1] if len(parts) > 1 else ""
        size_spec = parts[2] if len(parts) > 2 and parts[2] != "" else CONFIG['ImageWidthDesktop']
        alignment = parts[3] if len(parts) > 3 else ""

        # Clean and validate alignment
        alignment = alignment.strip().lower() if alignment else ""
        if alignment not in ['center', 'left', 'right']:
            alignment = "left"  # Default to left if not specified
        
        # Add mobile alignment class
        alignment_class = f" image-align-{alignment} mobile-align-center mobile-default-size"
        
        # NEW: Calculate width for caption based on size_spec
        caption_width_style = ""
        # Size handling with support for px, %, and plain numbers
        style_attr = ""

        if size_spec:
            size_spec = size_spec.strip()

            # Handle percentage values (e.g., "50%")
            #if size_spec.endswith('%'):
            #    caption_width_style = f' style="width: {size_spec}; max-width: {size_spec};"'
            if size_spec.endswith('%'):
                style_attr = f' style="width: {size_spec};"'
                caption_width_style = f' style="width: {size_spec}; "'
            
            # Handle pixel values (e.g., "300px" or "300")
            elif size_spec.endswith('px') or size_spec.isdigit():
                width_value = size_spec if size_spec.endswith('px') else f"{size_spec}px"
                style_attr = f' style="width: {width_value};"'
                caption_width_style = f' style="width: {width_value};"'
            
            # Handle dimensions like 400x300
            elif 'x' in size_spec:
                try:
                    width, height = size_spec.split('x')
                    # Add px if not specified for width
                    if not width.endswith('px') and not width.endswith('%'):
                        width = f"{width}px"
                    # Add px if not specified for height
                    if not height.endswith('px') and not height.endswith('%'):
                        height = f"{height}px"
                        
                    style_attr = f' style="width: {width}; height: {height};"'
                    caption_width_style = f' style="width: {width}; "'
                except ValueError:
                    # Fallback if dimension parsing fails
                    style_attr = f' style="width: {size_spec};"'
                    caption_width_style = f' style="width: {size_spec}; "'

        # Create HTML with inline width styling for caption
        image_html = f'<img src="{escape(image_filename)}" alt="Image"{style_attr}>'
        
        # NEW: Apply the calculated width to the caption
        caption_html = f'<div class="image-caption-popup"{caption_width_style}>{escape(description)}</div>' if description else ''
        
        return f'<div class="image-container{alignment_class}">{image_html}{caption_html}</div>'
    
    return re.sub(r'!\[\[.*?\]\]', replace_image, content)

#   CONVERTIONS FUNCTIONS END ======================================================================================

#   Get PAGE NUM START =============================================================================================
def page_num_toc(main_string, substring_to_count, search_text):
    # The page_num_toc function determines the page number (0‑based index) where a specific heading 
    # (e.g., ## Introduction) appears in the markdown content. It does this by:
    #   - Counting how many page‑break divs (<div style="break-after: page;"></div>) occur before the heading.
    #   - If the heading is not found, it returns the total number of page breaks in the entire content (which 
    #       corresponds to the last page index).
    #The function ignores its second parameter (substring_to_count) and always uses a fixed pattern to match 
    # page breaks. The result is used in generate_toc to create links that jump to the correct page 
    # when a TOC entry is clicked.
    #Returns:        int: The number of times the page break div was found before the heading.
    # We ignore the passed-in 'substring_to_count' and instead count page breaks 

    page_break_pattern = r'<div style="break-after: page;"></div>'
    
    search_text_index = main_string.find(search_text)

    if search_text_index == -1:
        # If the search text is not found, count all page breaks in the string
        return len(re.findall(page_break_pattern, main_string))
    else:
        # If the search text is found, count page breaks in the sliced string (content before the heading)
        content_before_heading = main_string[:search_text_index]
        return len(re.findall(page_break_pattern, content_before_heading))
    
#   Get PAGE NUM START =============================================================================================


#   BUILD PAGES START =============================================================================================
def generate_toc(content):
    """Generate table of contents with book title header"""
    # The generate_toc function creates the HTML for the Table of Contents page. It scans the markdown c
    # ontent for headings (##, ###, etc.), skips level‑1 headings (#), and for each heading it calculates 
    # the page number (using page_num_toc which counts page breaks before the heading). Based on the 
    # configuration flag TOCasList, it builds either a vertical list (.toc-entry) or a horizontal button 
    # bar (.compact-button). It also adds an optional “AboutMe” button (if BkListLink_show is true) and 
    # appends a tip_string (navigation tips) separated by a horizontal rule. The resulting HTML is wrapped 
    # in a .page container with id page-toc and a .page-content wrapper for consistent scrolling. This 
    # function is called only if TOC_ENABLE is true.

    toc_entries = []
    
    headings = re.findall(r'^(#+)\s+(.+)$', content, re.MULTILINE)

    # This code loops through all markdown headings found in the content (e.g., ## Title). Each heading is represented 
    # by a tuple (level, title), where level is the string of hash symbols (e.g., '#', '##', '###') and title is the 
    # heading text. The condition if level == '#': continue skips any heading that is a level‑1 heading (single #). 
    # This ensures that the TOC (Table of Contents) only includes H2 and deeper headings, ignoring the main document 
    # title (which is typically an H1).    

    for level, title in headings:
        if level == '#':  # Skip H1
            continue
            
        indent = (len(level) - 2) * 20

        # This code calculates the page number where a given markdown heading (## title) appears, and constructs a 
        # URL fragment (e.g., #page-3) to link to that page in the Table of Contents.
        #   - page_num_toc(content, 'dummy_string', '## '+title) scans the content to count how many page‑break 
        #       divs (<div style="break-after: page;"></div>) occur before the heading. This number is the page 
        #       index (0‑based) where that heading starts.
        #   - The resulting page_num is then used to create the href attribute: #page-{page_num}. This fragment 
        #       matches the id of the corresponding page element (e.g., <div id="page-3">), allowing the TOC 
        #       link to jump directly to that page when clicked.
        # The dummy_string argument is ignored because page_num_toc uses a fixed pattern for page breaks, not 
        #       the substring parameter. This function effectively maps headings to their page numbers for navigation.

        # The variable title in the loop contains the text of the markdown heading (excluding the leading # symbols). For example:
        #   - ## Introduction → title = "Introduction"
        #   - ### Detailed Analysis → title = "Detailed Analysis"
        #   - Main Title → title = "Main Title" (but this is skipped because level == '#')
        # It is then used to build the Table of Contents entry: the heading text appears as the link label, and it is 
        # also passed to page_num_toc to find the corresponding page number.

        page_num = page_num_toc(content, 'dummy_string', '## '+title)
        href = f'#page-{page_num}'

        # sets up the button or the list with the associated Href's
        if CONFIG['TOCasList']:
            # List style TOC
            toc_entries.append(
                f'<div class="toc-entry" style="margin-left: {indent}px;">'
                f'<a href="{href}" class="toc-link" style="display: flex; justify-content: space-between;">'
                f'<span>{title.strip()}</span>'
                f'<span>{page_num}</span>'
                f'</a>'
                f'</div>'
            )
        else:
            # Button style TOC - Horizontal layout with CSS gap
            toc_entries.append(
                f'<a href="{href}" class="glassbtn compact-button toc-link">'
                f'{title.strip() + "(" + f"{page_num}" + ")"}'
                f'</a>'
            )
    
    if not toc_entries:
        return None
    
    # Build the back‑to‑list button (if enabled)
    back_to_list_html = ''
    if CONFIG['TOC_ENABLE'] and CONFIG['BkListLink_show']:
        url = CONFIG['BkLinkURL']
        if not url.startswith(('http://', 'https://')):
            url = f'https://{url}'
        back_to_list_html = f'''
        <div class="toc-header-left">
            <a href="{url}" target="_self" class="glassbtn compact-button">
                📚
            </a>
        </div>
        '''
    
    book_title = f'<div class="book-title">{CONFIG["BkPage0_Title"]}</div>'
    
    # Determine container class based on TOC style
    container_class = "toc-list" if CONFIG['TOCasList'] else "toc-buttons"

    # This code returns the HTML for the Table of Contents page. It constructs a <div class="page" id="page-toc"> that contains:
    #   - A .page-content wrapper (for consistent scrolling and styling).
    #   - A {book_title} (usually the book title, placed inside the page content).
    #   - A .toc-container whose class depends on container_class (e.g., toc-list or toc-buttons), which controls the TOC layout.
    #   - An <h2> displaying the TOC title from the configuration (CONFIG["TOC_TITLE"]).
    #   - An optional {back_to_list_html} (e.g., an "AboutMe" button) if enabled.
    #   - A <div class="toc-button-container"> containing all the TOC entries (the toc_entries list joined into a single string).
    #   - A horizontal rule (<hr>) with a thin, semi‑transparent line.
    #   - A {tip_string} that typically contains navigation tips (e.g., how to use the book).
    #   The entire block is wrapped in the .page-content to ensure it scrolls properly and maintains the same glass‑panel 
    # appearance as other pages. This function is called by generate_toc() when TOC_ENABLE is true, and the resulting HTML 
    # is inserted into the list of pages.

    return f"""
    <div class="page" id="page-toc">
        <div class="page-content">
            <div class="toc-header-row">
                {back_to_list_html}
                <div class="book-title">{CONFIG["BkPage0_Title"]}</div>
            </div>
            <div class="toc-container {container_class}" style="margin-top: 20px;">
                <h2>{CONFIG["TOC_TITLE"]}</h2>
                <div class="toc-button-container">
                    {"".join(toc_entries)}
                </div>
            </div>
            <hr style="height: 1.2px; background-color: var(--text-color); opacity: 0.3; border: none;"><br>
            {tip_string}
        </div>       
    </div>
    """


def build_page_html(counter, image_filename, description, content):
    """Build HTML for a single page with image description (BubbleText and pop-up)"""
    # The build_page_html function generates the HTML for a single content page (or the TOC page) of the book. 
    # It takes five parameters:

    #   - counter – the page number (1‑based for content pages, or "toc" for the Table of Contents page).
    #   - image_filename – optional path to an image that will appear on the page.
    #   - description – optional text for a pop‑up caption that appears when hovering over the image.
    #   - title – an optional title extracted from the markdown (now always None, since font‑tag titles are no longer used).
    #   - content – the main HTML content of the page.
    # What it does:
    #   - Determines the page id – e.g., page-1, page-2, or page-toc.
    #   - Sets an empty book_title – because the book title is now placed in the .page-header by JavaScript.
    #   - Creates a title_part – if a title is provided, it wraps it in a highlighted <span>; otherwise empty.
    #   - Builds image and caption HTML – if image_filename is provided, it creates an <img> tag and, if a description exists, 
    #       a .image-caption-popup div.
    #   - Wraps the content in a .content-text div with responsive font‑size variables.
    #   - Assembles the final page – depending on whether an image exists, it uses either an .image-container 
    #       (with left/right alignment based on counter % 2) or a .text-only-container. Both containers are placed inside 
    #       a .page-content div, which itself is inside the .page wrapper.
    # The returned HTML is a complete .page element ready to be added to the list of pages. This function is called for each markdown section (page) after conversion.

    """Build HTML for a single page with image description (BubbleText and pop-up)"""
    page_id = f"page-{counter}" if counter != "toc" else "page-toc"
    
    # Book title for non-cover pages (now handled by .page-header in JavaScript)
    book_title = ''
    
    # Title part is no longer used (titles are now in .page-header)
    title_part = ''
    
    # Image with BubbleText AND pop-up caption
    image_html = ''
    caption_popup = ''
    
    if image_filename:
        image_html = f'<img src="{escape(image_filename)}" alt="Image {counter}">'
        if description:
            caption_popup = f'''
            <div class="image-caption-popup">
                {escape(description)}
            </div>
            '''
    
    # Content with mobile-responsive sizing
    styled_content = f'''
    <div class="content-text" 
         style="font-size: {CONFIG["BkFontSize"]};
                --mobile-font-size: {CONFIG["BkFontSizeMobile390"]}">
        {content}
    </div>
    '''
    
    # Page assembly
    if image_filename:
        position = 'right' if counter % 2 else 'left'
        return f"""
        <div class="page" id="{page_id}">
            <div class="page-content">
                {book_title}
                <div class="image-container {position}">
                    {image_html}
                    {caption_popup}
                    {title_part}
                    {styled_content}
                </div>
            </div>
        </div>
        """
    else:
        return f"""
        <div class="page" id="{page_id}">
            <div class="page-content">
                {book_title}
                <div class="text-only-container">
                    {title_part}
                    {styled_content}
                </div>
            </div>
        </div>
        """

def build_final_html(pages):
    # The build_final_html(pages) function assembles the complete HTML document from 
    # the list of individual page HTML strings. It performs the following steps:
    #   - Calculates the total number of pages – total_pages = len(pages) + (0 if CONFIG['Page0_skip'] else 1). 
    #       This accounts for the title page (which is not in the pages list) when it exists.
        #   - Builds the title page HTML (if Page0_skip is False) – creates a <div class="page active" id="page-0"> 
        #       containing the book title, tag, author name, last update date, and the tip_string. 
        #       This page is not part of the pages list.
        #   - Prepares mobile‑specific CSS – based on the ResizeForMobile flag, it generates either 
        #       a forced mobile‑sizing block or a fallback rule.
        #   - Prepares a dictionary of template variables (template_vars) – these include fonts, 
        #       colors, image widths, page numbers visibility, and the title page HTML, etc. These 
        #       will be inserted into the HTML_TEMPLATE string.
        #   - Formats the main HTML template – html_template = HTML_TEMPLATE.format(**template_vars) 
        #       replaces all placeholders (e.g., {BkFontColor}, {title_page_html}) with actual values.
        #   - Prepares the footer – replaces placeholders in FOOTER_TEMPLATE such as SLIDER_MAX, TOTALPAGES, 
        #       INITIAL_PAGE, ARW_HOVER_WIDTH, etc., with their final values (e.g., slider max = total_pages‑1, 
        #       initial page = 0). Also sets arrow display properties.
        #   - Combines everything – returns html_template + '\n'.join(pages) + footer, i.e., the header/template, 
        #       then all page HTML strings (title page already included in html_template), then the footer 
        #       (which contains the slider, arrows, and JavaScript).
    # The result is a complete, standalone HTML document that can be written to a file. This function is 
    # called after all pages have been generated.

    """Assemble the final HTML document with responsive font scaling"""
    total_pages = len(pages) + (0 if CONFIG['Page0_skip'] else 1)

    #Build Title page
    title_page_html = ''
    if not CONFIG['Page0_skip']:
        title_page_html = f"""
        <div class="page active" id="page-0">
            <div class="page-content">
                <div class="heading-container">
                    <h1>{escape(CONFIG['BkPage0_Title'])}</h1> 
                    <h2>{escape(CONFIG['BkPage0_Tag'])}</h2> 
                    <h2>{escape(CONFIG['Author_name'])}</h2> 
                    <p style="font-size: 0.9em; text-align: center; opacity: 0.8;">
                        Writing Period: {get_mdate(CONFIG['source_md'])}
                    </p>
                    <h3>{escape(CONFIG['BkPage0_head3'])}</h3>
                </div>
                {tip_string}
            </div>
        </div>
    """

    # Prepare mobile CSS based on flag (default to False if not specified)
    # This code prepares mobile‑specific CSS rules for images and captions 
    # based on the ResizeForMobile flag. If enabled, it forces images to a fixed 
    # mobile width (ImageWidthMobile), centers them, disables floating, and also 
    # centers caption popups. If disabled, it simply limits image and caption width 
    # to the page width. It ensures proper display on small screens.
    force_mobile = CONFIG.get('ResizeForMobile', False)
    force_mobile_css = ""
    
    if force_mobile:
        force_mobile_css = f"""
        /* FORCE SIZE FORCE TO ImageWidthMobile */
        .mobile-default-size img {{
            width:  {CONFIG['ImageWidthMobile']} !important;
            max-width:  {CONFIG['ImageWidthMobile']} !important;
            margin-top: 20px !important;
            margin-bottom: 40px !important;
            margin-left: 0px !important;
            margin-right: 0px !important;            
            left: 50% !important;
            transform: translateX(-50%) !important;     
            height: auto !important;
            float: none !important;
            display: block !important;
        }}

        /* FORCE ALL CAPTION POPUPS to be CENTERED on mobile */
        .image-align-left .image-caption-popup,
        .image-align-right .image-caption-popup,
        .image-align-center .image-caption-popup {{
            width:  {CONFIG['ImageWidthMobile']} !important;
            max-width:  {CONFIG['ImageWidthMobile']} !important;
            top: 20px;
            left: 50% !important; /* Center horizontally */
            transform: translateX(-50%) translateY(-20px) scale(0.95) !important; /* COMBINE transforms */
            padding: 0px 10px 0px 10px ! important;
        }}
        """
    else:
        force_mobile_css = f"""
        .image-container img {{
            max-width: var(--page-width) !important;
        }}
        .image-caption-popup {{
            max-width: var(--page-width) !important;
        }}
        """

    # Prepare all template variables
    template_vars = {
        'title_page_html': title_page_html,
        'BkFontColor': CONFIG['BkFontColor'],
        'BkPage0_FontColor': CONFIG['BkPage0_FontColor'],
        'BkImage': CONFIG['BkImage'],
        'BkFontSize': CONFIG['BkFontSize'],
        'BkFontSizeMobile390': CONFIG['BkFontSizeMobile390'],
        'ARW_HOVER_WIDTH': CONFIG['ARW_HOVER_WIDTH'],
        'ARW_VISIBLE_WIDTH': CONFIG['ARW_VISIBLE_WIDTH'],
        'ImageWidthDesktop': CONFIG['ImageWidthDesktop'],
        'TitleFontClr': CONFIG['TitleFontClr'],
        'ImageWidthMobile': CONFIG['ImageWidthMobile'],
        'BkPage0_Title': escape(CONFIG['BkPage0_Title']),
        'BkPage0_Description': escape(CONFIG['BkPage0_Description']),
        'BkPage0_Keywords': escape(CONFIG['BkPage0_Keywords']),
        'BkPage0_Tag': escape(CONFIG['BkPage0_Tag']),
        'Author_name': escape(CONFIG['Author_name']),
        'BkPage0_head3': escape(CONFIG['BkPage0_head3']),
        'TOC_FontColor': CONFIG.get('TOC_FontColor', '#ffffff'),
        'pageNumberStyle': "hidden" if CONFIG.get('Hide_page_number', False) else "visible",
        'ForceMobileCSS': force_mobile_css  # Add this new variable
    }
    
    # Format main template with mobile CSS included
    html_template = HTML_TEMPLATE.format(**template_vars)

    # Prepare footer with dynamic values
    footer = FOOTER_TEMPLATE\
        .replace('SLIDER_MAX', str(total_pages - 1))\
        .replace('TOTALPAGES', str(total_pages))\
        .replace('INITIAL_PAGE', '0')\
        .replace('SLIDER_DISPLAY', '' if CONFIG['SLDR_DISPLAY'] else 'display: none !important;')\
        .replace('{BkPage0_Title}', escape(CONFIG['BkPage0_Title']))\
        .replace('{ARW_HOVER_WIDTH}', str(CONFIG['ARW_HOVER_WIDTH']))\
        .replace('{ARW_DISPLAY}', 'true' if CONFIG['ARW_DISPLAY'] else 'false')\
        .replace('{Page0_skip}', 'true' if CONFIG['Page0_skip'] else 'false')\
        .replace('{BkLinkURL}', escape(CONFIG['BkLinkURL']))

    # Set arrow display properties
    arrow_display = {
        'ARW_DISPLAY': 'flex',
        'ARW_VISIBILITY': 'visible' if CONFIG['ARW_DISPLAY'] else 'hidden',
        'ARW_OPACITY': '0',
        'ARW_HOVER_OPACITY': '1' if CONFIG['ARW_DISPLAY'] else '0'
    }
    
    for key, value in arrow_display.items():
        html_template = html_template.replace(key, value)
    
    return html_template + '\n'.join(pages) + footer
#   BUILD PAGES END ==================================================================================================


#   DATE FUNCTIONS START =============================================================================================
def get_mdate(md_file_path):
    # The get_mdate function returns a string containing:
    #   - The modification date of the oldest image file (.jpg, .jpeg, .png, .svg) 
    #       found in the same directory as the markdown file, followed by a hyphen and
    #   - The modification date of the markdown file itself.
    # Both dates are formatted as '%b %d, %Y' (e.g., "Jan 15, 2020 - Apr 22, 2026"). 
    # If no images are found, it returns "No images - <md_date>". If the markdown 
    # file is missing, the second part becomes "Unknown date". This function is used 
    # by rep_mdate to replace _getMdate("filename") placeholders with the actual 
    # writing period (oldest image to latest markdown edit).
    """
    Return a string: oldest image date in the markdown's directory - markdown file date.
    Both dates formatted as '%b %d, %Y'.
    md_file_path should be an absolute Path object.
    """
    md_path = Path(md_file_path)
    # 1. Modification date of the markdown file
    if md_path.exists():
        md_mod_time = datetime.fromtimestamp(md_path.stat().st_mtime)
        md_date_str = md_mod_time.strftime('%b %d, %Y')
    else:
        md_date_str = "Unknown date"

    # 2. Find oldest image in the same directory as the markdown file
    img_extensions = ('.jpg', '.jpeg', '.png', '.svg')
    img_files = []
    if md_path.parent.exists():
        for ext in img_extensions:
            # case‑insensitive glob: use lower/upper or just glob with wildcard and filter
            img_files.extend(md_path.parent.glob(f'*{ext}'))
            img_files.extend(md_path.parent.glob(f'*{ext.upper()}'))
        # Remove duplicates
        img_files = list(set(img_files))
        if img_files:
            oldest_mtime = min(f.stat().st_mtime for f in img_files)
            oldest_image_date = datetime.fromtimestamp(oldest_mtime)
            oldest_image_date_str = oldest_image_date.strftime('%b %d, %Y')
        else:
            oldest_image_date_str = "No images"
    else:
        oldest_image_date_str = "No images"

    return f"{oldest_image_date_str} - {md_date_str}"

def rep_mdate(content):
    # The rep_mdate function scans the content for patterns like _getMdate("filename") and replaces each occurrence 
    # with an HTML <span> that displays the modification date of the referenced file 
    # (formatted as '%b %d, %Y', e.g., "Apr 22, 2026"). The date is retrieved by calling get_mdate(filename), 
    # which obtains the last modified timestamp of the file (relative to the script’s directory). The resulting span 
    # uses the configured BkFontColor and a reduced opacity for a subtle appearance. This function is typically 
    # called inside clean_content to dynamically insert file dates into the final HTML.

    """Replace _getMdate("filename") patterns with actual modification dates"""
    def replace_mdate(match):
        filename = match.group(1)   # not used anymore
        # Use the resolved absolute path of the source markdown
        md_abs_path = CONFIG.get('_resolved_source_md', None)
        if md_abs_path and Path(md_abs_path).exists():
            date_value = get_mdate(md_abs_path)
        else:
            date_value = "Unknown date"
        return f'<span style="font-size: 0.8em; color: {CONFIG["BkFontColor"]}; opacity: 0.65;">{date_value}</span>'
    
    pattern = r'_getMdate\("([^"]+)"\)'
    return re.sub(pattern, replace_mdate, content, flags=re.IGNORECASE)
#   DATE FUNCTIONS END== =============================================================================================


def main():
    # The main() function is the entry point of the script. It:
    #   - Parses command‑line arguments – expects a single argument: the path to a JSON configuration file.
    #   - Loads the configuration using load_config(args.config_file) and stores it in the global CONFIG variable.
    #   - Validates the configuration with validate_config().
    #   - Resolves file paths – combines source_path with source_md, output_md, output_html and converts them to 
    #       absolute paths relative to the script’s location.
    #   - Copies the source markdown file to the output .mdx file if COPY_ENABLE is True.
    #   - Reads the source markdown file (source_md).
    #   - Processes the markdown content by calling process_markdown(content), which returns a list of page HTML strings.
    #   - Builds the final HTML by passing the page list to build_final_html(pages).
    #   - Removes extra blank lines with collapse_consequtive_blank_lines(final_html).
    #   - Writes the final HTML to the output file (output_html).
    #   - Logs success or catches and logs any exception, then exits with an error code if needed.
    # In essence, main() orchestrates the entire conversion from markdown to a complete, styled HTML document.
    
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Process markdown to HTML with configurable settings')
    parser.add_argument('config_file', 
                       help='Path to configuration JSON file (including filename)')
    
    args = parser.parse_args()
    
    # Load configuration
    global CONFIG
    CONFIG = load_config(args.config_file)

    validate_config()
    
    try:
        # Resolve all paths relative to script directory
        script_dir = Path(__file__).parent

        # Use proper path joining instead of string concatenation
        CONFIG['source_md'] = str(Path(CONFIG['source_path']) / CONFIG['source_md'])
        CONFIG['output_md'] = str(Path(CONFIG['source_path']) / CONFIG['output_md'])
        CONFIG['output_html'] = str(Path(CONFIG['source_path']) / CONFIG['output_html'])

        source_md = resolve_relative_path(CONFIG['source_md'], script_dir)
        CONFIG['_resolved_source_md'] = str(source_md)
        output_md = resolve_relative_path(CONFIG['output_md'], script_dir)
        output_html = resolve_relative_path(CONFIG['output_html'], script_dir)
        
        if not source_md.exists():
            raise FileNotFoundError(f"Input file not found: {source_md}")
            
        # Copy the markdown file if enabled
        if CONFIG['COPY_ENABLE']:
            output_md.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_md, output_md)
            logging.info(f"Copied {source_md} to {output_md}")
        
        # Process content
        content = source_md.read_text(encoding='utf-8')
        pages = process_markdown(content)   
        
        # Generate HTML
        final_html = build_final_html(pages)

        # Remove extra blank lines
        final_html = collapse_consequtive_blank_lines(final_html)

        output_html.write_text(final_html, encoding='utf-8')
        logging.info(f"Created {output_html} with {len(pages)} pages")
        
    except Exception as e:
        logging.error(f"Conversion failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
    