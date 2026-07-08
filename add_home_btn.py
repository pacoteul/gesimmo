import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Check if "Accueil" link already exists before Construction
    if re.search(r'>Accueil</a>\s*</li>\s*<li>\s*<a[^>]*href="construction.html"', content, re.IGNORECASE) or \
       re.search(r'>Accueil</a>\s*<a[^>]*href="construction.html"', content, re.IGNORECASE):
        print(f"Skipping {f} (Accueil already present)")
        continue
        
    # Replace for <li> wrapped navs (like index.html, achat.html)
    # The active class could be present in construction.html
    new_content = re.sub(
        r'(<li>\s*<a[^>]*href="construction\.html"[^>]*>Construction</a>\s*</li>)',
        r'<li><a href="index.html">Accueil</a></li>\n            \1',
        content,
        flags=re.IGNORECASE
    )
    
    # Replace for naked <a> tags (like rendezvous.html)
    if new_content == content:
        new_content = re.sub(
            r'(<nav[^>]*>.*?)(<a[^>]*href="construction\.html"[^>]*>Construction</a>)',
            r'\1<a href="index.html">Accueil</a>\n            \2',
            content,
            flags=re.IGNORECASE | re.DOTALL
        )
        
    if new_content != content:
        # For index.html, the Accueil link should probably be active
        if f == 'index.html':
            new_content = new_content.replace(
                '<li><a href="index.html">Accueil</a></li>',
                '<li><a href="index.html" class="active" style="color: var(--primary);">Accueil</a></li>'
            )
            
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"Added Accueil to {f}")
    else:
        print(f"No match in {f}")
