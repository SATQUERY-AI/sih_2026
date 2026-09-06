def understand_query(query: str) -> dict:

    query = query.strip()

    if not query:
        return {
            "valid": False,
            "query": "",
            "message": "Query cannot be empty."
        }

    return {
        "valid": True,
        "query": query,
        "message": "Query understood successfully."
    }