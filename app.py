from flask import Flask, render_template
import os
import urllib.parse
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# ==========================================
# DONNÉES DES PROJETS (Mode "Snackable" / Vente Bois & Habitat)
# ==========================================
projets = {
    "cava-vin": {
        "titre_propre": "Cave à Vin sur mesure",
        "photos_tv": ['/static/images/cava-vin.webp'],
        "atouts": [
            "Aménagement optimisé sous l'escalier",
            "Matériaux nobles : 3 plis chêne",
            "Frigo encastré et éclairage LED scénographique"
        ]
    },
    "meuble-tv": {
        "titre_propre": "Meuble TV - Home Cinéma",
        "photos_tv": ['/static/images/meuble-tv.webp'],
        "atouts": [
            "Intégration d'un home cinéma invisible",
            "Cloison acoustique sur mesure",
            "Finition premium plaquée chêne et laquée"
        ]
    },
    "meuble-salon": {
        "titre_propre": "Aménagement & Porte Intégrée",
        "photos_tv": ['/static/images/meuble-salon.webp'],
        "atouts": [
            "Porte d'accès parfaitement dissimulée",
            "Lignes courbes et design fluide",
            "Mélange harmonieux stratifié bois et laque vert d'eau"
        ]
    },
    "cuisine-blanc-bleu": {
        "titre_propre": "Cuisine Blanc & Bleu",
        "photos_tv": ['/static/images/cuisine-blanc-bleu.webp'],
        "atouts": [
            "Ouverture passe-plat magnétique astucieuse",
            "Façades stratifié blanc mat et bleu profond",
            "Détails raffinés en plaqué chêne"
        ]
    },
    "cuisine-arrondie": {
        "titre_propre": "Cuisine Arrondie",
        "photos_tv": ['/static/images/cuisine-arondi.webp'], 
        "atouts": [
            "Îlot sur mesure épousant la courbe du mur",
            "MDF teinté bleu et lamellé collé chêne",
            "Design organique, fluide et naturel"
        ]
    },
    "buanderie": {
        "titre_propre": "Buanderie Optimisée",
        "photos_tv": ['/static/images/buanderie.webp'],
        "atouts": [
            "Esthétique soignée, ouverte sur le hall",
            "Machines surélevées pour un confort optimal",
            "Stratifié Balmoral sur MDF teinté noir"
        ]
    },
    "cuisine-verte": {
        "titre_propre": "Cuisine Verte",
        "photos_tv": ['/static/images/cusine-verte.webp'], 
        "atouts": [
            "Rénovation intelligente : conservation de la base",
            "Nouvelles façades laqué vert d'eau",
            "Plan de travail luxueux en Pierre Steel Grey"
        ]
    },
    "cuisine-bleu": {
        "titre_propre": "Cuisine Bleue",
        "photos_tv": ['/static/images/cusine-bleu.webp'], 
        "atouts": [
            "Optimisation maximale des espaces de rangement",
            "Laqué bleu profond et bois naturel",
            "Poignées élégantes en laiton doré"
        ]
    },
    "cuisine-gris": {
        "titre_propre": "Cuisine Grise",
        "photos_tv": ['/static/images/cusine-gris.webp'], 
        "atouts": [
            "Banquette sur mesure intégrée sous la fenêtre",
            "Coin bar convivial pour le quotidien",
            "Bouleau tranché vernis mat"
        ]
    },
    "cuisine-blanc": {
        "titre_propre": "Cuisine Blanche & Bois",
        "photos_tv": ['/static/images/cuisine-blanc.webp'],
        "atouts": [
            "Îlot central rassembleur avec 6 assises",
            "Baldaquin en bois avec éclairage intégré",
            "Matériaux d'exception : Sirocco blanc, chêne et Corian"
        ]
    },
    "chambre": {
        "titre_propre": "Aménagement Chambre",
        "photos_tv": ['/static/images/chambre.webp'],
        "atouts": [
            "Rangements astucieux et entièrement sur mesure",
            "Ambiance apaisante, naturelle et chaleureuse",
            "Matériaux durables et finitions haut de gamme"
        ]
    },
    "bibliotheque": {
        "titre_propre": "Bibliothèque Sur Mesure",
        "photos_tv": ['/static/images/bibliotheque.webp'],
        "atouts": [
            "Bibliothèque fluide intégrant une longue banquette",
            "Alliance de bois clair et façades vert sauge",
            "Lignes courbes et modernité des formes"
        ]
    },
    "dressing": {
        "titre_propre": "Dressing Élégant",
        "photos_tv": ['/static/images/dressing.webp'],
        "atouts": [
            "Contraste graphique chêne clair et noir mat",
            "Îlot central fonctionnel sous la lumière naturelle",
            "Éclairage LED scénographique intégré"
        ]
    },
    "cuisine-bois": {
        "titre_propre": "Cuisine Bois & Terrazzo",
        "photos_tv": ['/static/images/cuisine-bois.webp'],
        "atouts": [
            "Design organique aux lignes courbes",
            "Bois clair à grain prononcé et plan Terrazzo",
            "Crédence texturée audacieuse en OSB"
        ]
    },
    "hall-entree": {
        "titre_propre": "Aménagement Hall d'entrée",
        "photos_tv": ['/static/images/hall-entree.webp'],
        "atouts": [
            "Meuble vestiaire et bibliothèque astucieusement combinés",
            "Banc aux lignes arrondies et grand miroir en arche",
            "Pureté visuelle avec poignées creusées dans la masse"
        ]
    }
}

@app.route('/')
def index():
    toutes_les_images = [donnees['photos_tv'][0] for id_proj, donnees in projets.items() if donnees.get('photos_tv')]
    return render_template('index.html', toutes_les_images=toutes_les_images)

@app.route('/reset')
def reset():
    toutes_les_images = [donnees['photos_tv'][0] for id_proj, donnees in projets.items() if donnees.get('photos_tv')]
    socketio.emit('lancer_diaporama', {'urls': toutes_les_images, 'is_idle': True})
    return "Reset OK", 200

@app.route('/scan/<id_projet>')
def scan(id_projet):
    if id_projet not in projets:
        return render_template('404.html'), 404
        
    donnees = projets[id_projet]
    
    # Envoi direct à la TV via SocketIO
    socketio.emit('lancer_diaporama', {'urls': donnees['photos_tv'], 'is_idle': False})
    
    # Formatage des bullet points
    atouts_html = "".join([f"<li><span class='check'>✨</span> {atout}</li>" for atout in donnees['atouts']])
    
    # Message WhatsApp dynamique qui inclut le nom du projet
    titre_projet_encode = urllib.parse.quote(donnees['titre_propre'])
    whatsapp_url = f"https://wa.me/3281470500?text=Bonjour%20Ambiose%20!%20%F0%9F%91%8B%0AJe%20suis%20sur%20votre%20stand%20%C3%A0%20Bois%20%26%20Habitat.%20J'ai%20scann%C3%A9%20le%20projet%20%22{titre_projet_encode}%22%20et%20j'aimerais%20discuter%20d'un%20am%C3%A9nagement.%0A%0A%F0%9F%91%89%20Mon%20projet%20%3A%20%5BCuisine%20%2F%20Dressing%20%2F%20Meuble%20%2F%20Autre%5D%0A%E2%8F%B3%20Mon%20timing%20%3A%20%5BUrgent%20%2F%20J'ai%20le%20temps%5D%0A%0A%C3%80%20tr%C3%A8s%20vite%20!"
    
    # Interface mobile orientée "Landing Page / Conversion"
    page_mobile = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <link rel="icon" type="image/png" href="/static/images/logo.png">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Ambiose - {donnees['titre_propre']}</title>
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            body {{ background-color: #FAF8F5; color: #1a1a1a; font-family: 'Montserrat', sans-serif; margin: 0; padding: 0; padding-bottom: 150px; }}
            .event-banner {{ background-color: #2E4F40; color: white; text-align: center; padding: 10px; font-size: 0.85em; font-weight: 600; letter-spacing: 1px; }}
            .header {{ background-color: #FFFFFF; padding: 15px; text-align: center; border-bottom: 2px solid #a3bfa3; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }}
            .header img {{ max-height: 40px; }}
            
            .hero-image {{ width: 100%; height: 250px; background-image: url('{donnees['photos_tv'][0]}'); background-size: cover; background-position: center; }}
            
            .content {{ padding: 25px 20px; }}
            h1 {{ font-size: 1.6em; color: #2E4F40; margin-top: 0; margin-bottom: 20px; text-align: center; }}
            
            .atouts-list {{ list-style-type: none; padding: 0; margin: 0 0 25px 0; }}
            .atouts-list li {{ margin-bottom: 15px; font-size: 1em; line-height: 1.5; display: flex; align-items: flex-start; background: white; padding: 15px; border-radius: 12px; box-shadow: 0 4px 10px rgba(163, 191, 163, 0.15); }}
            .check {{ margin-right: 12px; font-size: 1.2em; }}
            
            .tv-badge {{ background-color: #b4c3dc; color: white; padding: 12px 20px; border-radius: 30px; font-weight: 700; font-size: 0.9em; text-align: center; margin: 0 auto; width: fit-content; box-shadow: 0 4px 10px rgba(180, 195, 220, 0.4); }}
            
            .bottom-bar {{ position: fixed; bottom: 0; left: 0; right: 0; background: #FFFFFF; box-shadow: 0 -10px 20px rgba(0,0,0,0.1); padding: 15px 20px 25px 20px; z-index: 100; }}
            
            .fomo-box {{ background-color: #fcf1eb; border: 1px solid #e8d0c1; color: #a1584b; font-size: 0.75em; font-weight: 600; text-align: center; padding: 8px; border-radius: 8px; margin-bottom: 12px; }}
            
            .cta-sticky {{ display: block; width: 100%; max-width: 400px; margin: 0 auto; background-color: #C26D5C; color: #FFFFFF; text-decoration: none; padding: 18px 20px; border-radius: 30px; text-align: center; font-weight: 700; font-size: 1.1em; box-shadow: 0 4px 15px rgba(194, 109, 92, 0.4); animation: pulse-terracotta 2s infinite; }}
            
            @keyframes pulse-terracotta {{
                0% {{ box-shadow: 0 0 0 0 rgba(194, 109, 92, 0.7); }}
                70% {{ box-shadow: 0 0 0 15px rgba(194, 109, 92, 0); }}
                100% {{ box-shadow: 0 0 0 0 rgba(194, 109, 92, 0); }}
            }}
        </style>
    </head>
    <body>
        <div class="event-banner">📍 En direct du Salon Bois & Habitat</div>
        <div class="header">
            <a href="https://ambiose.be/" target="_blank">
                <img src="/static/images/logo.png" alt="Logo Ambiose">
            </a>
        </div>
        
        <div class="hero-image"></div>
        
        <div class="content">
            <h1>{donnees['titre_propre']}</h1>
            
            <ul class="atouts-list">
                {atouts_html}
            </ul>
            
            <div class="tv-badge">👀 Regardez la grande TV du stand</div>
        </div>
        
        <div class="bottom-bar">
            <div class="fomo-box">🎁 Avantage Salon : 1ère étude 3D offerte pour tout contact aujourd'hui !</div>
            <a href="{whatsapp_url}" target="_blank" class="cta-sticky">
                📞 Concevoir mon projet
            </a>
        </div>
    </body>
    </html>
    """
    return page_mobile

@app.route('/remote')
def remote_control():
    boutons_html = """<button onclick="resetTV()" class="remote-btn reset-btn">🔄 Relancer l'écran de veille</button>"""
    for id_proj, data in projets.items():
        boutons_html += f"""<button onclick="triggerProject('{id_proj}')" class="remote-btn">{data['titre_propre']}</button>"""

    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Télécommande Vendeur</title>
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700&display=swap" rel="stylesheet">
        <style>
            body {{ background: #FAF8F5; color: #2E4F40; font-family: 'Montserrat', sans-serif; padding: 20px; text-align: center; }}
            .remote-grid {{ display: grid; grid-template-columns: 1fr; gap: 12px; margin-top: 20px; }}
            .remote-btn {{ background: white; color: #2E4F40; border: 2px solid #a3bfa3; padding: 18px; border-radius: 12px; font-weight: 700; font-size: 1em; cursor: pointer; }}
            .reset-btn {{ background: #2E4F40; color: white; border: none; margin-bottom: 15px; }}
            #status {{ margin-top: 15px; font-weight: bold; color: #a3bfa3; }}
        </style>
    </head>
    <body>
        <img src="/static/images/logo.png" style="max-height: 40px;" alt="Logo Ambiose">
        <h2>Télécommande Cadres</h2>
        <div id="status"></div>
        <div class="remote-grid">{boutons_html}</div>
        <script>
            function triggerProject(id) {{
                fetch('/scan/' + id).then(r => document.getElementById('status').innerText = "TV mise à jour ! ✅");
                setTimeout(() => document.getElementById('status').innerText = "", 2000);
            }}
            function resetTV() {{
                fetch('/reset').then(r => document.getElementById('status').innerText = "Écran de veille ! 🔄");
                setTimeout(() => document.getElementById('status').innerText = "", 2000);
            }}
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)