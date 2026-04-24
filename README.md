# 🧶 CrochetChic — Application d'enquête

Application Flask de collecte et d'analyse descriptive des données pour une marque de mode au crochet.

## Structure
```
crochet-app/
├── app.py              # Backend Flask (API)
├── templates/
│   └── index.html      # Frontend (design rose & blanc)
├── requirements.txt
├── Procfile            # Pour déploiement Render/Railway
└── responses.json      # Données collectées (auto-créé)
```

## Fonctionnalités
- ✅ Formulaire de collecte (10 champs)
- ✅ Tableau de bord avec statistiques
- ✅ Graphiques en barres par variable
- ✅ Liste des suggestions clients
- ✅ Export CSV des données
- ✅ Design rose & blanc élégant

## Déploiement sur Render.com (GRATUIT)

1. Créez un compte sur https://render.com
2. "New Web Service" → connectez votre GitHub
3. Uploadez ce dossier sur GitHub
4. Sur Render : Build Command = `pip install -r requirements.txt`
5. Start Command = `gunicorn app:app`
6. Déployez → vous obtenez un lien `.onrender.com`

## Lancer en local
```bash
pip install flask gunicorn
python app.py
# → http://localhost:5000
```

## API Endpoints
- `GET /` — Page principale
- `POST /api/submit` — Soumettre une réponse
- `GET /api/stats` — Statistiques descriptives
- `GET /api/export` — Télécharger CSV

## INF 232 EC2 — Critères notés
- **Idée** : Marque de crochet fait main (mode & accessoires) 🧶
- **Robustesse** : Validation des champs, gestion des erreurs
- **Efficacité** : API REST légère, réponses rapides
- **Fiabilité** : Stockage JSON persistant, export CSV
