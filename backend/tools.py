import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "claimpilot.db")

def get_claim_info(claim_id: int) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = """
        SELECT u.name, c.status, c.claim_amount 
        FROM claims c
        JOIN users u ON c.user_id = u.id
        WHERE c.id = ?
    """
    
    cursor.execute(query, (claim_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        name, status, amount = result
        return f"Claim #{claim_id} for {name} is currently '{status}' with an amount of ${amount:,.2f}."
        return "Claim not found in database."

def update_claim_status(claim_id: int, new_status: str) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = "UPDATE claims SET status = ? WHERE id = ?"
    cursor.execute(query, (new_status, claim_id))
    
    if cursor.rowcount == 0:
        conn.close()
        return f"Claim #{claim_id} not found in database."
        
    conn.commit()
    conn.close()
    return f"Success! Claim #{claim_id} status updated to '{new_status}'."

if __name__ == '__main__':
    print(get_claim_info(1))
