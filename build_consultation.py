import codecs

with open('consultation.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('<title>G.E.S Immo - Prendre Rendez-vous</title>', '<title>G.E.S Immo - Demander une Consultation</title>')
text = text.replace('<span class="xel-eyebrow">Rencontrons-nous</span>', '<span class="xel-eyebrow">Expertise Construction</span>')
text = text.replace('<h2>Prendre Rendez-vous</h2>', '<h2>Demander une Consultation</h2>')
text = text.replace('<p>Programmez une visite ou une entrevue avec nos experts immobiliers.</p>', '<p>Parlez-nous de votre projet de construction ou de rénovation. Nos ingénieurs sont à votre écoute.</p>')

# Replace the specific fields
text = text.replace('Objectif de la visite', 'Type de projet')
text = text.replace('<option value="achat">Achat d\'un bien</option>', '<option value="neuve">Construction neuve</option>')
text = text.replace('<option value="location">Visite pour location</option>', '<option value="renovation">Rénovation / Aménagement</option>')
text = text.replace('<option value="vente">Confier une vente</option>', '<option value="gros_oeuvre">Gros Œuvre / Architecture</option>')
text = text.replace('<option value="gestion">Mettre en gestion</option>', '<option value="autre">Autre</option>')

text = text.replace('Date de visite souhaitée', 'Date de début souhaitée')

text = text.replace('Confirmer le Rendez-vous', 'Envoyer la Demande')

text = text.replace('Retour à la page Location', 'Retour à la page Construction')
text = text.replace('href="location.html"', 'href="construction.html"')

with open('consultation.html', 'w', encoding='utf-8') as f:
    f.write(text)
