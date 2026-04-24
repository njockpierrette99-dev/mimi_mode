from flask import Flask, render_template, request, jsonify, send_file
import os
import csv
import io
from datetime import datetime
from supabase import create_client, Client

app = Flask(__name__)

# ─── Connexion Supabase ───────────────────────────────────────────────────────
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://psyrmypxuvetttuqtvmy.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzeXJteXB4dXZldHR0dXF0dm15Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY4NDQwNzMsImV4cCI6MjA5MjQyMDA3M30.qDba28f1QjHIr46UuwZwu37SEzx9bfZCSQUjXDPmxoI")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
TABLE = "reponses"

# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/submit", methods=["POST"])
def submit():
    try:
        data = request.get_json()

        required = ["sexe", "age", "produit", "frequence", "budget",
                    "couleur", "style", "plateforme", "interet"]
        for field in required:
            if not data.get(field):
                return jsonify({"success": False, "error": f"Champ manquant : {field}"}), 400

        entry = {
            "sexe":       data["sexe"],
            "age":        data["age"],
            "produit":    data["produit"],
            "frequence":  data["frequence"],
            "budget":     data["budget"],
            "couleur":    data["couleur"],
            "style":      data["style"],
            "plateforme": data["plateforme"],
            "interet":    data["interet"],
            "suggestion": data.get("suggestion", "")[:500]
        }

        result = supabase.table(TABLE).insert(entry).execute()

        if result.data:
            count = supabase.table(TABLE).select("id", count="exact").execute()
            return jsonify({
                "success": True,
                "message": "Réponse enregistrée avec succès !",
                "total": count.count
            })
        else:
            return jsonify({"success": False, "error": "Erreur lors de l'insertion"}), 500

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/stats", methods=["GET"])
def stats():
    try:
        result = supabase.table(TABLE).select("*").execute()
        responses = result.data or []

        if not responses:
            return jsonify({"total": 0, "stats": {}})

        def freq(field):
            counts = {}
            for r in responses:
                v = r.get(field, "") or ""
                counts[v] = counts.get(v, 0) + 1
            return counts

        return jsonify({
            "total": len(responses),
            "stats": {
                "sexe":       freq("sexe"),
                "age":        freq("age"),
                "produit":    freq("produit"),
                "frequence":  freq("frequence"),
                "budget":     freq("budget"),
                "couleur":    freq("couleur"),
                "style":      freq("style"),
                "plateforme": freq("plateforme"),
                "interet":    freq("interet"),
            },
            "suggestions": [r["suggestion"] for r in responses if r.get("suggestion")]
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/export", methods=["GET"])
def export_csv():
    try:
        result = supabase.table(TABLE).select("*").order("created_at").execute()
        responses = result.data or []

        output = io.StringIO()
        fieldnames = ["id", "created_at", "sexe", "age", "produit", "frequence",
                      "budget", "couleur", "style", "plateforme", "interet", "suggestion"]
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for r in responses:
            writer.writerow(r)

        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode("utf-8-sig")),
            mimetype="text/csv",
            as_attachment=True,
            download_name=f"crochet_enquete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
