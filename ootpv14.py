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
                    'BkFontColor', 'BkFontSize', 'BkFontSizeMobile390', 'TitleFontSize', 'BkPage0_FontColor', 
                    'BkPage0_Title', 'BkPage0_Description', 'BkPage0_Tag','BkPage0_Keywords', 'BkPage0_head3',
                    'BkListLink_show', 'BkLinkURL', 
                    'ImageWidthDesktop', 'ImageWidthMobile', 'Page0_skip',
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

# HTML Template with all requested changes
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
            --glass-border: rgba(255, 255, 255, 0.1);
            --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            --text-color: {BkFontColor};
            --arrow-block-display: ARW_DISPLAY;
            --arrow-visibility: ARW_VISIBILITY;
            --arrow-opacity: ARW_OPACITY;
            --arrow-hover-opacity: ARW_HOVER_OPACITY;
            --arrow-hover-width: {ARW_HOVER_WIDTH}%;
            --page-width: 94vw;
            --page-height: 94vh;
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
            color: #4fc3f7 !important; /* Bright blue - adjust hue as needed */
            text-decoration: none;
            font-weight: 500;
            transition: all 0.2s ease;
            padding: 2px 0;
        }}
        /* Underline effect on hover */
        a:hover {{
            color: #82e9ff !important;
            text-decoration: underline;
            text-decoration-thickness: 2px;
        }}
        a:focus {{
            outline: 2px solid #ffeb3b;
            outline-offset: 2px;
        }}
        
        /* Progress Bar */
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

        /* change page width and height below to create varyong borders */
        .page {{
            width: var(--page-width);
            height: var(--page-height);
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) scale(0.95);
            opacity: 0;
            color: {BkFontColor};
            overflow-y: auto;
            padding: 20px;
            box-sizing: border-box;
            background: var(--glass-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            -webkit-overflow-scrolling: touch;
            border-radius: 12px;
            border: 1px solid var(--glass-border);
            box-shadow: var(--glass-shadow);
            transition: all 0.6s cubic-bezier(0.65, 0, 0.35, 1);
            z-index: 1;
            display: none;
        }}

        /* Title Page (Page 0) Specific Styles */
        #page-0 h1,
        #page-0 h2,
        #page-0 h3 {{
            color: {BkPage0_FontColor} !important;
        }}

        /* Fixed header elements (page number, book title, back button) */
        .page-header {{
            position: fixed;
            top: 20px;
            width: calc(var(--page-width) - 60px);
            display: flex;
            justify-content: space-between;
            z-index: 3;
            pointer-events: none;
        }}
        /* Keep page number on right */
        .page-number {{
                order: 2; /* Moves to far right */
                right: 0px;
                font-size: 0.85em;
                background: transparent !important;
                visibility: {pageNumberStyle} !important;
        }}

        /* Center book title */
        .book-title {{
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
        }}

        .back-to-toc {{
            color: var(--text-color);
            text-decoration: none;
            font-size: 0.8em;
            padding: 5px 15px;
            background: rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 20px;
            transition: all 0.3s ease;
            pointer-events: auto;
            order: 2; /* Moves to left */
            margin-right: auto; /* Pushes other elements right */
            bottom: 60px; /* Above mobile slider */
        }}
        .back-to-list {{
            color: var(--text-color);
            text-decoration: none;
            font-size: 0.8em;
            padding: 5px 15px;
            background: rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 20px;
            transition: all 0.3s ease;
            pointer-events: auto;
            order: 2; /* Moves to left */
            border-radius: 12px;
            margin-right: auto; /* Pushes other elements right */
            bottom: 60px; /* Above mobile slider */
        }}

        .back-to-toc:hover {{
            background: rgba(0,0,0,0.4);
            color: var(--primary-color);
        }}
        .back-to-list:hover {{
            background: rgba(0,0,0,0.4);
            color: var(--primary-color);
        }}

        /* Fixed Custom Scrollbar */
        .page::-webkit-scrollbar {{
            width: 10px;
        }}

        .page::-webkit-scrollbar-track {{
            background: transparent;
        }}

        .page::-webkit-scrollbar-thumb {{
            background-color: rgba(0,0,0,0.2);
            border-radius: 10px;
            border: 2px solid transparent;
            background-clip: content-box;
        }}

        .page::-webkit-scrollbar-thumb:hover {{
            background-color: rgba(0,0,0,0.3);
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

        .heading-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            gap: 1rem;
            width: 100%;
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
        }}

        /* Arrow Containers - Always present but visibility controlled */
        .arrow-container {{
            position: fixed;
            top: 50%;
            transform: translateY(-50%);
            height: 85vh;
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

        /* When arrows are visible (ARW_DISPLAY=True) */
        .arrow-container[data-visible="true"] {{
            width: {ARW_VISIBLE_WIDTH}% !important;
        }}

        .arrow-container.left {{
            left: 10px;
        }}

        .arrow-container.right {{
            right: 10px;
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

        /* Arrow Hover Areas - Always present but visibility controlled */
        .arrow-area {{
            position: fixed;
            top: 0;
            height: 100%;
            width: var(--arrow-hover-width);
            z-index: 9;
            display: flex;
            pointer-events: auto;
            -webkit-tap-highlight-color: transparent;
        }}

        .arrow-area.left {{
            left: 0;
        }}

        .arrow-area.right {{
            right: 0;
        }}

        .arrow-area.left:hover ~ .arrow-container.left {{
            opacity: var(--arrow-hover-opacity);
        }}

        .arrow-area.right:hover ~ .arrow-container.right {{
            opacity: var(--arrow-hover-opacity);
        }}

        /* Slider Container */
        .slider-container {{
            position: fixed;
            bottom: 10px;
            left: 50%;
            transform: translateX(-50%);
            width: var(--page-width);
            height: 40px;
            background: rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            z-index: 20;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            box-shadow: 0 -5px 15px rgba(0,0,0,0.1);
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
            margin: 10px auto;
            -webkit-appearance: none;
            height: 6px;
            background: rgba(255,255,255,0.2);
            border-radius: 10px;
            outline: none;
            transition: all 0.3s cubic-bezier(0.65, 0, 0.35, 1);
        }}

        .slider::-webkit-slider-thumb {{
            -webkit-appearance: none;
            width: 8px;
            height: 20px;
            background: #000;
            cursor: pointer;
            border-radius: 0;
            box-shadow: none;
            transition: all 0.2s cubic-bezier(0.65, 0, 0.35, 1);
        }}

        .slider-track {{
            position: absolute;
            height: 6px;
            background: #000;
            border-radius: 10px;
            top: 50%;
            transform: translateY(-50%);
            left: 0;
            pointer-events: none;
        }}

        /* Content Styles */
        .image-container {{
            width: 100%;
            position: relative;
            overflow: visible; /* Changed from hidden to visible for captions */
        }}

        .image-container img {{
            position: relative;
            display: block;
            margin: 0 25px 20px 0;
            width: {ImageWidthDesktop};
            height: auto;
            border-radius: 8px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            shape-outside: margin-box;
            transition: all 0.5s cubic-bezier(0.65, 0, 0.35, 1);
            opacity: 0.95;
            transform: scale(0.98);
            filter: drop-shadow(0 4px 12px rgba(0,0,0,0.6));
        }}

        /* Add alignment-specific float rules */
        .image-align-left img {{
            float: left;
            margin: 0 25px 20px 0;
        }}

        .image-align-right img {{
            float: right;
            margin: 0 0 20px 25px;
        }}

        .image-align-center img {{
            float: none;
            margin: 20px auto;
            display: block;
        }}

        .image-container img:hover {{
            opacity: 1;
            transform: scale(1);
            box-shadow: 0 15px 35px rgba(0,0,0,0.9);
            filter: drop-shadow(0 8px 20px rgba(0,0,0,0.8));
        }}

        .text-only-container {{
            width: 90%;
            margin: 30px auto;
            padding: 0;
        }}

        .toc-container {{
            width: 90%;
            margin: 0 auto;
            padding: 20px;
        }}
        .toc-entry {{
            margin: 8px 0;
            padding: 5px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            transition: all 0.3s ease;
        }}

        .toc-entry a {{
            color: {TOC_FontColor} !important;  /* Use configurable color */
            text-decoration: none;
            display: block;
        }}

        .toc-entry:hover {{
            border-bottom-color: var(--primary-color);
        }}

        .toc-entry:hover a {{
            color: var(--primary-color);
        }}

        /* Table Styles */
        table {{
            width: auto;
            max-width: 100%; /* Never exceed content block width */
            table-layout: auto; /* Auto-size columns based on content */
            word-wrap: break-word; /* Allow text wrapping */
            border-collapse: collapse;
            font-size: 0.9em;
            min-width: 400px;
            border-radius: 5px ;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
            background: rgba(15, 15, 15, 0.25) !important;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }}
        /* Special styling for links in tables */
        table a {{
            background: rgba(0, 0, 0, 0.15);
            padding: 2px 6px;
            border-radius: 4px;
            display: inline-block;
        }}

        table a:hover {{
            background: rgba(0, 0, 0, 0.3);
            text-decoration: none;
        }}

        table thead tr {{
            background: transparent !important;
            position: relative; /* Needed for pseudo-element */
            overflow: hidden; /* Contain the blur effect */
        }}

            /* Set minimum column width (adjust 15% as needed) */
        table th,
        table td {{
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            min-width: 15%; /* Minimum column width as % of table */
            max-width: 100%; /* Prevent columns from overflowing */
            word-break: break-word; /* Break long words if needed */
            background: transparent !important;
        }}

        table tbody tr {{
            transition: all 0.2s ease;
            background: rgba(255, 255, 255, 0.05) !important;
        }}

        table tbody tr:last-of-type {{
            border-bottom: 2px solid var(--primary-color);
        }}

        table tbody tr:hover {{
            background-color: rgba(0, 0, 0, 0.3);
        }}

        .highlight-text {{
            color: var(--primary-color);
            font-weight: 300;
            font-size: 1.1em;
            margin-bottom: 0.3em;
            display: inline-block;
            border-bottom: 2px solid var(--primary-color);
            padding-bottom: 3px;
        }}

        p {{
            margin-bottom: 1.8em;
            text-align: left;
            line-height: 1.7;
            font-size: 1.05em;
        }}
        /* Make the paragraph inline */
        p.inline {{
        display: inline;
        }}
    
        /* Hide the paragraph */
        p.none {{
        display: none;
        }}
        h1 {{
            font-size: 2.8em;
            margin: 0 0 10px 0;
            color: #fff;
            font-weight: 700;
        }}
        h2 {{
            font-size: 1.4em;
            margin: 0;
            font-weight: 400;
            color: rgba(255,255,255,0.8);
        }}
        h3 {{
            font-size: 1.3em;
            margin: 20px 0;
            font-weight: 300;
            color: rgba(255,255,255,0.7);
        }}

        /* ================== */
        /* TOC Container */
        .toc-container {{
            width: 90%;
            margin: 0 auto;
            padding: 20px;
        }}

        .toc-button-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 15px;
            justify-content: flex-start !important; /* Add this to align items to the left */
            width: 100%; /* Ensure full width */
        }}

        .compact-button {{
            border: 2px solid #4fc3f7 !important; /* Blue border */
            padding: 6px 12px;
            background: rgba(0,0,0,0.2);
            border-radius: 12px;
            transition: all 0.3s ease;
            white-space: nowrap;
            margin: 2px 0;
            color: {BkFontColor} !important; /* Use your config color */
        }}

        .compact-button:hover {{
            border-color: #82e9ff !important; /* Lighter blue on hover */
            background: rgba(0,0,0,0.4);
            color: var(--primary-color) !important;
        }}

        /* List-style TOC */
        .toc-list .toc-button-container {{
            display: block;
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
        .content-text {{
            font-size: inherit; /* Inherits from parent */
        }}

        /*********************************************/
        /* Multiple in-place images per page.                 */
        /*********************************************/
        .text-content-container {{
            width: 90%;
            padding: 0;
        }}

        /* Style for multiple image containers */
        .image-container + .image-container {{
            margin-top: 10px;
        }}

        /* Ensure images don't get too large when multiple are present */
        .image-container img {{
            max-width: 100%;
            height: auto;
        }}

        /* Inline image styling */
        .inline-image-wrapper {{
            display: block;
            text-align: center;
        }}

        .inline-image {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }}

        .inline-image-caption {{
            font-style: italic;
            font-size: 0.9em;
            margin-top: 10px;
            color: rgba(255,255,255,0.7);
            text-align: center;
        }}

        /*********************************************/
        /* Caption Pop-up Box - Begin */
        /*********************************************/
        
        .image-caption-popup {{
            position: absolute;
            
            /* REMOVE: left: 0; */
            /* Position relative to the image container */
            top: 0;

            /* Width handling - auto for text, but constrained */
            width: auto;
            max-width: calc({ImageWidthDesktop} * 0.95) !important;
            font-size: .8em;
            padding: 3px 10px 3px 10px;
            box-sizing: border-box;

            /* INITIAL STATE - HIDDEN */
            opacity: 0 !important;
            transform: translateY(-20px) scale(0.95) !important;
            transition: all 0.5s cubic-bezier(0.65, 0, 0.35, 1) !important;
            pointer-events: none;

            /* GLASS MORPHISM EFFECT */
            background: rgba(0, 0, 0, 0.45) !important;
            backdrop-filter: blur(15px) !important;
            -webkit-backdrop-filter: blur(15px) !important;
            
            border-radius: 8px;
            box-shadow: 0 5px 5px rgba(0, 0, 0, 0.95);
            z-index: 1000;
        }}
        /* Position captions based on alignment */
        .image-align-left .image-caption-popup {{
            top: 20px;
            left: 0;
            right: auto;
        }}
        .image-align-right .image-caption-popup {{
            top: 20px;
            right: 0;
            left: auto;
        }}

        /*  keeep this together.  */
        .image-align-center .image-caption-popup {{
            left: 50% !important; /* Center horizontally */
            transform: translateX(-50%) !important;
        }}
        /* Hover state for centered captions */
        .image-align-center .image-caption-popup:hover,
        .image-align-center img:hover ~ .image-caption-popup {{
            transform: translateX(-50%) t!important;
        }}
        /*  keeep this together.  */        

        /* SHOW / HIDE POP-UP when hovering over image OR pop-up itself */
        .image-container img:hover ~ .image-caption-popup,
        .image-caption-popup:hover {{
            opacity: 1 !important;
            pointer-events: auto !important;
        }}


        /* Ensure z-index stacking */
        body .page .image-container .image-caption-popup {{
            z-index: 1000 !important;
        }}
        body .page .image-container img {{
            z-index: 2 !important;
        }}
                
        /* PERMANENTLY SHOW POPUP: Force all popups to be always visible 
        .image-caption-popup {{
            top: 30px;
            opacity: 1 !important;
            transform: none; !important;
            pointer-events: auto !important;
            transition: none !important;
        }}
        /*********************************************/
        /* Caption Pop-up Box - End */
        /*********************************************/

       /* Tablets and such */

        @media (max-width: 768px) {{

            body {{
                margin-top: 0px !important;
                height: 75% !important;
                overflow: hidden;
            }}

            /* Fix for iOS Safari */
            @supports (-webkit-touch-callout: none) {{
                .page {{
                    height: -webkit-fill-available !important;
                    margin-top: 0 !important;
                }}
            }}        

                /* Book title - below back button */
            .book-title {{
                font-size: 0.75em; /* Slightly smaller */
                margin-bottom: 15px !important;
            }} 

            .back-to-List {{
                padding: 6px 12px;
                font-size: 0.85em;
            }} 

            /* Page number - top right */
        

            a {{
                color: #00b0ff !important; /* Even brighter for mobile */
            }}

            a:focus {{
                outline: 2px solid #ffeb3b;
                outline-offset: 2px;
            }}

            .text-only-container {{
                width: 100% !important;
                padding: 0 10px !important;
                margin: 15px auto !important;
            }}

            /* Improved spacing for mobile text */
            p, h1, h2, h3 {{
                margin-bottom: 1.2em !important;
                line-height: 1.6 !important;
            }}

            /* Adjust heading sizes for mobile */
            h1 {{ font-size: 2.2em !important; }}
            h2 {{ font-size: 1.3em !important; }}
            h3 {{ font-size: 1.1em !important; }}

            /* Mobile table styles */
            table {{
                min-width: 0 !important /* ALlow Shrinking */
                width: 100%; !important /* Full width on mobile */
                overflow-x: visible !important; /* Disable scrolling */
                backdrop-filter: blur(8px);
                -webkit-backdrop-filter: blur(8px);
                background: rgba(15, 15, 15, 0.3) !important;
                font-size: 0.9em !important;
            }}
            table * {{
            box-sizing: border-box !important; /* Include padding in width */
            }}
            
            table a {{
                padding: 3px 8px; /* Larger tap targets */
                background: rgba(0, 0, 0, 0.2); /* More contrast */
                margin: 0 auto !important;
            }}
            .table-container {{
                width: calc(100% - 10px) !important;
                overflow-x: visible !important; /* Disable scrolling */
            }}
            table th,
            table td {{
                min-width: 0% !important ; /* Larger minimum on small screens */
                white-space: normal !important; /* Ensure wrapping on mobile */
                width: auto !important; /* Reset widths */
                max-width: 100% !important;      
            }}
                /* Slightly stronger contrast on mobile for readability */
            table thead tr {{
                background: rgba(0, 0, 0, 0.4) !important;
            }}
            table td.important-column {{
                width: 60% !important;
                word-break: break-word !important; /* Break long words */
                overflow-wrap: anywhere !important; /* Emergency break */
            }}
            table td {{
                hyphens: auto !important;
                word-break: break-word !important; /* Break long words */
                overflow-wrap: anywhere !important; /* Emergency break */
            }}
            /* Force links/buttons to wrap */
            table a, table button {{
            white-space: normal !important;
            display: inline-block !important;
            }}

            .toc-container {{
                width: 95%;
                padding: 15px 5px;
            }}
            
            .toc-entry {{
                margin: 6px 0;
            }}
        }}

       /* phones and such */ 


        @media (max-width: 415px) {{
            body {{
                margin-top: 0px !important;
                height: 60% !important;
                overflow: hidden;
            }}

            .page {{
                /* Adjust height calculation */
                height: 60vh !important;
            }}
            .content-text {{
                font-size: var(--mobile-font-size) !important;
            }}
            
            /* Fix for iOS Safari */
            @supports (-webkit-touch-callout: none) {{
                .page {{
                    height: -webkit-fill-available !important;
                    margin-top: 0 !important;
                }}
            }}
            .image-container img {{
                float: none;
            }}
            .back-to-toc {{
                font-size: 0.6em;
                padding: 5px 5px;
                border-radius: 10px;
            }}
            .back-to-list {{
                font-size: 0.6em;
            }}
        
            .toc-container {{
                margin-top: 50px;
                width: 95%;
            }}
              /* Reduce gap after heading */
            .toc-container h2 {{
                margin-bottom: 8px !important; /* Reduce space below title */
            }}
            .compact-button {{
            padding: 3px 8px !important;
            font-size: 0.65em !important;
            }}

            /* Force center alignment for mobile */
            .mobile-align-center {{
                text-align: center !important;
            }}
            
            /* FORCE ALIGNMENT FORCE TO CENTER */
            .mobile-align-center img {{
                float: none !important;
                margin: 10px auto !important;
                display: block !important;
                box-shadow: 0 5px 5px rgba(0,0,0,0.5);
            }}
            .mobile-align-center img:hover {{
            opacity: 1;
            transform: scale(1);
            box-shadow: 0 10px 10px rgba(0,0,0,0.9);
            filter: drop-shadow(0 8px 20px rgba(0,0,0,0.8));
            }}

            /* FORCE SIZE FORCE TO ImageWidthMobile */
            /* Set mobile width for images without specified size */
            .mobile-default-size img {{
                width: {ImageWidthMobile} !important;
                max-width: 100% !important;
                height: auto !important;
                float: none !important;
            }}

            /* FORCEe ALL CAPTION POPUPS to be CENTERED on mobile */
            /* Override all alignment-specific positioning */
            .image-align-left .image-caption-popup,
            .image-align-right .image-caption-popup,
            .image-align-center .image-caption-popup {{
                width: {ImageWidthMobile} !important;
                float: none;
                margin: 0 !important;
                left: 50% !important;
                top: 0px !important;
                right: auto !important;
                transform: translateX(-50%) !important;
                text-align: center !important;
                font-size: 0.8em;
                pointer-events: auto; /* Ensure clickable on mobile */
            }}            

            
            /* Make captions always visible on mobile when active */
            .image-caption-popup.mobile-visible {{
                opacity: 1;
                transform: translateY(0);
            }}


            /* ===== TABLE STYLES ===== */
            .table-container {{
                width: 100% !important;
                overflow-x: auto !important;
                -webkit-overflow-scrolling: touch !important;
                display: block;
                margin: 15px 0;
                background: rgba(0,0,0,0.1); /* Visual cue for scrollable area */
                border-radius: 8px;
                padding: 8px 0;
            }}

            table {{
                display: table !important; /* Revert to table layout but allow scrolling */
                width: auto !important;
                min-width: 100% !important; /* Ensure it fills container */
                white-space: nowrap;
                font-size: 0.85em; /* Slightly smaller text for tables */
            }}

            table th,
            table td {{
                white-space: nowrap !important;
                min-width: 100px !important; /* Reasonable minimum column width */
            }}

            /* Optional scroll indicator */
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
            <input type="range" min="0" max="TOTALPAGES" value="INITIAL_PAGE" class="slider" id="page-slider">
        </div>
        <div class="slider-info">
            <span id="current-page">INITIAL_PAGE</span>/<span id="total-pages">TOTALPAGES</span>
        </div>
    </div>

    <script>
        let currentPage = INITIAL_PAGE;
        const totalPages = TOTALPAGES;
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

        // FIXED: Image caption handling
        document.addEventListener('DOMContentLoaded', () => {
            // Debug: Check if captions are being generated
            console.log('Image captions found:', document.querySelectorAll('.image-caption-popup').length);
            document.querySelectorAll('.image-caption-popup').forEach((caption, i) => {
                console.log(`Caption ${i}:`, caption.textContent);
            });

            // Make captions click-to-toggle on mobile
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


            // Manual pop-up toggle for testing
            document.addEventListener('DOMContentLoaded', () => {
                console.log('=== MANUAL POPUP TEST ===');
                
                let allPopupsVisible = false;
                
                // Add toggle button for testing
                const testButton = document.createElement('button');
                testButton.textContent = 'Toggle All Popups';
                testButton.style.position = 'fixed';
                testButton.style.top = '10px';
                testButton.style.right = '10px';
                testButton.style.zIndex = '9999';
                testButton.style.padding = '10px';
                testButton.style.background = 'red';
                testButton.style.color = 'white';
                testButton.style.border = 'none';
                testButton.style.borderRadius = '5px';
                testButton.style.cursor = 'pointer';
                
                testButton.addEventListener('click', () => {
                    allPopupsVisible = !allPopupsVisible;
                    const popups = document.querySelectorAll('.image-caption-popup');
                    
                    popups.forEach(popup => {
                        if (allPopupsVisible) {
                            popup.style.opacity = '1';
                            popup.style.transform = 'translateY(0) scale(1)';
                            popup.style.background = 'rgba(255,0,0,0.9)';
                        } else {
                            popup.style.opacity = '';
                            popup.style.transform = '';
                            popup.style.background = '';
                        }
                    });
                    
                    console.log('All popups', allPopupsVisible ? 'VISIBLE' : 'HIDDEN');
                });
                
                document.body.appendChild(testButton);
            });            
            
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

        // Determine initial page based on configuration
        function getInitialPage() {
            const page0Skipped = {Page0_skip};
            const hasTOC = document.getElementById('page-toc') !== null;
            
            if (page0Skipped && hasTOC) {
                return 0; // Start at TOC (page 0)
            } else if (!page0Skipped && hasTOC) {
                return 0; // Start at title page (page 0)
            } else if (page0Skipped && !hasTOC) {
                return 0; // Start at first content page (page 0)
            } else {
                return 0; // Start at title page (page 0)
            }
        }

        // Initialize with correct active page
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
            const startPage = {Page0_skip} ? 0 : 1;

            for (let i = startPage; i < pages.length; i++) {

                // Skip TOC page
                if (pages[i].id === 'page-toc') continue;            

                const header = document.createElement('div');
                header.className = 'page-header';
                
                // Back to TOC button (left side)
                if (document.getElementById('page-toc')) {
                    const backButton = document.createElement('a');
                    backButton.className = 'back-to-toc';
                    backButton.href = '#page-toc';
                    backButton.textContent = 'Contents';
                    header.appendChild(backButton);
                }
                
                // Page number (right side)
                const pageNumber = document.createElement('div');
                pageNumber.className = 'page-number';
                pageNumber.textContent = calculatePageNumber(i);
                header.appendChild(pageNumber);
                
                pages[i].insertBefore(header, pages[i].firstChild);
            }
            
            // Touch events for swipe
            let touchStartX = 0;
            let touchEndX = 0;

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

            // Arrow click events
            leftArrowContainer.addEventListener('click', prevPage);
            rightArrowContainer.addEventListener('click', nextPage);

            // TOC Navigation (handles both list and button styles)
            document.querySelectorAll('.toc-link, .back-to-toc').forEach(link => {
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

        // Calculate proper page number based on Page0_skip and TOC
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
            if (pageNum < 0 || pageNum > totalPages) return;
            
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
            }, 300);
        }

        function nextPage() {
            if (currentPage < totalPages - 1) {
                goToPage(currentPage + 1);
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
        function updateSlider() {
            slider.value = currentPage;
            currentPageDisplay.textContent = currentPage;
            updateSliderTrack();
        }

        function updateProgress() {
            const progress = (currentPage / totalPages) * 100;
            progressBar.style.width = `${progress}%`;
        }

        
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

        // Current date display
        document.addEventListener('DOMContentLoaded', function() {
            const options = { 
                year: 'numeric', 
                month: 'short', 
                day: 'numeric',
                // hour: '2-digit',
                // minute: '2-digit'
            };
            document.getElementById('currentDate').textContent = 
                new Date().toLocaleDateString('en-US', options);
        });
        
    </script>
</body>
</html>
"""

def rep_mdate(content):
    """Replace _getMdate("filename") patterns with actual modification dates (case-insensitive)"""
    def replace_mdate(match):
        filename = match.group(1)
        date_value = get_mdate(filename)
        # Simple approach using opacity for lighter appearance
        return f'<span style="font-size: 0.8em; color: {CONFIG["BkFontColor"]}; opacity: 0.65;">{date_value}</span>'
    
    pattern = r'_getMdate\("([^"]+)"\)'
    return re.sub(pattern, replace_mdate, content, flags=re.IGNORECASE)



def clean_content(content):
    """Clean content while perfectly preserving paragraph content, processing fonts, and cleaning markdown"""
    
    # 1. FONT TAG HANDLING (Original Logic)
    # First protect <br> tags inside font tags to prevent them from being modified
    protected_content = re.sub(r'(<font[^>]*>.*?)<br>(.*?</font>)', 
                             r'\1<!--BR_TAG-->\2', 
                             content, 
                             flags=re.DOTALL)
    
    # Extract title from font tags using original matching logic
    title_match = re.search(r'<font[^>]*>(.*?)</font>', protected_content)
    if title_match:
        title_content = title_match.group(1).strip()
        # Only return title if there's actual content
        title = title_content.replace('<!--BR_TAG-->', '<br>') if title_content else None
    else:
        title = None

    # 2. PARAGRAPH PROTECTION (No Changes Inside)
    protected_paragraphs = []
    
    def protect_paragraphs(match):
        """Callback to store original paragraphs exactly as they are"""
        protected_paragraphs.append(match.group(0))
        return f"<!--PARAGRAPH_{len(protected_paragraphs)-1}-->"

    # Find and protect all <p> tags (with any attributes and content)
    content = re.sub(r'<p\b[^>]*>.*?</p>', protect_paragraphs, content, flags=re.DOTALL)

    # 3. ORIGINAL FONT TAG REMOVAL
    # Remove font tags after extracting title (original behavior)
    if title:
        content = re.sub(r'<font[^>]*>.*?</font>', '', content, flags=re.DOTALL)

    # 4. LINK CONVERSION (Original Logic)
    def convert_links(match):
        """Convert markdown links to HTML links (3 supported formats)"""
        # Format 1: [text](url)
        if match.group(1) and match.group(2):
            #return f'<a href="{match.group(2)}" target="_blank">{match.group(1)}</a>'
            return f'<a href="{match.group(2)}">{match.group(1)}</a>'
        # Format 2: plain URL (http://...)
        elif match.group(3):
            url = match.group(3)
            #return f'<a href="{url}" target="_blank">{url}</a>'
            return f'<a href="{url}">{url}</a>'
        return match.group(0)

    # Process all link formats in the content
    content = re.sub(
        r'\[([^\]]*)\]\(([^)]+)\)|(https?://[^\s<>]+)',  # Matches both formats
        convert_links,
        content
    )

    # 5. TABLE PROCESSING (Original Logic)
    def process_table(match):
        """Convert markdown tables to HTML tables"""
        return convert_markdown_table_to_html(match.group(0))

    # Find and convert markdown tables (format: | Header | ... |)
    content = re.sub(
        r'(\n\|[^\n]+\|\n\|[-:|]+\|[\s\S]*?)(?=\n\n|\Z)',  # Table pattern
        process_table,
        content
    )

    # 6. MARKDOWN CLEANING (Original Logic)
    # Remove markdown headings (lines containing ##)
    content = re.sub(r'^.*##.*$', '', content, flags=re.MULTILINE)
    # Remove bold formatting (**text** or __text__)
    content = re.sub(r'(\*\*|__)(.*?)\1', r'\2', content)
    # Remove highlight formatting (==text==)
    content = re.sub(r'==(.*?)==', r'\1', content)
    # Remove italics (*text* or _text_)
    content = re.sub(r'(\*|_)(.*?)\1', r'\2', content)
    # Remove underline tags (<u>text</u>)
    content = re.sub(r'<u>(.*?)</u>', r'\1', content, flags=re.DOTALL)
    # Remove span tags (<span ...>text</span>)
    content = re.sub(r'<span[^>]*>(.*?)</span>', r'\1', content, flags=re.DOTALL)
    # Remove emphasis tags (<em>text</em>)
    content = re.sub(r'<em>(.*?)</em>', r'\1', content, flags=re.DOTALL)

    # 7. RESTORE PROTECTED PARAGRAPHS (Exactly As They Were)
    # Put back all original paragraph tags without any changes
    for i, para in enumerate(protected_paragraphs):
        content = content.replace(f"<!--PARAGRAPH_{i}-->", para)

    # 8. LINE BREAK HANDLING (Only Between Text Paragraphs)
    # Split content by paragraphs to avoid modifying inside them
    parts = re.split(r'(<p\b[^>]*>.*?</p>)', content, flags=re.DOTALL)
    processed_parts = []
    
    for i, part in enumerate(parts):
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

    return title, processed_content.strip()

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



def page_num_toc(main_string, substring_to_count, search_text):
    """
    Counts the number of times a substring (now the page break div) appears in a larger string,
    but only up to a specific search text (the heading).

    Args:
        main_string (str): The string to be searched.
        substring_to_count (str): The substring to be counted (ignored, we use the div).
        search_text (str): The text that acts as the cutoff point for the search.

    Returns:
        int: The number of times the page break div was found before the heading.
    """
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



def generate_toc(content):
    """Generate table of contents with book title header"""
    toc_entries = []
    
    headings = re.findall(r'^(#+)\s+(.+)$', content, re.MULTILINE)
    
    for level, title in headings:
        if level == '#':  # Skip H1
            continue
            
        indent = (len(level) - 2) * 20

        # page_num = page_num_toc(content, '![[', '## '+title)
        page_num = page_num_toc(content, 'dummy_string', '## '+title)
        href = f'#page-{page_num}'


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
                f'<a href="{href}" class="back-to-toc compact-button toc-link">'
                f'{title.strip() + "(" + f"{page_num}" + ")"}'
                f'</a>'
            )
    
    if not toc_entries:
        return None
    
    # Add booklist link button if enabled
    booklist_button = ''
    if CONFIG['TOC_ENABLE'] and CONFIG['BkListLink_show'] == 1:
        url = CONFIG['BkLinkURL']
        if not url.startswith(('http://', 'https://')):
            url = f'https://{url}'
            
        # ORIGINAL <button onclick="window.open('{url}', '_blank')" class="back-to-list">
        booklist_button = f"""
        <button onclick="window.open('{url}', '_self')" class="back-to-list">
            AboutMe
        </button>
        """
    
    # Add book title to TOC page
    book_title = f'<div class="book-title">{CONFIG["BkPage0_Title"]}</div>'
    
    # Determine container class based on TOC style
    container_class = "toc-list" if CONFIG['TOCasList'] else "toc-buttons"
        
    return f"""
    <div class="page" id="page-toc">
        {book_title}
        <div class="toc-container {container_class}">
            <h2>{CONFIG["TOC_TITLE"]}</h2>
            {booklist_button}
            <div class="toc-button-container">
                {"".join(toc_entries)}
            </div>
        </div>
    </div>
    """


def build_page_html(counter, image_filename, description, title, content):
    """Build HTML for a single page with image description (tooltip and pop-up)"""
    page_id = f"page-{counter}" if counter != "toc" else "page-toc"
    
    # Book title for non-cover pages
    book_title = ''
    if counter != 0:
        book_title = f'<div class="book-title">{CONFIG["BkPage0_Title"]}</div>'
    
    # Title styling
    if title and title.strip():
        styled_title = f'<span style="font-size: {CONFIG["TitleFontSize"]}">{title}</span>'
        title_part = f'<p><span class="highlight-text">{styled_title}</span></p>'
    else:
        title_part = ''
    
    # Image with tooltip AND pop-up caption
    image_html = ''
    caption_popup = ''
    
    if image_filename:
        # Tooltip (title attribute)
        # to get tooltip uncomment these lines
        #title_attr = f' title="{escape(description)}"' if description else ""
        #image_html = f'<img src="{escape(image_filename)}" alt="Image {counter}"{title_attr}>'
        image_html = f'<img src="{escape(image_filename)}" alt="Image {counter}">'

        # Pop-up caption box (only if description exists)
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
            {book_title}
            <div class="image-container {position}">
                {image_html}
                {caption_popup}
                {title_part}
                {styled_content}
            </div>
        </div>
        """
    else:
        return f"""
        <div class="page" id="{page_id}">
            {book_title}
            <div class="text-only-container">
                {title_part}
                {styled_content}
            </div>
        </div>
        """

    

def remove_before_page_break_flexible(input_string):
    """
    More flexible version that handles potential whitespace variations.
    Removes everything from a string before the first occurrence of the page break div.
    
    Args:
        input_string (str): The input string to process
        
    Returns:
        str: The string content starting from the page break div
    """
    import re
    
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


# Image Syntax Options: ![[ filename | description | size | alignment ]]
# # 
# ![[image.jpeg]] - Just filename
# ![[image.jpeg | Beautiful sunset]] - Filename + description
# ![[image.jpeg | | 300px]] - Filename + pixel size
# ![[image.jpeg | | 50%]] - Filename + percentage size
# ![[image.jpeg | | 400x300]] - Filename + dimensions
# ![[image.jpeg | | 300]] - Filename + auto-px size
# ![[image.jpeg | | | center]] - Filename + center alignment
# ![[image.jpeg | | | left]] - Filename + left alignment
# ![[image.jpeg | | | right]] - Filename + right alignment
# ![[image.jpeg | Sunset | 300px]] - Filename + description + pixel size
# ![[image.jpeg | Landscape | 50%]] - Filename + description + percentage size
# ![[image.jpeg | Portrait | 400x300]] - Filename + description + dimensions
# ![[image.jpeg | Photo | 300]] - Filename + description + auto-px size
# ![[image.jpeg | Sunset | | center]] - Filename + description + center alignment
# ![[image.jpeg | Landscape | | left]] - Filename + description + left alignment
# ![[image.jpeg | Portrait | | right]] - Filename + description + right alignment
# ![[image.jpeg | | 300px | center]] - Filename + pixel size + center alignment
# ![[image.jpeg | | 50% | left]] - Filename + percentage size + left alignment
# ![[image.jpeg | | 400x300 | right]] - Filename + dimensions + right alignment
# ![[image.jpeg | | 300 | center]] - Filename + auto-px size + center alignment
# ![[image.jpeg | Beautiful sunset | 300px | center]] - All parameters: centered
# ![[image.jpeg | Landscape view | 50% | left]] - All parameters: left aligned
# ![[image.jpeg | Portrait photo | 400x300 | right]] - All parameters: right aligned
# ![[image.jpeg | Nature scene | 300 | center]] - All parameters: auto-px + centered
# ![[image.jpeg | | 50%x200px | center]] - 50% width, 200px height, centered
# ![[image.jpeg | | 300pxx50% | left]] - 300px width, 50% height, left aligned
# ![[image.jpeg | | 80%x60% | right]] - 80% width, 60% height, right aligned
# ![[image.jpeg ||300px|]] - No description, 300px size, default alignment
# ![[image.jpeg |Description||] - Description, default size, default alignment
# ![[image.jpeg |||center]] - No description, default size, centered
# 
# 300px - Fixed pixels
# 50% - Percentage width
# 400x300 - Width × Height
# 400 - Auto-convert to pixels
# Alignment Options:
# 
# center - Centered
# left - Left aligned, text wraps right
# right - Right aligned, text wraps left
# All parameters are optional except the filename! Use empty | placeholders to skip parameters.

def convert_inline_images(content):
    """Fixed parser that handles alignment correctly with px and % size support"""
    
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
        size_spec = parts[2] if len(parts) > 2 and parts[2] != "" else ""
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
                caption_width_style = f' style="--image-width: {size_spec}; width: var(--image-width); max-width: var(--image-width);"'
            
            # Handle pixel values (e.g., "300px" or "300")
            elif size_spec.endswith('px') or size_spec.isdigit():
                width_value = size_spec if size_spec.endswith('px') else f"{size_spec}px"
                style_attr = f' style="width: {width_value};"'
                caption_width_style = f' style="--image-width: {width_value}; width: var(--image-width); max-width: var(--image-width);"'
            
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
                except ValueError:
                    # Fallback if dimension parsing fails
                    style_attr = f' style="width: {size_spec};"'

        # Create HTML with inline width styling for caption
        image_html = f'<img src="{escape(image_filename)}" alt="Image"{style_attr}>'
        
        # NEW: Apply the calculated width to the caption
        caption_html = f'<div class="image-caption-popup"{caption_width_style}>{escape(description)}</div>' if description else ''
        
        return f'<div class="image-container{alignment_class}">{image_html}{caption_html}</div>'
    
    return re.sub(r'!\[\[.*?\]\]', replace_image, content)


def process_markdown(content):
    """Process markdown content and return list of page HTMLs. Uses <div style="break-after: page;"></div> as page separator."""
    pages = []
    
    # remove everything before 1st page break
    content = remove_before_page_break_flexible(content)

    # Generate TOC if enabled
    toc_html = generate_toc(content) if CONFIG['TOC_ENABLE'] else None
    
    try:
        # Split the entire content by the page break div
        page_sections = re.split(r'(?=<div style="break-after: page;"></div>)', content)
        
        # Filter out any empty sections
        page_sections = [section.strip() for section in page_sections if section.strip()]
        
        logging.debug(f"Found {len(page_sections)} page sections using break-after div")

        # Process each section as a separate page
        for counter, section_content in enumerate(page_sections, 1):
            # Remove the page break div from the start of the content, if it exists
            cleaned_section = re.sub(r'^<div style="break-after: page;"></div>', '', section_content)
            
            # Convert inline images to HTML while preserving their position
            processed_content = convert_inline_images(cleaned_section)
            
            title, cleaned_content = clean_content(processed_content)
            
            # Pass None for image_filename and description to avoid main image container
            page_html = build_page_html(counter, None, None, title, cleaned_content)
            
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

def get_mdate(fname):
    # Get source file modification date
    script_dir = Path(__file__).parent
    source_md_path = resolve_relative_path(fname, script_dir)
    if source_md_path.exists():
        mod_time = datetime.fromtimestamp(source_md_path.stat().st_mtime)
        #last_modified = mod_time.strftime('%B %d, %Y at %I:%M %p')
        last_modified = mod_time.strftime('%b %d, %Y')
    else:
        last_modified = "Unknown date"

    return last_modified

def build_final_html(pages):
    """Assemble the final HTML document with responsive font scaling"""
    total_pages = len(pages)

    title_page_html = ''
    if not CONFIG['Page0_skip']:
        title_page_html = f"""
    <div class="page active" id="page-0">
        <div class="heading-container">
            <h1>{escape(CONFIG['BkPage0_Title'])}</h1>
            <br><br>
            <h2>{escape(CONFIG['BkPage0_Tag'])}</h2>
            <p style="font-size: 0.9em; text-align: center; opacity: 0.8;">
                <br><br>Last updated: {get_mdate(CONFIG['source_md'])}<br><br>
            </p>
            <h3>{escape(CONFIG['BkPage0_head3'])}</h3>
        </div>
    </div>
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
        'ImageWidthMobile': CONFIG['ImageWidthMobile'],
        'BkPage0_Title': escape(CONFIG['BkPage0_Title']),
        'BkPage0_Description': escape(CONFIG['BkPage0_Description']),
        'BkPage0_Keywords': escape(CONFIG['BkPage0_Keywords']),
        'BkPage0_Tag': escape(CONFIG['BkPage0_Tag']),
        'BkPage0_head3': escape(CONFIG['BkPage0_head3']),
        'TOC_FontColor': CONFIG.get('TOC_FontColor', '#ffffff'),
        'pageNumberStyle': "hidden" if CONFIG.get('Hide_page_number', False) else "visible"
    }
    
    # Format main template with mobile CSS included
    html_template = HTML_TEMPLATE.format(**template_vars)

    # Prepare footer with dynamic values
    footer = FOOTER_TEMPLATE\
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

def main():
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
        output_html.write_text(final_html, encoding='utf-8')
        logging.info(f"Created {output_html} with {len(pages)} pages")
        
    except Exception as e:
        logging.error(f"Conversion failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
    