#!/usr/bin/env python3
import re
import os

SOURCE_HTML = "/home/stark/Downloads/NetExec/extracted/netexec-export/LeHACK2025 CTF 30b79e9ad7c980878d4dc276cc75f665.html"
OUTPUT_FILE = "/home/stark/mr-stark-study-notes/ctf/netexec-labs/lehack2025-ctf/index.html"
ASSETS_PATH = "/home/stark/mr-stark-study-notes/assets/ctf/lehack2025-ctf"

SIDEBAR_NAV = """          <a href="../../" class="portfolio-link">← Home</a>
          <a href="../../../ctf/" class="portfolio-link">← CTFs</a>
          <a href="../../" class="portfolio-link">← NetExec Labs</a>
          <h3>Sections</h3>
          <a href="#introduction" class="">Introduction</a>
          <a href="#setting-up-etc-hosts-kerberos" class="">Setting up /etc/hosts & Kerberos</a>
          <a href="#setting-up-fqdn" class="">Setting up FQDN</a>
          <a href="#dnsmasq" class="">DNSMASQ</a>
          <a href="#enumerate-null-session" class="">Enumerate Null Session</a>
          <a href="#enumerate-guest-logon" class="">Enumerate Guest Logon</a>
          <a href="#scan-for-vulnerabilities" class="">Scan for Vulnerabilities</a>
          <a href="#smbghost" class="">SmbGhost</a>
          <a href="#network-level-authentication-nla" class="">Network Level Authentication (NLA)</a>
          <a href="#asrep-roasting-attack" class="">ASREP-Roasting Attack</a>
          <a href="#kerberoasting-attack-without-pre-auth" class="">Kerberoasting Without Pre-Auth</a>
          <a href="#kerberoasting-attack-with-auth" class="">Kerberoasting Attack With Auth</a>
          <a href="#spidering-shares" class="">Spidering Shares</a>
          <a href="#password-spraying" class="">Password Spraying</a>
          <a href="#mssql-abuse-trust-links" class="">MSSQL Abuse - Trust Links</a>
          <a href="#basic-enumeration-via-trust-links" class="">Basic Enumeration via Trust Links</a>
          <a href="#pre-created-computer-accounts" class="">Pre-Created Computer Accounts</a>
          <a href="#gmsa-abuse" class="">gMSA Abuse</a>
          <a href="#certificate-authentication-pfx" class="">Certificate Auth (PFX)</a>
          <a href="#dumping-lsa-hashes" class="">Dumping LSA Hashes</a>
          <a href="#backup-operators-abuse" class="">Backup Operators Abuse</a>
          <a href="#domain-admin-to-empire" class="">Domain Admin to empire.local</a>
"""

HTML_TEMPLATE = r"""---
title: LeHACK 2025 CTF
layout: docs
---

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>LeHACK 2025 CTF - Mr Stark</title>
  <link rel="shortcut icon" href="../../../assets/images/logo.ico" type="image/x-icon">
  <link rel="stylesheet" href="../../../assets/css/style.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
  <style>
    .ctf-sidebar { padding: 20px; }
    .ctf-sidebar h3 { color: #ffdb70; margin-bottom: 15px; font-size: 1.1rem; }
    .ctf-sidebar .portfolio-link { 
      display: block; 
      padding: 10px 12px; 
      margin-bottom: 10px; 
      color: #ffdb70; 
      text-decoration: none; 
      border-radius: 6px; 
      font-size: 0.9rem; 
      font-weight: 600;
      background: #2a2a2a;
      transition: all 0.2s;
    }
    .ctf-sidebar .portfolio-link:hover { 
      background: #ffdb70; 
      color: #1a1a1a; 
    }
    .ctf-sidebar a { display: block; padding: 8px 12px; margin: 4px 0; color: #d6d6d6; text-decoration: none; border-radius: 6px; font-size: 0.9rem; transition: all 0.2s; }
    .ctf-sidebar a:hover { background: #2a2a2a; color: #ffdb70; }
    .ctf-sidebar a.active { background: #ffdb70; color: #1a1a1a; font-weight: 600; }
    .page-nav { display: flex; justify-content: space-between; margin: 30px 0; padding: 20px 0; border-top: 1px solid #2a2a2a; }
    .nav-btn { background: #2a2a2a; color: #ffdb70; padding: 10px 20px; border-radius: 6px; text-decoration: none; transition: all 0.2s; }
    .nav-btn:hover { background: #ffdb70; color: #1a1a1a; }
    .notion-content { line-height: 1.6; }
    .notion-content img { max-width: 100%; height: auto; margin: 20px 0; border-radius: 8px; }
    .notion-content h1 { font-size: 1.8rem; margin: 30px 0 20px; color: #fafafa; border-bottom: 2px solid #ffdb70; padding-bottom: 10px; }
    .notion-content h2 { font-size: 1.5rem; margin: 25px 0 15px; color: #fafafa; }
    .notion-content h3 { font-size: 1.3rem; margin: 20px 0 10px; color: #fafafa; }
    .notion-content p { margin: 15px 0; color: #d6d6d6; }
    .notion-content ul, .notion-content ol { margin: 15px 0; padding-left: 30px; }
    .notion-content li { margin: 5px 0; color: #d6d6d6; }
    .notion-content code { background: #2a2a2a; padding: 2px 6px; border-radius: 4px; font-family: 'Courier New', monospace; color: #ffdb70; }
    .notion-content pre { background: #1e1e1e; border-left: 4px solid #ffdb70; padding: 15px; margin: 20px 0; border-radius: 0 8px 8px 0; overflow-x: auto; }
    .notion-content pre code { background: transparent; padding: 0; color: #d6d6d6; }
    .notion-content a { color: #ffdb70; text-decoration: underline; }
    .notion-content strong { color: #fafafa; font-weight: 600; }
    .notion-content figure { margin: 20px 0; }
    .notion-content figcaption { display: none; }
    .main-content { max-width: 100% !important; }
    .about { max-width: 100% !important; padding: 20px 40px !important; }
    .machine-summary { background: #2a2a2a; border: 2px solid #ffdb70; border-radius: 10px; padding: 20px; margin-bottom: 30px; }
    .machine-summary h3 { color: #ffdb70; margin: 0 0 15px 0; font-size: 1.2rem; }
    .machine-summary .summary-item { display: flex; margin: 8px 0; }
    .machine-summary .summary-label { color: #ffdb70; font-weight: 600; min-width: 120px; }
    .machine-summary .summary-value { color: #d6d6d6; }
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
          <p class="title">LeHACK 2025 CTF</p>
        </div>
        <button class="info_more-btn" data-sidebar-btn>
          <span>Show Navigation</span>
          <ion-icon name="chevron-down"></ion-icon>
        </button>
      </div>
      <div class="sidebar-info_more">
        <div class="separator"></div>
        <div class="ctf-sidebar">
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
              <a href="../../" class="contact-link">NetExec Labs</a>
            </div>
          </li>
        </ul>
        <div class="separator"></div>
        <ul class="social-list">
          <li class="social-item">
            <a href="https://github.com/daviosardinha/mr-stark-study-notes" class="social-link" target="_blank">
              <ion-icon name="logo-github"></ion-icon>
            </a>
          </li>
        </ul>
      </div>
    </aside>

    <div class="main-content">
      <article class="about active" data-page="about">
        <header class="h2 article-title">LeHACK 2025 CTF</header>
        <section class="about-text">
          <div class="machine-summary">
            <h3>Machine Summary</h3>
            <div class="summary-item">
              <span class="summary-label">Machine:</span>
              <span class="summary-value">LeHACK 2025</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Category:</span>
              <span class="summary-value">Active Directory</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Platform:</span>
              <span class="summary-value">CTF</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Difficulty:</span>
              <span class="summary-value">Expert</span>
            </div>
          </div>
          <div class="notion-content">
{CONTENT}
          </div>
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

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def process_html():
    with open(SOURCE_HTML, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Find the article body content
    body_match = re.search(r'<div class="page-body">(.*)</div>\s*</article>', html, re.DOTALL)
    if not body_match:
        print("Could not find page body")
        return ""
    
    content = body_match.group(1)
    
    # Remove the first image (hero) from content - we'll add it manually
    content = re.sub(r'<div style="display:contents" dir="ltr"><figure[^>]*>.*?</figure></div>', '', content, count=1)
    
    # Process h1 elements - convert to h2 with anchor IDs
    def replace_h1(match):
        h1_id = match.group(1)
        title = match.group(2)
        slug = slugify(title)
        return f'<h2 id="{slug}" class="">{title}</h2>'
    
    content = re.sub(r'<h1 id="([0-9a-f-]+)"[^>]*>(.*?)</h1>', replace_h1, content)
    
    # Process h3 elements - keep them but clean up
    def replace_h3(match):
        title = match.group(1)
        return f'<h3>{title}</h3>'
    
    content = re.sub(r'<h3 id="[0-9a-f-]+"[^>]*>(.*?)</h3>', replace_h3, content)
    
    # Remove Notion-specific wrappers
    content = re.sub(r'<div style="display:contents"[^>]*>', '', content)
    content = re.sub(r'</div>', '', content)
    
    # Clean up figure elements - keep img but remove wrapper
    content = re.sub(r'<figure[^>]*>\s*<a href="([^"]+)"><img[^>]*src="([^"]+)"[^>]*/></a>\s*</figure>', 
                     r'<img src="\2" alt="Image"/>', content)
    
    # Clean up standalone images
    content = re.sub(r'<figure[^>]*>\s*<img[^>]*src="([^"]+)"[^>]*/>\s*</figure>', 
                     r'<img src="\1" alt="Image"/>', content)
    
    # Fix image paths - convert LeHACK2025 CTF/image.png to /assets/ctf/lehack2025-ctf/image.png
    content = re.sub(r'src="LeHACK2025%20CTF/([^"]+)"', r'src="../../../assets/ctf/lehack2025-ctf/\1"', content)
    content = re.sub(r'src="LeHACK2025 CTF/([^"]+)"', r'src="../../../assets/ctf/lehack2025-ctf/\1"', content)
    
    # Clean up code blocks
    content = re.sub(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', 
                     r'<pre><code>\1</code></pre>', content, flags=re.DOTALL)
    
    # Remove prism.js and prism.css references
    content = re.sub(r'<script[^>]*prism[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<link[^>]*prism[^>]*>', '', content)
    
    # Clean up empty paragraphs
    content = re.sub(r'<p[^>]*>\s*</p>', '', content)
    
    # Clean up bulleted and numbered lists
    content = re.sub(r'<ul[^>]*class="bulleted-list"[^>]*>', r'<ul>', content)
    content = re.sub(r'<ol[^>]*class="numbered-list"[^>]*>', r'<ol>', content)
    content = re.sub(r'<li[^>]*style="[^"]*"[^>]*>', r'<li>', content)
    
    return content

def main():
    content = process_html()
    
    # Generate final HTML
    final_html = HTML_TEMPLATE.replace("{SIDEBAR}", SIDEBAR_NAV).replace("{CONTENT}", content)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"Created: {OUTPUT_FILE}")
    
    # Count images
    img_count = content.count('<img src=')
    print(f"Images embedded: {img_count}")

if __name__ == "__main__":
    main()
