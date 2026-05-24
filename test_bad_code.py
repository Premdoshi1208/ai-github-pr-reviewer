password = "admin123"

def get_user_data(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    print(query)
    return query
