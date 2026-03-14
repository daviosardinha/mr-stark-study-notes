#!/usr/bin/env python3
import re
import os
import html

SOURCE_HTML = "/home/stark/Downloads/CRTE/extracted/crte-export/CRTE - Certified Red Team Expert 30c79e9ad7c980c28933e21c73f4f769.html"
CRTE_DIR = "/home/stark/mr-stark-study-notes/certifications/crte"
ASSETS_DIR = "/home/stark/mr-stark-study-notes/assets/crte"

SECTIONS = [
    ("part-01-introduction.html", "Introduction", "introduction"),
    ("part-02-enumeration.html", "Enumeration", "enumeration"),
    ("part-03-enumerating-gpos-ous.html", "Enumerating GPOs and OUs", "enumerating-gpos-ous"),
    ("part-04-enumerating-acl.html", "Enumerating ACL (Access Control List)", "enumerating-acl"),
    ("part-05-enumerating-domain-forest-trusts.html", "Enumerating Domain, Forest & Trusts ", "enumerating-domain-forest-trusts"),
    ("part-06-privilege-escalation.html", "Privilege Escalation", "privilege-escalation"),
    ("part-07-kerberoasting-attack.html", "Kerberoasting attack", "kerberoasting-attack"),
    ("part-08-targeted-kerberoasting.html", "Privilege Escalation - Targeted Kerberoasting", "targeted-kerberoasting"),
    ("part-09-laps-attack.html", "Privilege Escalation - LAPS (Local Administrator Password Solution) Attack", "laps-attack"),
    ("part-10-dumping-lsass-credentials.html", "Dumping LSASS Credentials", "dumping-lsass-credentials"),
    ("part-11-gmsa-attack.html", "Privilege Escalation - gMSA Attack", "gmsa-attack"),
    ("part-12-lsass-mde-bypass.html", "LSASS Attack With MDE Bypass", "lsass-mde-bypass"),
    ("part-13-pass-the-certificates.html", "Pass The Certificates Attack", "pass-the-certificates"),
    ("part-14-unconstrained-delegation.html", "Privilege Escalation - Unconstrained Delegation", "unconstrained-delegation"),
    ("part-15-constrained-delegation.html", "Privilege Escalation - Constrained Delegation", "constrained-delegation"),
    ("part-16-rbcd.html", "Privilege Escalation - RBCD(Resource Based Constrained Delegation)", "rbcd"),
    ("part-17-golden-ticket.html", "Domain Persistence - Golden Ticket attack", "golden-ticket"),
    ("part-18-silver-ticket.html", "Domain Persistence - Silver Ticket Attack", "silver-ticket"),
    ("part-19-diamond-ticket.html", "Domain Persistence - Diamond Ticket Attack", "diamond-ticket"),
    ("part-20-skeleton-key.html", "Domain Persistence - Skeleton Key Attack", "skeleton-key"),
    ("part-21-sapphire-ticket.html", "Domain Persistence - Sapphire Ticket Attack", "sapphire-ticket"),
    ("part-22-adminsdholder.html", "Domain Persistence - AdminSDHolder attack", "adminsdholder"),
    ("part-23-adcs-attacks.html", "Cross Domain Attacks - Active Directory Certificate Services Attacks", "adcs-attacks"),
    ("part-24-shadow-credentials.html", "Shadow Credentials - Abusing User Object", "shadow-credentials"),
    ("part-25-cross-domain-unconstrained.html", "Cross Domain Attacks - Unconstrained Delegation to Enterprise Admin", "cross-domain-unconstrained"),
    ("part-26-azure-ad-phs.html", "Cross Domain Attacks - Attacking Azure AD Integration PHS", "azure-ad-phs"),
    ("part-27-child-to-forest-trust-key.html", "Cross Domain attacks - Child To Forest Root - SID-History Trust Key Abuse", "child-to-forest-trust-key"),
    ("part-28-child-to-forest-sidhistory-krbtgt.html", "Cross Domain attacks - Child To Forest Root - SID-History KRBTGT Hash Abuse", "child-to-forest-sidhistory-krbtgt"),
    ("part-29-cross-forest-kerberoast.html", "Cross Forest Attacks - Kerberoast Attack", "cross-forest-kerberoast"),
    ("part-30-protocol-transition.html", "Cross Forest Attacks - Constrained Delegation with Protocol Transition", "protocol-transition"),
    ("part-31-cross-forest-unconstrained.html", "Cross Forest Attacks - Unconstrained Delegation", "cross-forest-unconstrained"),
    ("part-32-trust-key-shared-resources.html", "Cross Forest Attacks - Trust Key Abuse to Access Explicitly Shared Resources", "trust-key-shared-resources"),
    ("part-33-injecting-sidhistory.html", "Cross Forest Attacks - Injecting SID History to Bypass SID Filtering", "injecting-sidhistory"),
    ("part-34-mssql-database-links.html", "Trust Abuse - MSSQL Servers - Database Links", "mssql-database-links"),
    ("part-35-foreign-security-principals.html", "Cross Forest Attacks - Foreign Security Principals & ACLs", "foreign-security-principals"),
    ("part-36-pam-shadow-security-principals.html", "Cross Forest Attacks - Abusing PAM(Privileged Management Principals) Trust - Shadow Security Principals", "pam-shadow-security-principals"),
    ("part-37-trusting-to-trusted.html", "Cross Forest Attacks - Trusting to Trusted - Trust Key", "trusting-to-trusted"),
    ("part-38-abusing-trust-transitivity.html", "Cross Forest Attacks - Abusing Trust Transitivity", "abusing-trust-transitivity"),
]

SIDEBAR_TEMPLATE = """          <a href="../../" class="portfolio-link">← Portfolio</a>
          <h3>Sections</h3>
          <a href="overview.html" class="">Overview</a>
"""

for filename, title, anchor in SECTIONS:
    SIDEBAR_TEMPLATE += f'\n          <a href="{filename}" class="">{title}</a>'

PAGE_TEMPLATE = """---
title: {title}
layout: docs
---

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} - CRTE</title>
  <link rel="shortcut icon" href="../../../assets/images/logo.ico" type="image/x-icon">
  <link rel="stylesheet" href="../../../assets/css/style.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
  <style>
    .crtp-sidebar {{ padding: 20px; }}
    .crtp-sidebar h3 {{ color: #ffdb70; margin-bottom: 15px; font-size: 1.1rem; }}
    .crtp-sidebar .portfolio-link {{ 
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
    .crtp-sidebar .portfolio-link:hover {{ 
      background: #ffdb70; 
      color: #1a1a1a; 
    }}
    .crtp-sidebar a {{ display: block; padding: 8px 12px; margin: 4px 0; color: #d6d6d6; text-decoration: none; border-radius: 6px; font-size: 0.9rem; transition: all 0.2s; }}
    .crtp-sidebar a:hover {{ background: #2a2a2a; color: #ffdb70; }}
    .crtp-sidebar a.active {{ background: #ffdb70; color: #1a1a1a; font-weight: 600; }}
    .main-content {{ max-width: 100% !important; }}
    .about {{ max-width: 100% !important; padding: 20px 40px !important; }}
    .notion-content {{ line-height: 1.6; }}
    .notion-content img {{ max-width: 100%; height: auto; margin: 20px 0; border-radius: 8px; }}
    .notion-content h1, .notion-content h2, .notion-content h3 {{ color: #fafafa; margin: 20px 0 10px; }}
    .notion-content p {{ margin: 15px 0; color: #d6d6d6; }}
    .notion-content ul, .notion-content ol {{ margin: 15px 0; padding-left: 30px; }}
    .notion-content li {{ margin: 5px 0; color: #d6d6d6; }}
    .notion-content code {{ background: #2a2a2a; padding: 2px 6px; border-radius: 4px; font-family: 'Courier New', monospace; color: #ffdb70; }}
    .notion-content pre {{ background: #1e1e1e; border-left: 4px solid #ffdb70; padding: 15px; margin: 20px 0; border-radius: 0 8px 8px 0; overflow-x: auto; }}
    .notion-content a {{ color: #ffdb70; text-decoration: underline; }}
    .notion-content strong {{ color: #fafafa; font-weight: 600; }}
  </style>
</head>
<body>
  <main>
    <aside class="sidebar" data-sidebar>
      <div class="sidebar-info">
        <figure class="avatar-box">
          <img src="../../../assets/images/my-avatar.png?v=3" alt="Mr Stark" width="80">
        </figure>
        <div class="info-content">
          <h1 class="name" title="Mr Stark">Mr Stark</h1>
          <p class="title">CRTE Study Notes</p>
        </div>
        <button class="info_more-btn" data-sidebar-btn>
          <span>Show Navigation</span>
          <ion-icon name="chevron-down"></ion-icon>
        </button>
      </div>
      <div class="sidebar-info_more">
        <div class="separator"></div>
        <div class="crtp-sidebar">
{SIDEBAR}
        </div>
        <div class="separator"></div>
        <ul class="contacts-list">
          <li class="contact-item">
            <div class="icon-box">
              <ion-icon name="arrow-back-outline"></ion-icon>
            </div>
            <div class="contact-info">
              <p class="contact-title">Back</p>
              <a href="../../../" class="contact-link">Portfolio</a>
            </div>
          </li>
        </ul>
      </div>
    </aside>

    <div class="main-content">
      <article class="about active" data-page="about">
        <header class="h2 article-title">{title}</header>
        <section class="about-text notion-content">
{CONTENT}
        </section>
      </article>
    </div>
  </main>

  <script src="../../../assets/js/script.js"></script>
  <script type="module" src="https://unpkg.com/ionicons@5.5.2/dist/ionicons/ionicons.esm.js"></script>
  <script nomodule src="https://unpkg.com/ionicons@5.5.2/dist/ionicons/ionicons.js"></script>
</body>
</html>
"""

def clean_content(content):
    content = re.sub(r'<div style="display:contents"[^>]*>', '', content)
    content = re.sub(r'</div>', '', content)
    content = re.sub(r'<figure[^>]*>\s*<a href="([^"]+)"><img[^>]*src="([^"]+)"[^>]*/></a>\s*</figure>', 
                     r'<img src="../../../assets/crte/\1" alt="Image"/>', content)
    content = re.sub(r'src="CRTE%20-%20Certified%20Red%20Team%20Expert/([^"]+)"', 
                     r'src="../../../assets/crte/\1"', content)
    content = re.sub(r'src="CRTE - Certified Red Team Expert/([^"]+)"', 
                     r'src="../../../assets/crte/\1"', content)
    content = re.sub(r'<script[^>]*prism[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<link[^>]*prism[^>]*>', '', content)
    content = re.sub(r'<p[^>]*>\s*</p>', '', content)
    content = re.sub(r'<ul[^>]*class="bulleted-list"[^>]*>', r'<ul>', content)
    content = re.sub(r'<ol[^>]*class="numbered-list"[^>]*>', r'<ol>', content)
    content = re.sub(r'<li[^>]*style="[^"]*"[^>]*>', r'<li>', content)
    return content

def extract_toggle_sections(html_content):
    pattern = r'<ul[^>]*class="toggle"[^>]*><li><details[^>]*><summary><strong>([^<]+)</strong></summary>(.*?)</details></li></ul>'
    matches = re.findall(pattern, html_content, re.DOTALL)
    return matches

def get_section_title(content):
    # Extract title from summary
    match = re.search(r'<summary><strong>([^<]+)</strong></summary>', content)
    if match:
        return match.group(1)
    return None

def main():
    with open(SOURCE_HTML, 'r', encoding='utf-8') as f:
        html = f.read()
    
    body_match = re.search(r'<div class="page-body">(.*?)</div>\s*</article>', html, re.DOTALL)
    if not body_match:
        print("Could not find page body")
        return
    
    content = body_match.group(1)
    
    sections = extract_toggle_sections(content)
    print(f"Found {len(sections)} sections in content")
    
    for title, section_content in sections[:10]:
        print(f"  - {title[:50]}...")
    
    import html as html_module
    
    title_to_filename = {}
    for filename, t, anchor in SECTIONS:
        title_to_filename[t] = filename
        title_to_filename[t.strip()] = filename
        title_to_filename[t.rstrip()] = filename
        title_to_filename[html_module.unescape(t)] = filename
    
    for title, section_content in sections:
        title_unescaped = html_module.unescape(title)
        filename = title_to_filename.get(title) or title_to_filename.get(title_unescaped) or title_to_filename.get(title.strip()) or title_to_filename.get(title.rstrip())
        if not filename:
            print(f"Warning: No mapping for section '{title}'")
            continue
        
        section_content = clean_content(section_content)
        
        sidebar = f"""          <a href="../../" class="portfolio-link">← Portfolio</a>
          <h3>Sections</h3>
          <a href="overview.html" class="">Overview</a>
"""
        for fname, t, anchor in SECTIONS:
            active_class = 'active' if fname == filename else ''
            sidebar += f'\n          <a href="{fname}" class="{active_class}">{t}</a>'
        
        page = PAGE_TEMPLATE.format(
            title=title,
            SIDEBAR=sidebar,
            CONTENT=section_content
        )
        
        filepath = os.path.join(CRTE_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(page)
        print(f"Generated: {filename}")

if __name__ == "__main__":
    main()
