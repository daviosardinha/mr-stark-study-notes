#!/usr/bin/env python3
"""
CRTP Migration - Re-extract with images
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

# Section mapping
SECTION_MAP = {
    "Enumeration": "enumeration.html",
    "Privilege Escalation": "privilege-escalation.html",
    "Privilege Escalation via Domain Admin session": "privilege-escalation-domain-admin.html",
    "Golden Ticket": "golden-ticket.html",
    "Silver Ticket": "silver-ticket.html",
    "Diamond Ticket": "diamond-ticket.html",
    "Abusing DSRM Credentials": "abusing-dsrm-credentials.html",
    "DCSync Attack": "dcsync-attack.html",
    "Security Descriptor Abuse": "security-descriptor-abuse.html",
    "ASREP-Roasting Attack": "asrep-roasting.html",
    "Unconstrained Delegation": "unconstrained-delegation.html",
    "Constrained Delegation": "constrained-delegation.html",
    "Resource-Based Constrained Delegation (RBCD)": "rbcd.html",
    "Enterprise Admins Trust - SID-History Abuse with Trust Ticket": "sid-history-trust-ticket.html",
    "Enterprise Admin Trust - SID-History Abuse with KRBTGT hash": "sid-history-krbtgt.html",
    "CrossForest Trust - Trust Flow": "cross-forest-trust.html",
    "ADCS Attacks": "adcs-attacks.html",
    "Trust Links Abuse": "trust-links-abuse.html",
    "MDE/MDI Bypass": "mde-mdi-bypass.html",
}


def extract_summary_title(details):
    """Extract title from details/summary tag"""
    summary = details.find('summary')
    if summary:
        title = summary.get_text()
        title = re.sub(r'\s+', ' ', title).strip()
        return title
    return None


def extract_details_content(details):
    """Extract all content inside details tag after the summary"""
    content_parts = []
    summary = details.find('summary')
    if summary:
        for sibling in summary.find_next_siblings():
            content_parts.append(str(sibling))
    return ''.join(content_parts)


def find_all_details_sections(body):
    """Find all top-level details sections in the body"""
    sections = {}
    
    toggle_uls = body.find_all('ul', class_='toggle')
    
    for ul in toggle_uls:
        for li in ul.find_all('li', recursive=False):
            details = li.find('details', recursive=False)
            if details:
                title = extract_summary_title(details)
                if title and title in SECTION_MAP:
                    content = extract_details_content(details)
                    if len(content) > 50:
                        sections[title] = content
                        print(f"Found section: {title} ({len(content)} chars)")
    
    return sections


def convert_to_html(html_content):
    """Convert HTML content to clean HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove unwanted tags
    for tag in soup(['style', 'script', 'figcaption', 'mark']):
        tag.decompose()
    
    # Remove display:contents divs and unwrap divs
    for tag in soup.find_all('div'):
        style = tag.get('style', '')
        if 'display:contents' in str(style):
            tag.unwrap()
        elif not tag.get('class') and not tag.contents:
            tag.decompose()
        else:
            tag.unwrap()
    
    # Process images - fix src paths
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if src and not src.startswith('http'):
            # Extract filename from path like "CRTP%20-%20Certified%20Red%20Team%20Professional/Untitled%201.png"
            filename = os.path.basename(urllib.parse.unquote(src))
            img['src'] = f"../../assets/crtp/{filename}"
        
        # Remove style attributes
        if img.get('style'):
            del img['style']
        if img.get('width'):
            del img['width']
    
    # Remove figure tags but keep content
    for figure in soup.find_all('figure'):
        figure.unwrap()
    
    # Process anchor tags wrapping images
    for a in soup.find_all('a'):
        href = a.get('href', '')
        if href and not href.startswith('http') and not href.startswith('#'):
            filename = os.path.basename(urllib.parse.unquote(href))
            a['href'] = f"../../assets/crtp/{filename}"
    
    # Clean up strong tags that are just for bold
    for strong in soup.find_all('strong'):
        if not strong.contents:
            strong.decompose()
    
    return str(soup)


def get_template(title, content, current_file):
    """Generate HTML with vCard template"""
    
    # Build navigation links
    nav_links = ""
    for idx, (filename, section_title) in enumerate(SECTION_MAP.items()):
        active = "active" if filename == current_file else ""
        nav_links += f'          <a href="{filename}" class="{active}">{section_title}</a>\n'
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} - CRTP</title>
  <link rel="shortcut icon" href="../../assets/images/logo.ico" type="image/x-icon">
  <link rel="stylesheet" href="../../assets/css/style.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
  <style>
    .crtp-sidebar {{ padding: 20px; }}
    .crtp-sidebar h3 {{ color: #ffdb70; margin-bottom: 15px; font-size: 1.1rem; }}
    .crtp-sidebar .home-link {{ 
      display: block; 
      padding: 10px 12px; 
      margin-bottom: 15px; 
      color: #ffdb70; 
      text-decoration: none; 
      border-radius: 6px; 
      font-size: 0.9rem; 
      font-weight: 600;
      background: #2a2a2a;
      transition: all 0.2s;
    }}
    .crtp-sidebar .home-link:hover {{ 
      background: #ffdb70; 
      color: #1a1a1a; 
    }}
    .crtp-sidebar a {{ display: block; padding: 8px 12px; margin: 4px 0; color: #d6d6d6; text-decoration: none; border-radius: 6px; font-size: 0.9rem; transition: all 0.2s; }}
    .crtp-sidebar a:hover {{ background: #2a2a2a; color: #ffdb70; }}
    .crtp-sidebar a.active {{ background: #ffdb70; color: #1a1a1a; font-weight: 600; }}
    .page-nav {{ display: flex; justify-content: space-between; margin: 30px 0; padding: 20px 0; border-top: 1px solid #2a2a2a; }}
    .nav-btn {{ background: #2a2a2a; color: #ffdb70; padding: 10px 20px; border-radius: 6px; text-decoration: none; transition: all 0.2s; }}
    .nav-btn:hover {{ background: #ffdb70; color: #1a1a1a; }}
    .notion-content {{ line-height: 1.6; }}
    .notion-content img {{ max-width: 100%; height: auto; margin: 20px 0; border-radius: 8px; }}
    .notion-content h1 {{ font-size: 1.8rem; margin: 30px 0 20px; color: #fafafa; }}
    .notion-content h2 {{ font-size: 1.5rem; margin: 25px 0 15px; color: #fafafa; }}
    .notion-content h3 {{ font-size: 1.3rem; margin: 20px 0 10px; color: #fafafa; }}
    .notion-content p {{ margin: 15px 0; color: #d6d6d6; }}
    .notion-content ul, .notion-content ol {{ margin: 15px 0; padding-left: 30px; }}
    .notion-content li {{ margin: 5px 0; color: #d6d6d6; }}
    .notion-content code {{ background: #2a2a2a; padding: 2px 6px; border-radius: 4px; font-family: 'Courier New', monospace; color: #ffdb70; }}
    .notion-content pre {{ background: #1e1e1e; border-left: 4px solid #ffdb70; padding: 15px; margin: 20px 0; border-radius: 0 8px 8px 0; overflow-x: auto; }}
    .notion-content pre code {{ background: transparent; padding: 0; color: #d6d6d6; }}
    .notion-content a {{ color: #ffdb70; text-decoration: underline; }}
    .notion-content strong {{ color: #fafafa; font-weight: 600; }}
    .notion-content em {{ font-style: italic; }}
    .notion-content figure {{ margin: 20px 0; }}
    .notion-content figcaption {{ display: none; }}
    .main-content {{ max-width: 100% !important; }}
    .about {{ max-width: 100% !important; padding: 20px 40px !important; }}
  </style>
</head>
<body>
  <main>
    <aside class="sidebar" data-sidebar>
      <div class="sidebar-info">
        <figure class="avatar-box">
          <img src="../../assets/images/my-avatar.png?v=3" alt="Mr Stark" width="80">
        </figure>
        <div class="info-content">
          <h1 class="name" title="Mr Stark">Mr Stark</h1>
          <p class="title">CRTP Study Notes</p>
        </div>
        <button class="info_more-btn" data-sidebar-btn>
          <span>Show Navigation</span>
          <ion-icon name="chevron-down"></ion-icon>
        </button>
      </div>
      <div class="sidebar-info_more">
        <div class="separator"></div>
        <div class="crtp-sidebar">
          <a href="../../" class="home-link">← Home</a>
          <a href="../../certifications/" class="home-link">← Certifications</a>
          <h3>Sections</h3>
{nav_links}
        </div>
        <div class="separator"></div>
        <ul class="contacts-list">
          <li class="contact-item">
            <div class="icon-box">
              <ion-icon name="mail-outline"></ion-icon>
            </div>
            <div class="contact-info">
              <p class="contact-title">Email</p>
              <a href="mailto:daviosardinha@gmail.com" class="contact-link">daviosardinha@gmail.com</a>
            </div>
          </li>
        </ul>
      </div>
    </aside>

    <div class="main-content">
      <article class="about active" data-page="about">
        <header class="h2 article-title">{title}</header>
        <section class="about-text">
          <div class="notion-content">
{content}
          </div>
        </section>
      </article>
    </div>
  </main>

  <script src="../../assets/js/script.js"></script>
  <script type="module" src="https://unpkg.com/ionicons@5.5.2/dist/ionicons/ionicons.esm.js"></script>
  <script nomodule src="https://unpkg.com/ionicons@5.5.2/dist/ionicons/ionicons.js"></script>
</body>
</html>'''
    return html


def extract_sections():
    """Extract all sections from HTML file"""
    print(f"Reading HTML file: {HTML_FILE}")
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    body = soup.find('div', class_='page-body')
    if not body:
        print("Warning: Could not find page-body")
        return {}
    
    sections = find_all_details_sections(body)
    
    return sections


def main():
    """Main function"""
    # Ensure images are in place
    print("\n=== Verifying Images ===")
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR, exist_ok=True)
        # Copy images
        for f in os.listdir(IMAGE_DIR):
            if f.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                shutil.copy2(os.path.join(IMAGE_DIR, f), ASSETS_DIR)
        print(f"Images copied to {ASSETS_DIR}")
    else:
        print(f"Images already exist in {ASSETS_DIR}")
    
    # Extract sections
    print("\n=== Extracting Sections ===")
    sections = extract_sections()
    
    print(f"\nFound {len(sections)} sections")
    
    # Generate HTML files
    print("\n=== Generating HTML Files ===")
    for title, content in sections.items():
        if title in SECTION_MAP:
            filename = SECTION_MAP[title]
            
            # Convert content to clean HTML with images
            html_content = convert_to_html(content)
            
            # Generate full HTML with template
            output_html = get_template(title, html_content, filename)
            
            # Write file
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(output_html)
            
            print(f"Generated: {filename}")
    
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
