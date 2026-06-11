# app/shortener.py

import random
import string

# the characters we'll use to generate short codes
# this gives us 62 possible characters per position
# with 6 characters that's 62^6 = 56 billion possible codes
CHARACTERS = string.ascii_letters + string.digits  # a-z, A-Z, 0-9

def generate_short_code(length: int = 6) -> str:
    # randomly pick `length` characters from CHARACTERS and join them
    # e.g. "aB3xZ9"
    return "".join(random.choices(CHARACTERS, k=length))

def create_short_url(original_url: str, db) -> str:
    # import here to avoid circular imports
    from app.models import URL

    # keep generating codes until we find one that isn't already taken
    # collisions are extremely rare with 56 billion possibilities
    # but we check anyway to be safe
    while True:
        code = generate_short_code()

        # check if this code already exists in the database
        existing = db.query(URL).filter(URL.short_code == code).first()

        if not existing:
            # code is unique — save it and return
            new_url = URL(short_code=code, original_url=original_url)
            db.add(new_url)       # stage the new row
            db.commit()           # write it to the database
            db.refresh(new_url)   # reload the row to get any db-generated values
            return code