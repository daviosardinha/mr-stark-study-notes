#!/usr/bin/env python3
"""
Convert CRTP markdown files to HTML with vCard template
"""

import os
import re
import markdown

# Configuration
CRTP_DIR = "/home/stark/mr-stark-study-notes/certifications/crtp"

# Section mapping - filename to display title and nav order
SECTIONS = [
    ("enumeration.md", "Enumeration"),
    ("privilege-escalation.md", "Privilege Escalation"),
    ("privilege-escalation-domain-admin.md", "Privilege Escalation via Domain Admin"),
    ("golden-ticket.md", "Golden Ticket"),
    ("silver-ticket.md", "Silver Ticket"),
    ("diamond-ticket.md", "Diamond Ticket"),
    ("abusing-dsrm-credentials.md", "Abusing DSRM Credentials"),
    ("dcsync-attack.md", "DCSync Attack"),
    ("security-descriptor-abuse.md", "Security Descriptor Abuse"),
    ("asrep-roasting.md", "AS-REP Roasting"),
    ("unconstrained-delegation.md", "Unconstrained Delegation"),
    ("constrained-delegation.md", "Constrained Delegation"),
    ("rbcd.md", "RBCD"),
    ("sid-history-trust-ticket.md", "SID-History Trust Ticket"),
    ("sid-history-krbtgt.md", "SID-History KRBTGT"),
    ("cross-forest-trust.md", "Cross-Forest Trust"),
    ("adcs-attacks.md", "ADCS Attacks"),
    ("trust-links-abuse.md", "Trust Links Abuse"),
    ("mde-mdi-bypass.md", "MDE/MDI Bypass"),
]


def get_template(title, content, current_file):
    """Generate HTML with vCard template"""
    
    # Build navigation links
    nav_links = ""
    for idx, (filename, section_title) in enumerate(SECTIONS):
        active = "active" if filename == current_file else ""
        nav_links += f'          <a href="{filename.replace(".md", ".html")}" class="{active}">{section_title}</a>\n'
    
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


def convert_markdown_to_html(md_content):
    """Convert markdown to HTML"""
    # Configure markdown processor
    md = markdown.Markdown(
        extensions=['extra', 'codehilite'],
        extension_configs={
            'codehilite': {
                'css_class': 'highlight',
                'linenums': False
            }
        }
    )
    
    # Convert markdown to HTML
    html = md.convert(md_content)
    
    # Process images - fix paths
    html = html.replace('src="/assets/crtp/', 'src="../../assets/crtp/')
    html = html.replace('alt="/assets/crtp/', 'alt="../../assets/crtp/')
    
    return html


def process_markdown_files():
    """Convert all markdown files to HTML"""
    
    # Remove old markdown files after conversion
    files_to_remove = []
    
    for md_file, title in SECTIONS:
        md_path = os.path.join(CRTP_DIR, md_file)
        
        if os.path.exists(md_path):
            # Read markdown file
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip front matter
            if content.startswith('---'):
                # Find end of front matter
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    content = parts[2].strip()
            
            # Convert to HTML
            html_content = convert_markdown_to_html(content)
            
            # Generate HTML with template
            output_html = get_template(title, html_content, md_file)
            
            # Write HTML file
            html_file = md_file.replace('.md', '.html')
            html_path = os.path.join(CRTP_DIR, html_file)
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(output_html)
            
            print(f"Generated: {html_file}")
            files_to_remove.append(md_path)
    
    # Remove markdown files
    for md_path in files_to_remove:
        os.remove(md_path)
        print(f"Removed: {os.path.basename(md_path)}")


def main():
    print("Converting CRTP markdown files to HTML...")
    process_markdown_files()
    print("\nDone!")


if __name__ == "__main__":
    main()
