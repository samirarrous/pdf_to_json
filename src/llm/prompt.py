




def build_prompt(user_prompt: str, schema: str, text: str) -> str:
    return f"""
Tu es un système d'extraction d'informations depuis des documents.

RÈGLES ABSOLUES :
- Tu réponds UNIQUEMENT en JSON valide
- Aucun texte avant ou après
- Aucun commentaire
- Aucun markdown
- Tu respectes STRICTEMENT le schéma fourni

IMPORTANT :
- Si une information est absente → "" ou 0
- Ne jamais inventer d'information

---

SCHÉMA JSON À RESPECTER :
{schema}

---

TÂCHE DEMANDÉE PAR L'UTILISATEUR :
{user_prompt}

---

DOCUMENT :
{text}
"""