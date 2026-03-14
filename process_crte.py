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
    ("part-03-privilege-escalation.html", "Privilege Escalation", "privilege-escalation"),
    ("part-04-kerberoasting-attack.html", "Kerberoasting attack", "kerberoasting-attack"),
    ("part-05-targeted-kerberoasting.html", "Privilege Escalation - Targeted Kerberoasting", "targeted-kerberoasting"),
    ("part-06-laps-attack.html", "Privilege Escalation - LAPS Attack", "laps-attack"),
    ("part-07-dumping-lsass-credentials.html", "Dumping LSASS Credentials", "dumping-lsass-credentials"),
    ("part-08-gmsa-attack.html", "Privilege Escalation - gMSA Attack", "gmsa-attack"),
    ("part-09-lsass-mde-bypass.html", "LSASS Attack With MDE Bypass", "lsass-mde-bypass"),
    ("part-10-pass-the-certificates-attack.html", "Pass The Certificates Attack", "pass-the-certificates-attack"),
    ("part-11-unconstrained-delegation.html", "Privilege Escalation - Unconstrained Delegation", "unconstrained-delegation"),
    ("part-12-constrained-delegation.html", "Privilege Escalation - Constrained Delegation", "constrained-delegation"),
    ("part-13-rbcd.html", "Privilege Escalation - RBCD", "rbcd"),
    ("part-14-golden-ticket.html", "Domain Persistence - Golden Ticket attack", "golden-ticket"),
    ("part-15-silver-ticket.html", "Domain Persistence - Silver Ticket Attack", "silver-ticket"),
    ("part-16-diamond-ticket.html", "Domain Persistence - Diamond Ticket Attack", "diamond-ticket"),
    ("part-17-skeleton-key.html", "Domain Persistence - Skeleton Key Attack", "skeleton-key"),
    ("part-18-sapphire-ticket.html", "Domain Persistence - Sapphire Ticket Attack", "sapphire-ticket"),
    ("part-19-adminsdholder.html", "Domain Persistence - AdminSDHolder attack", "adminsdholder"),
    ("part-20-adcs-attacks.html", "Cross Domain Attacks - ADCS Attacks", "adcs-attacks"),
    ("part-21-shadow-credentials.html", "Shadow Credentials - Abusing User Object", "shadow-credentials"),
    ("part-22-cross-domain-unconstrained.html", "Cross Domain Attacks - Unconstrained Delegation to Enterprise Admin", "cross-domain-unconstrained"),
    ("part-23-azure-ad-phs.html", "Cross Domain Attacks - Azure AD Integration PHS", "azure-ad-phs"),
    ("part-24-child-to-forest-trust-key.html", "Cross Domain Attacks - Child to Forest Root - SID History Trust Key Abuse", "child-to-forest-trust-key"),
    ("part-25-child-to-forest-sidhistory-krbtgt.html", "Cross Domain Attacks - Child to Forest Root - SID History KRBTGT Hash Abuse", "child-to-forest-sidhistory-krbtgt"),
    ("part-26-cross-forest-kerberoast.html", "Cross Forest Attacks - Kerberoast Attack", "cross-forest-kerberoast"),
    ("part-27-protocol-transition.html", "Cross Forest Attacks - Constrained Delegation with Protocol Transition", "protocol-transition"),
    ("part-28-cross-forest-unconstrained.html", "Cross Forest Attacks - Unconstrained Delegation", "cross-forest-unconstrained"),
    ("part-29-trust-key-shared-resources.html", "Cross Forest Attacks - Trust Key Abuse to Access Shared Resources", "trust-key-shared-resources"),
    ("part-30-injecting-sidhistory.html", "Cross Forest Attacks - Injecting SID History to Bypass SID Filtering", "injecting-sidhistory"),
    ("part-31-mssql-database-links.html", "Trust Abuse - MSSQL Servers Database Links", "mssql-database-links"),
    ("part-32-foreign-security-principals.html", "Cross Forest Attacks - Foreign Security Principals & ACLs", "foreign-security-principals"),
    ("part-33-pam-trust.html", "Cross Forest Attacks - Abusing PAM Trust", "pam-trust"),
    ("part-34-trusting-to-trusted.html", "Cross Forest Attacks - Trusting to Trusted - Trust Key", "trusting-to-trusted"),
    ("part-35-abusing-trust-transitivity.html", "Cross Forest Attacks - Abusing Trust Transitivity", "abusing-trust-transitivity"),
]

TITLE_MAP = {
    "Introduction": "part-01-introduction.html",
    "Enumeration": "part-02-enumeration.html",
    "Enumerating GPOs and OUs": "part-02-enumeration.html",
    "Enumerating ACL (Access Control List)": "part-02-enumeration.html",
    "Enumerating Domain, Forest & Trusts ": "part-02-enumeration.html",
    "Privilege Escalation": "part-03-privilege-escalation.html",
    "Kerberoasting attack": "part-04-kerberoasting-attack.html",
    "Privilege Escalation - Targeted Kerberoasting": "part-05-targeted-kerberoasting.html",
    "Privilege Escalation - LAPS (Local Administrator Password Solution) Attack": "part-06-laps-attack.html",
    "Dumping LSASS Credentials": "part-07-dumping-lsass-credentials.html",
    "Privilege Escalation - gMSA Attack": "part-08-gmsa-attack.html",
    "LSASS Attack With MDE Bypass": "part-09-lsass-mde-bypass.html",
    "Pass The Certificates Attack": "part-10-pass-the-certificates-attack.html",
    "Privilege Escalation - Unconstrained Delegation": "part-11-unconstrained-delegation.html",
    "Privilege Escalation - Constrained Delegation": "part-12-constrained-delegation.html",
    "Privilege Escalation - RBCD(Resource Based Constrained Delegation)": "part-13-rbcd.html",
    "Domain Persistence - Golden Ticket attack": "part-14-golden-ticket.html",
    "Domain Persistence - Silver Ticket Attack": "part-15-silver-ticket.html",
    "Domain Persistence - Diamond Ticket Attack": "part-16-diamond-ticket.html",
    "Domain Persistence - Skeleton Key Attack": "part-17-skeleton-key.html",
    "Domain Persistence - Sapphire Ticket Attack": "part-18-sapphire-ticket.html",
    "Domain Persistence - AdminSDHolder attack": "part-19-adminsdholder.html",
    "Cross Domain Attacks - Active Directory Certificate Services Attacks": "part-20-adcs-attacks.html",
    "Shadow Credentials - Abusing User Object": "part-21-shadow-credentials.html",
    "Cross Domain Attacks - Unconstrained Delegation to Enterprise Admin": "part-22-cross-domain-unconstrained.html",
    "Cross Domain Attacks - Attacking Azure AD Integration PHS": "part-23-azure-ad-phs.html",
    "Cross Domain attacks - Child To Forest Root - SID-History Trust Key Abuse": "part-24-child-to-forest-trust-key.html",
    "Cross Domain attacks - Child To Forest Root - SID-History KRBTGT Hash Abuse": "part-25-child-to-forest-sidhistory-krbtgt.html",
    "Cross Forest Attacks - Kerberoast Attack": "part-26-cross-forest-kerberoast.html",
    "Cross Forest Attacks - Constrained Delegation with Protocol Transition": "part-27-protocol-transition.html",
    "Cross Forest Attacks - Unconstrained Delegation": "part-28-cross-forest-unconstrained.html",
    "Cross Forest Attacks - Trust Key Abuse to Access Explicitly Shared Resources": "part-29-trust-key-shared-resources.html",
    "Cross Forest Attacks - Injecting SID History to Bypass SID Filtering ": "part-30-injecting-sidhistory.html",
    "Trust Abuse - MSSQL Servers - Database Links": "part-31-mssql-database-links.html",
    "Cross Forest Attacks - Foreign Security Principals & ACLs": "part-32-foreign-security-principals.html",
    "Cross Forest Attacks - Abusing PAM(Privileged Management Principals) Trust - Shadow Security Principals": "part-33-pam-trust.html",
    "Cross Forest Attacks - Trusting to Trusted - Trust Key": "part-34-trusting-to-trusted.html",
    "Cross Forest Attacks - Abusing Trust Transitivity": "part-35-abusing-trust-transitivity.html",
}

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

def get_page_title(filename):
    for fname, title, anchor in SECTIONS:
        if fname == filename:
            return title
    return ""

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
    
    for title, section_content in sections[:5]:
        print(f"  - {title[:50]}...")
    
    section_content_map = {}
    import html as html_module
    for title, section_content in sections:
        title_unescaped = html_module.unescape(title)
        filename = TITLE_MAP.get(title) or TITLE_MAP.get(title_unescaped)
        if filename:
            if filename in section_content_map:
                section_content_map[filename] += section_content
            else:
                section_content_map[filename] = section_content
    
    for filename in section_content_map:
        title = get_page_title(filename)
        if not title:
            continue
        
        section_content = clean_content(section_content_map[filename])
        
        sidebar = """          <a href="../../" class="portfolio-link">← Portfolio</a>
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
    
    overview_content = '''<img src="../../../assets/crte/LabDiagram.png" alt="Lab Diagram" style="width:100%;max-width:800px;display:block;margin:20px auto;border-radius:8px;">
<img src="../../../assets/crte/All_AttackFlow.png" alt="Attack Flow" style="width:100%;max-width:800px;display:block;margin:20px auto;border-radius:8px;">

<p>The CRTE (Certified Red Team Expert) course is focused on attacking and defending Active Directory environments using an assume breach methodology. This comprehensive guide covers various advanced attack techniques used by red teams to compromise and persist in enterprise environments.</p>

<h2>Parts</h2>
<ul>
'''

for fname, title, anchor in SECTIONS:
    overview_content += f'<li><a href="{fname}">{title}</a></li>\n'

overview_content += '</ul>'

sidebar = """          <a href="../../" class="portfolio-link">← Portfolio</a>
          <h3>Sections</h3>
          <a href="overview.html" class="active">Overview</a>
"""
for fname, title, anchor in SECTIONS:
    sidebar += f'\n          <a href="{fname}" class="">{title}</a>'

overview_page = PAGE_TEMPLATE.format(
    title="CRTE - Certified Red Team Expert",
    SIDEBAR=sidebar,
    CONTENT=overview_content
)

with open(os.path.join(CRTE_DIR, "overview.html"), 'w', encoding='utf-8') as f:
    f.write(overview_page)

print("Generated overview.html")
