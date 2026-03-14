#!/usr/bin/env python3
"""
CRTP Migration Script - BeautifulSoup based
Extracts sections from Notion HTML export and converts to clean Markdown
"""

import os
import re
import shutil
from bs4 import BeautifulSoup
import urllib.parse

# Configuration
HTML_FILE = "/home/stark/Downloads/crtp-export-new/crtp-final/CRTP - Certified Red Team Professional 30c79e9ad7c9801b9285cbdbfdd8d9e4.html"
IMAGE_DIR = "/home/stark/Downloads/crtp-export-new/crtp-final/CRTP - Certified Red Team Professional"
OUTPUT_DIR = "/home/stark/mr-stark-study-notes/certifications/crtp"
ASSETS_DIR = "/home/stark/mr-stark-study-notes/assets/crtp"

# Section mapping from summary title to filename
SECTION_MAP = {
    "Enumeration": "enumeration.md",
    "Privilege Escalation": "privilege-escalation.md",
    "Privilege Escalation via Domain Admin session": "privilege-escalation-domain-admin.md",
    "Golden Ticket": "golden-ticket.md",
    "Silver Ticket": "silver-ticket.md",
    "Diamond Ticket": "diamond-ticket.md",
    "Abusing DSRM Credentials": "abusing-dsrm-credentials.md",
    "DCSync Attack": "dcsync-attack.md",
    "Security Descriptor Abuse": "security-descriptor-abuse.md",
    "ASREP-Roasting Attack": "asrep-roasting.md",
    "Unconstrained Delegation": "unconstrained-delegation.md",
    "Constrained Delegation": "constrained-delegation.md",
    "Resource-Based Constrained Delegation (RBCD)": "rbcd.md",
    "Enterprise Admins Trust - SID-History Abuse with Trust Ticket": "sid-history-trust-ticket.md",
    "Enterprise Admin Trust - SID-History Abuse with KRBTGT hash": "sid-history-krbtgt.md",
    "CrossForest Trust - Trust Flow": "cross-forest-trust.md",
    "ADCS Attacks": "adcs-attacks.md",
    "Trust Links Abuse": "trust-links-abuse.md",
    "MDE/MDI Bypass": "mde-mdi-bypass.md",
}


def extract_summary_title(details):
    """Extract title from details/summary tag"""
    summary = details.find('summary')
    if summary:
        # Get text content, handling strong tags
        title = summary.get_text()
        # Clean up
        title = re.sub(r'\s+', ' ', title).strip()
        return title
    return None


def extract_details_content(details):
    """Extract all content inside details tag after the summary"""
    content_parts = []
    summary = details.find('summary')
    if summary:
        # Get all siblings after summary
        for sibling in summary.find_next_siblings():
            content_parts.append(str(sibling))
    return ''.join(content_parts)


def find_all_details_sections(body):
    """Find all top-level details sections in the body"""
    sections = {}
    
    # Find all ul with class="toggle"
    toggle_uls = body.find_all('ul', class_='toggle')
    
    for ul in toggle_uls:
        # Find direct li children
        for li in ul.find_all('li', recursive=False):
            # Find details in li
            details = li.find('details', recursive=False)
            if details:
                title = extract_summary_title(details)
                if title and title in SECTION_MAP:
                    content = extract_details_content(details)
                    if len(content) > 50:  # Reasonable content check
                        sections[title] = content
                        print(f"Found section: {title} ({len(content)} chars)")
    
    return sections


def process_images():
    """Copy images to assets directory"""
    os.makedirs(ASSETS_DIR, exist_ok=True)
    
    # Get all image files from export
    image_files = [f for f in os.listdir(IMAGE_DIR) if f.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
    
    # Copy each image
    for filename in image_files:
        src_path = os.path.join(IMAGE_DIR, filename)
        dst_path = os.path.join(ASSETS_DIR, filename)
        if not os.path.exists(dst_path):
            shutil.copy2(src_path, dst_path)
    
    print(f"Total images copied: {len(image_files)}")


def html_to_markdown(html_content):
    """Convert HTML content to clean Markdown"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove unwanted tags
    for tag in soup(['style', 'script', 'figure', 'figcaption', 'mark']):
        tag.decompose()
    
    # Remove display:contents divs
    for tag in soup.find_all('div'):
        style = tag.get('style', '')
        if 'display:contents' in str(style):
            tag.unwrap()
        elif tag.get('class') == [] and not tag.contents:
            tag.decompose()
        else:
            tag.unwrap()
    
    markdown = ""
    
    # Process all elements in order
    elements = soup.find_all(True)
    
    for i, element in enumerate(elements):
        # Skip if already processed
        if element.name in ['html', 'head', 'body', 'article']:
            continue
            
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = element.name
            text = element.get_text(strip=True)
            if text:
                prefix = '#' * int(level[1])
                markdown += f"\n{prefix} {text}\n\n"
        
        elif element.name == 'p':
            text = process_paragraph_element(element)
            if text:
                markdown += f"{text}\n\n"
        
        elif element.name == 'ul':
            if 'toggle' not in element.get('class', []):
                text = process_list_element(element)
                if text:
                    markdown += f"{text}\n"
        
        elif element.name == 'ol':
            text = process_ol_element(element)
            if text:
                markdown += f"{text}\n"
        
        elif element.name == 'pre':
            text = process_pre_element(element)
            if text:
                markdown += f"{text}\n\n"
        
        elif element.name == 'img':
            src = element.get('src', '')
            if src and not src.startswith('http'):
                filename = os.path.basename(urllib.parse.unquote(src))
                markdown += f"![{filename}](/assets/crtp/{filename})\n\n"
    
    # Clean up
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    markdown = markdown.strip()
    
    return markdown


def process_paragraph_element(p):
    """Process a paragraph element"""
    result = ""
    
    for child in p.children:
        if hasattr(child, 'name') and child.name:
            if child.name == 'code':
                result += f"`{child.get_text()}`"
            elif child.name in ['strong', 'b']:
                text = child.get_text(strip=True)
                if text:
                    result += f"**{text}**"
            elif child.name in ['em', 'i']:
                text = child.get_text(strip=True)
                if text:
                    result += f"*{text}*"
            elif child.name == 'a':
                href = child.get('href', '')
                text = child.get_text(strip=True)
                if text and href:
                    result += f"[{text}]({href})"
            elif child.name == 'br':
                result += "\n"
        elif isinstance(child, str):
            result += child
    
    return result.strip()


def process_list_element(ul):
    """Process unordered list"""
    markdown = ""
    items = ul.find_all('li', recursive=False)
    
    for item in items:
        # Get text excluding nested lists
        text = item.get_text()
        for nested in item.find_all(['ul', 'ol']):
            text = text.replace(nested.get_text(), '')
        text = text.strip()
        
        if text:
            markdown += f"- {text}\n"
        
        # Process nested lists
        for nested in item.find_all(['ul', 'ol'], recursive=False):
            for nested_item in nested.find_all('li', recursive=False):
                nested_text = nested_item.get_text(strip=True)
                if nested_text:
                    prefix = "- " if nested.name == 'ul' else "  - "
                    markdown += f"  {prefix}{nested_text}\n"
    
    return markdown


def process_ol_element(ol):
    """Process ordered list"""
    markdown = ""
    items = ol.find_all('li', recursive=False)
    start = int(ol.get('start', 1))
    
    for i, item in enumerate(items):
        text = item.get_text()
        for nested in item.find_all(['ul', 'ol']):
            text = text.replace(nested.get_text(), '')
        text = text.strip()
        
        if text:
            markdown += f"{start + i}. {text}\n"
        
        # Process nested lists
        for nested in item.find_all(['ul', 'ol'], recursive=False):
            for nested_item in nested.find_all('li', recursive=False):
                nested_text = nested_item.get_text(strip=True)
                if nested_text:
                    prefix = "- " if nested.name == 'ul' else "  - "
                    markdown += f"  {prefix}{nested_text}\n"
    
    return markdown


def process_pre_element(pre):
    """Process pre/code block"""
    code = pre.find('code')
    if code:
        code_text = code.get_text()
        # Determine language
        lang = 'powershell'
        classes = code.get('class', [])
        for cls in classes:
            if 'language-' in cls:
                lang = cls.replace('language-', '')
                break
            elif cls in ['bash', 'powershell', 'shell', 'cmd', 'python', 'javascript', 'source']:
                if cls == 'source':
                    lang = 'powershell'
                else:
                    lang = cls
        return f"```{lang}\n{code_text}\n```"
    return ""


def extract_sections():
    """Extract all sections from HTML file"""
    print(f"Reading HTML file: {HTML_FILE}")
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find body
    body = soup.find('div', class_='page-body')
    if not body:
        print("Warning: Could not find page-body")
        return {}
    
    # Extract sections using the toggle structure
    sections = find_all_details_sections(body)
    
    return sections


def generate_markdown_file(title, content, filename):
    """Generate a markdown file with front matter"""
    # Convert content to markdown
    markdown = html_to_markdown(content)
    
    # Create front matter
    front_matter = f"""---
title: {title}
layout: docs
---

"""
    
    # Write file
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(front_matter + markdown)
    
    print(f"Generated: {filename}")


def main():
    """Main function"""
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Process images first
    print("\n=== Processing Images ===")
    process_images()
    
    # Extract sections
    print("\n=== Extracting Sections ===")
    sections = extract_sections()
    
    print(f"\nFound {len(sections)} sections")
    
    # Generate markdown files
    print("\n=== Generating Markdown Files ===")
    for title, content in sections.items():
        if title in SECTION_MAP:
            filename = SECTION_MAP[title]
            generate_markdown_file(title, content, filename)
    
    # Check for missing sections
    print("\n=== Summary ===")
    print(f"Sections found: {len(sections)}")
    print(f"Expected: {len(SECTION_MAP)}")
    
    missing = set(SECTION_MAP.keys()) - set(sections.keys())
    if missing:
        print(f"Missing sections: {missing}")
    else:
        print("All sections found!")


if __name__ == "__main__":
    main()
