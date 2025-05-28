# search.py
import os

def search_local_courses(query, base_path="courses/"):
    matches = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if query.lower() in file.lower():
                matches.append(os.path.join(root, file))
    return matches
