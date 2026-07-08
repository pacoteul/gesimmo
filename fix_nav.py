import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    content = re.sub(r'<li>\s*<a[^>]*>Achat</a>\s*</li>', '<li><a href="achat.html">Achat</a></li>', content)
    content = re.sub(r'<li>\s*<a[^>]*>Location</a>\s*</li>', '<li><a href="location.html">Location</a></li>', content)
    content = re.sub(r'<li>\s*<a[^>]*>Vente</a>\s*</li>', '<li><a href="vente.html">Vente</a></li>', content)
    content = re.sub(r'<li>\s*<a[^>]*>Construction</a>\s*</li>', '<li><a href="construction.html">Construction</a></li>', content)
    content = re.sub(r'<li>\s*<a[^>]*>Gestion</a>\s*</li>', '<li><a href="gestion.html">Gestion</a></li>', content)
    
    # Handle the active state for the current page
    if f == 'achat.html':
        content = content.replace('<li><a href="achat.html">Achat</a></li>', '<li><a href="achat.html" class="active" style="color: var(--primary);">Achat</a></li>')
    elif f == 'location.html':
        content = content.replace('<li><a href="location.html">Location</a></li>', '<li><a href="location.html" class="active" style="color: var(--primary);">Location</a></li>')
    elif f == 'vente.html':
        content = content.replace('<li><a href="vente.html">Vente</a></li>', '<li><a href="vente.html" class="active" style="color: var(--primary);">Vente</a></li>')
    elif f == 'construction.html':
        content = content.replace('<li><a href="construction.html">Construction</a></li>', '<li><a href="construction.html" class="active" style="color: var(--primary);">Construction</a></li>')
    elif f == 'gestion.html':
        content = content.replace('<li><a href="gestion.html">Gestion</a></li>', '<li><a href="gestion.html" class="active" style="color: var(--primary);">Gestion</a></li>')
        
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
        
    print(f"Updated links in {f}")
