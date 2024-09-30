from pymongo import MongoClient

# Establish a connection to the MongoDB cluster
# ISERT YOUR OWN DATA
client = MongoClient("mongodb+srv://USERNAME:PASSWORD@URI_CONNECTION/")

# Access the database and collection
db = client["cats_db"]
collection = db["cats"]

# List of cat documents to be inserted into the collection
cats = [
    {"name": "Barsik", "age": 3, "features": ["love tricks", "love milk", "black"]},
    {"name": "Murzik", "age": 5, "features": ["hate water", "love naps", "gray"]},
    {"name": "Vasya", "age": 2, "features": ["playful", "curious", "white"]},
    {"name": "Simba", "age": 4, "features": ["brave", "love climbing", "orange"]},
    {"name": "Fluffy", "age": 1, "features": ["gentle", "love being petted", "fluffy"]},
    {"name": "Milo", "age": 6, "features": ["smart", "independent", "striped"]},
    {"name": "Oscar", "age": 7, "features": ["calm", "love sleeping", "brown"]},
    {"name": "Tom", "age": 2, "features": ["active", "love chasing mice", "gray"]},
    {"name": "Leo", "age": 3, "features": ["adventurous", "love exploring", "white"]},
    {"name": "Felix", "age": 4, "features": ["mischievous", "love hunting", "black"]},
]


def fill_collection(data):
    """
    Inserts multiple documents into the collection.
    """
    collection.insert_many(data)
    print(f"Collection {collection.name} was filled")


def all_docs():
    """
    Retrieves and prints all documents from the collection.
    """
    try:
        docs = collection.find({})
        for cat in docs:
            print(cat)
    except Exception as e:
        print(f"Error fetching documents: {e}")


def find_by_name(name):
    """
    Finds and prints a document by the cat's name.
    """
    try:
        result = collection.find_one({"name": name}, {"_id": 0})
        if result:
            print(result)
        else:
            print(f"No cat found with name: {name}")
    except Exception as e:
        print(f"Error finding document: {e}")


def update_age_by_name(name, age):
    """
    Updates the age of the cat with the specified name.
    """
    try:
        collection.update_one({"name": name}, {"$set": {"age": age}})
        result = collection.find_one({"name": name}, {"_id": 0})
        print(result)
    except Exception as e:
        print(f"Error updating document: {e}")


def add_features(name, features):
    """
    Adds new features to the cat's feature list.
    Accepts a list of features or a single feature.
    """
    try:
        if isinstance(features, list):
            collection.update_one(
                {"name": name}, {"$push": {"features": {"$each": features}}}
            )
        else:
            collection.update_one({"name": name}, {"$push": {"features": features}})

        result = collection.find_one({"name": name}, {"_id": 0})
        print(result)
    except Exception as e:
        print(f"Error adding features: {e}")


def delete(name):
    """
    Deletes a document from the collection by the cat's name.
    """
    try:
        collection.delete_one({"name": name})
        print(f"{name} was deleted")
    except Exception as e:
        print(f"Error deleting document: {e}")


def delete_all():
    """
    Deletes all documents from the collection.
    """
    try:
        collection.delete_many({})
        print("All documents deleted")
    except Exception as e:
        print(f"Error deleting documents: {e}")


# Example usage of fill_collection
# Fill the collection with initial data (list of cats)
fill_collection(cats)

# Example usage of all_docs
# Display all documents currently in the collection
all_docs()

# Example usage of find_by_name
# Find and display the document for the cat named "Barsik"
find_by_name("Barsik")

# Example usage of update_age_by_name
# Update the age of the cat named "Murzik" to 6 years old
update_age_by_name("Murzik", 6)

# Example usage of add_features
# Add new features to the cat named "Simba"
# Passing multiple features as a list
add_features("Simba", ["fearless", "loves to purr"])

# Passing a single feature
add_features("Simba", "likes to cuddle")

# Example usage of delete
# Delete the document for the cat named "Fluffy"
delete("Fluffy")

# Example usage of delete_all
# Delete all documents from the collection
delete_all()
