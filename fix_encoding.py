import os

files = [f for f in os.listdir('.') if f.endswith('.html')]

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Ǹ -> é
    content = content.replace('Ǹ', 'é')
    
    # Common  replacements
    content = content.replace(' la ', 'à la ')
    content = content.replace(' l\'', 'à l\'')
    content = content.replace("jusqu'", "jusqu'à")
    content = content.replace('Prêt ', 'Prêt à')
    content = content.replace('prêt ', 'prêt à')
    content = content.replace('O', 'Où')
    content = content.replace('Dcrivez', 'Décrivez')
    content = content.replace('prfrs', 'préférés')
    content = content.replace('dlais', 'délais')
    content = content.replace('estim', 'estimé')
    content = content.replace('', 'à') # remaining ones are mostly 'à'
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Files fixed.")
