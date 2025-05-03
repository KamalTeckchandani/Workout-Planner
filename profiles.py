from db import personal_data_collection, notes_collection

def get_values(_id):
    return {
        "_id": _id, 
        "general": {
            "name": "",
            "age": 30,
            "weight": 60,
            "height": 165,
            "activity_level": "Moderately Active",
            "gender": "Male"
        },
        "goals": ["Muscle Gain"],
        "nutrition": {
            "calories": 2000,
            "protein": 140,
            "fat": 20,
            "carbs": 100,
            },
    }
    
def create_profile(_id):
    profile_values = get_values(_id)
    personal_data_collection.insert_one(profile_values)
    return _id, profile_values  


def get_profile(_id):
    return personal_data_collection.find_one({"_id": {"$eq": _id}})

def get_notes(_id):
    return list(notes_collection.find({"profile_id": {"$eq": _id}}))

