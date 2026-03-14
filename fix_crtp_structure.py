#!/usr/bin/env python3
import os
import re

CRTP_DIR = "/home/stark/mr-stark-study-notes/certifications/crtp"

MAPPING = {
    "enumeration.html": "part-01-enumeration.html",
    "privilege-escalation.html": "part-02-privilege-escalation.html",
    "privilege-escalation-domain-admin.html": "part-03-da-session.html",
    "golden-ticket.html": "part-04-golden-ticket.html",
    "silver-ticket.html": "part-05-silver-ticket.html",
    "diamond-ticket.html": "part-06-diamond-ticket.html",
    "abusing-dsrm-credentials.html": "part-07-dsrm-credentials.html",
    "dcsync-attack.html": "part-08-dcsync.html",
    "security-descriptor-abuse.html": "part-09-security-descriptor.html",
    "asrep-roasting.html": "part-10-asrep-roasting.html",
    "unconstrained-delegation.html": "part-11-unconstrained-delegation.html",
    "constrained-delegation.html": "part-12-constrained-delegation.html",
    "rbcd.html": "part-13-rbcd.html",
    "sid-history-trust-ticket.html": "part-14-sid-history-trust-ticket.html",
    "sid-history-krbtgt.html": "part-15-sid-history-krbtgt.html",
    "cross-forest-trust.html": "part-16-cross-forest-trust.html",
    "adcs-attacks.html": "part-17-adcs-attacks.html",
    "trust-links-abuse.html": "part-18-trust-links-abuse.html",
    "mde-mdi-bypass.html": "part-19-mde-mdi-bypass.html",
}

SIDEBAR_LINKS = """          <a href="../" class="portfolio-link">← Portfolio</a>
          <h3>Sections</h3>
          <a href="overview.html" class="">Overview</a>
          <a href="part-01-enumeration.html" class="">Part 1 – Enumeration</a>
          <a href="part-02-privilege-escalation.html" class="">Part 2 – Privilege Escalation</a>
          <a href="part-03-da-session.html" class="">Part 3 – Privilege Escalation via Domain Admin session</a>
          <a href="part-04-golden-ticket.html" class="">Part 4 – Golden Ticket</a>
          <a href="part-05-silver-ticket.html" class="">Part 5 – Silver Ticket</a>
          <a href="part-06-diamond-ticket.html" class="">Part 6 – Diamond Ticket</a>
          <a href="part-07-dsrm-credentials.html" class="">Part 7 – Abusing DSRM Credentials</a>
          <a href="part-08-dcsync.html" class="">Part 8 – DCSync Attack</a>
          <a href="part-09-security-descriptor.html" class="">Part 9 – Security Descriptor Abuse</a>
          <a href="part-10-asrep-roasting.html" class="">Part 10 – ASREP-Roasting Attack</a>
          <a href="part-11-unconstrained-delegation.html" class="">Part 11 – Unconstrained Delegation</a>
          <a href="part-12-constrained-delegation.html" class="">Part 12 – Constrained Delegation</a>
          <a href="part-13-rbcd.html" class="">Part 13 – Resource-Based Constrained Delegation (RBCD)</a>
          <a href="part-14-sid-history-trust-ticket.html" class="">Part 14 – Enterprise Admins Trust – SID-History Abuse with Trust Ticket</a>
          <a href="part-15-sid-history-krbtgt.html" class="">Part 15 – Enterprise Admin Trust – SID-History Abuse with KRBTGT hash</a>
          <a href="part-16-cross-forest-trust.html" class="">Part 16 – Cross-Forest Trust – Trust Flow</a>
          <a href="part-17-adcs-attacks.html" class="">Part 17 – ADCS Attacks</a>
          <a href="part-18-trust-links-abuse.html" class="">Part 18 – Trust Links Abuse</a>
          <a href="part-19-mde-mdi-bypass.html" class="">Part 19 – MDE / MDI Bypass</a>
"""

OVERVIEW_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Overview - CRTP</title>
  <link rel="shortcut icon" href="../../assets/images/logo.ico" type="image/x-icon">
  <link rel="stylesheet" href="../../assets/css/style.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
  <style>
    .crtp-sidebar { padding: 20px; }
    .crtp-sidebar h3 { color: #ffdb70; margin-bottom: 15px; font-size: 1.1rem; }
    .crtp-sidebar .portfolio-link { 
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
    }
    .crtp-sidebar .portfolio-link:hover { 
      background: #ffdb70; 
      color: #1a1a1a; 
    }
    .crtp-sidebar a { display: block; padding: 8px 12px; margin: 4px 0; color: #d6d6d6; text-decoration: none; border-radius: 6px; font-size: 0.9rem; transition: all 0.2s; }
    .crtp-sidebar a:hover { background: #2a2a2a; color: #ffdb70; }
    .crtp-sidebar a.active { background: #ffdb70; color: #1a1a1a; font-weight: 600; }
    .page-nav { display: flex; justify-content: space-between; margin: 30px 0; padding: 20px 0; border-top: 1px solid #2a2a2a; }
    .nav-btn { background: #2a2a2a; color: #ffdb70; padding: 10px 20px; border-radius: 6px; text-decoration: none; transition: all 0.2s; }
    .nav-btn:hover { background: #ffdb70; color: #1a1a1a; }
    .notion-content { line-height: 1.6; }
    .notion-content img { max-width: 100%; height: auto; margin: 20px 0; border-radius: 8px; }
    .notion-content h1 { font-size: 1.8rem; margin: 30px 0 20px; color: #fafafa; }
    .notion-content h2 { font-size: 1.5rem; margin: 25px 0 15px; color: #fafafa; }
    .notion-content h3 { font-size: 1.3rem; margin: 20px 0 10px; color: #fafafa; }
    .notion-content p { margin: 15px 0; color: #d6d6d6; }
    .notion-content ul, .notion-content ol { margin: 15px 0; padding-left: 30px; }
    .notion-content li { margin: 5px 0; color: #d6d6d6; }
    .notion-content code { background: #2a2a2a; padding: 2px 6px; border-radius: 4px; font-family: 'Courier New', monospace; color: #ffdb70; }
    .notion-content pre { background: #1e1e1e; border-left: 4px solid #ffdb70; padding: 15px; margin: 20px 0; border-radius: 0 8px 8px 0; overflow-x: auto; }
    .notion-content a { color: #ffdb70; text-decoration: underline; }
    .notion-content strong { color: #fafafa; font-weight: 600; }
    .notion-content figure { margin: 20px 0; }
    .notion-content figcaption { display: none; }
    .main-content { max-width: 100% !important; }
    .about { max-width: 100% !important; padding: 20px 40px !important; }
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
""" + SIDEBAR_LINKS + """
        </div>
        <div class="separator"></div>
        <ul class="contacts-list">
          <li class="contact-item">
            <div class="icon-box">
              <ion-icon name="arrow-back-outline"></ion-icon>
            </div>
            <div class="contact-info">
              <p class="contact-title">Back</p>
              <a href="../../" class="contact-link">Portfolio</a>
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
        <header class="h2 article-title">Overview</header>
        <section class="about-text notion-content">
          <h1>CRTP - Certified Red Team Professional</h1>
          <p>Welcome to my CRTP (Certified Red Team Professional) study notes. This comprehensive guide covers various attack techniques in Active Directory environments.</p>
          
          <p><strong>Note:</strong> This is the main overview page. Select a section from the sidebar to begin.</p>
          
          <h2>What is CRTP?</h2>
          <p>Certified Red Team Professional (CRTP) is a certification that teaches Red Team operators how to audit and exploit Microsoft environments, focusing on Active Directory attacks and defense techniques.</p>
          
          <h2>Parts</h2>
          <ul>
            <li><strong>Part 1:</strong> Enumeration</li>
            <li><strong>Part 2:</strong> Privilege Escalation</li>
            <li><strong>Part 3:</strong> Privilege Escalation via Domain Admin session</li>
            <li><strong>Part 4:</strong> Golden Ticket</li>
            <li><strong>Part 5:</strong> Silver Ticket</li>
            <li><strong>Part 6:</strong> Diamond Ticket</li>
            <li><strong>Part 7:</strong> Abusing DSRM Credentials</li>
            <li><strong>Part 8:</strong> DCSync Attack</li>
            <li><strong>Part 9:</strong> Security Descriptor Abuse</li>
            <li><strong>Part 10:</strong> ASREP-Roasting Attack</li>
            <li><strong>Part 11:</strong> Unconstrained Delegation</li>
            <li><strong>Part 12:</strong> Constrained Delegation</li>
            <li><strong>Part 13:</strong> Resource-Based Constrained Delegation (RBCD)</li>
            <li><strong>Part 14:</strong> Enterprise Admins Trust – SID-History Abuse with Trust Ticket</li>
            <li><strong>Part 15:</strong> Enterprise Admin Trust – SID-History Abuse with KRBTGT hash</li>
            <li><strong>Part 16:</strong> Cross-Forest Trust – Trust Flow</li>
            <li><strong>Part 17:</strong> ADCS Attacks</li>
            <li><strong>Part 18:</strong> Trust Links Abuse</li>
            <li><strong>Part 19:</strong> MDE / MDI Bypass</li>
          </ul>
          
          <p>Select a section from the sidebar to begin your learning journey.</p>
        </section>
      </article>
    </div>
  </main>

  <script src="../../assets/js/script.js"></script>
  <script type="module" src="https://unpkg.com/ionicons@5.5.2/dist/ionicons/ionicons.esm.js"></script>
  <script nomodule src="https://unpkg.com/ionicons@5.5.2/dist/ionicons/ionicons.js"></script>
</body>
</html>
"""

INDEX_REDIRECT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url=overview.html">
    <title>CRTP - Redirecting...</title>
</head>
<body>
    <p>Redirecting to <a href="overview.html">CRTP Overview</a>...</p>
</body>
</html>
"""

def get_title_from_filename(filename):
    """Extract title from filename for the page header"""
    name = filename.replace('.html', '').replace('-', ' ')
    return name.title()

def get_page_title(filename):
    """Get the title that appears in the header of the page"""
    titles = {
        "part-01-enumeration.html": "Part 1 – Enumeration",
        "part-02-privilege-escalation.html": "Part 2 – Privilege Escalation",
        "part-03-da-session.html": "Part 3 – Privilege Escalation via Domain Admin session",
        "part-04-golden-ticket.html": "Part 4 – Golden Ticket",
        "part-05-silver-ticket.html": "Part 5 – Silver Ticket",
        "part-06-diamond-ticket.html": "Part 6 – Diamond Ticket",
        "part-07-dsrm-credentials.html": "Part 7 – Abusing DSRM Credentials",
        "part-08-dcsync.html": "Part 8 – DCSync Attack",
        "part-09-security-descriptor.html": "Part 9 – Security Descriptor Abuse",
        "part-10-asrep-roasting.html": "Part 10 – ASREP-Roasting Attack",
        "part-11-unconstrained-delegation.html": "Part 11 – Unconstrained Delegation",
        "part-12-constrained-delegation.html": "Part 12 – Constrained Delegation",
        "part-13-rbcd.html": "Part 13 – Resource-Based Constrained Delegation (RBCD)",
        "part-14-sid-history-trust-ticket.html": "Part 14 – Enterprise Admins Trust – SID-History Abuse with Trust Ticket",
        "part-15-sid-history-krbtgt.html": "Part 15 – Enterprise Admin Trust – SID-History Abuse with KRBTGT hash",
        "part-16-cross-forest-trust.html": "Part 16 – Cross-Forest Trust – Trust Flow",
        "part-17-adcs-attacks.html": "Part 17 – ADCS Attacks",
        "part-18-trust-links-abuse.html": "Part 18 – Trust Links Abuse",
        "part-19-mde-mdi-bypass.html": "Part 19 – MDE / MDI Bypass",
    }
    return titles.get(filename, filename.replace('.html', '').replace('-', ' ').title())

def process_file(old_filename, new_filename):
    """Process a file: update sidebar and fix links"""
    filepath = os.path.join(CRTP_DIR, old_filename)
    if not os.path.exists(filepath):
        print(f"Skipping {old_filename} - not found")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace sidebar section
    # Match from start of sidebar div to end of sidebar links
    sidebar_pattern = r'<div class="crtp-sidebar">.*?<h3>Sections</h3>.*?</div>'
    sidebar_replacement = f'<div class="crtp-sidebar">\n{SIDEBAR_LINKS}\n        </div>'
    
    content = re.sub(sidebar_pattern, sidebar_replacement, content, flags=re.DOTALL)
    
    # Fix internal links: change from *.html to proper part-XX-*.html
    for old_name, new_name in MAPPING.items():
        if old_name != new_name:
            # Only replace links that point to old files
            content = content.replace(f'href="{old_name}"', f'href="{new_name}"')
    
    # Update page title in header
    page_title = get_page_title(new_filename)
    content = re.sub(r'<title>.*? - CRTP</title>', f'<title>{page_title} - CRTP</title>', content)
    
    # Update article title
    content = re.sub(r'<header class="h2 article-title">.*?</header>', f'<header class="h2 article-title">{page_title}</header>', content)
    
    # Write to new file
    new_filepath = os.path.join(CRTP_DIR, new_filename)
    with open(new_filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Processed: {old_filename} -> {new_filename}")
    
    # Remove old file if different
    if old_filename != new_filename:
        os.remove(filepath)
        print(f"  Removed: {old_filename}")

def main():
    # Create overview.html
    overview_path = os.path.join(CRTP_DIR, "overview.html")
    with open(overview_path, 'w', encoding='utf-8') as f:
        f.write(OVERVIEW_CONTENT)
    print("Created overview.html")
    
    # Update index.html to redirect
    index_path = os.path.join(CRTP_DIR, "index.html")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(INDEX_REDIRECT)
    print("Updated index.html to redirect to overview.html")
    
    # Process each file
    for old_name, new_name in MAPPING.items():
        process_file(old_name, new_name)
    
    print("\nDone! All files processed.")

if __name__ == "__main__":
    main()
