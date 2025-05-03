from db import personal_data_collection, notes_collection
from datetime import datetime, timezone  # <--- IMPORTANT: Add timezone import

def update_personal_info(existing, update_type, **kwargs):
    if update_type == "goals":
        existing["goals"] = kwargs.get("goals", [])
        update_field = {"goals": existing["goals"]}
    else:
        existing[update_type] = kwargs
        update_field = {update_type: existing[update_type]}

    personal_data_collection.update_one(
        {"_id": existing["_id"]}, {"$set": update_field}
    )
    return existing

def add_note(note_text, profile_id):
    new_note = {
        "text": note_text,
        "profile_id": profile_id,
        "injected": datetime.now(timezone.utc).isoformat()  # safe UTC time
    }

    inserted_note = notes_collection.insert_one(new_note)

    # Correct way to get inserted ID:
    new_note["_id"] = inserted_note.inserted_id  # ✅ CORRECT
    return new_note


def delete_note(_id):
    return notes_collection.delete_one({"_id": _id})
