import os
files = [f for f in os.listdir('.') if f.endswith('.html')]
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    content = content.replace('href="index.html#anchor-achat-vente-location"', 'href="vente.html"')
    content = content.replace('href="#" onclick="lenis.scrollTo(\'#anchor-achat-vente-location\', {duration: 1.5}); return false;"', 'href="vente.html"')
    content = content.replace('href="index.html#anchor-gestion"', 'href="gestion.html"')
    content = content.replace('href="#" onclick="lenis.scrollTo(\'#anchor-gestion\', {duration: 1.5}); return false;"', 'href="gestion.html"')
    content = content.replace('href="#estimation"', 'href="estimation.html"')
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
