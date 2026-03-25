from datetime import datetime

def extraction_entity(user_id, url, title, word_count, text):
    return {
        "user_id" : user_id,
        "url" :url,
        "title" : title,
        "word_count" : word_count,
        "text" : text,
        "created_at" : datetime.utcnow()
    }