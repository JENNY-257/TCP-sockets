import socket
import threading
import mysql.connector

# Connect to the MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password="admin",  
        database="cst_directory" 
    )

# Query wrapper
def query_database(query, params=(), fetch_all=False):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall() if fetch_all else cursor.fetchone()
    conn.close()
    return result

# Handle each client
def handle_client(client_socket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            print(f"[DEBUG] Received: {data}")
            parts = data.strip().split('|')
            cmd = parts[0]
            response = ""

            if cmd == 'get_email_by_name':
                first, last = parts[1].strip(), parts[2].strip()
                result = query_database(
                    "SELECT email FROM directory WHERE LOWER(first)=LOWER(%s) AND LOWER(last)=LOWER(%s)",
                    (first, last)
                )
                response = f"Email: {result[0]}" if result else " Email not found."

            elif cmd == 'get_email_by_dept':
                dept_no, last = parts[1].strip(), parts[2].strip()
                result = query_database(
                    "SELECT email FROM directory WHERE LOWER(dept_no)=LOWER(%s) AND LOWER(last)=LOWER(%s)",
                    (dept_no, last)
                )
                response = f"Email: {result[0]}" if result else " Email not found."

            elif cmd == 'get_phone':
                first, last = parts[1].strip(), parts[2].strip()
                result = query_database(
                    "SELECT phone FROM directory WHERE LOWER(first)=LOWER(%s) AND LOWER(last)=LOWER(%s)",
                    (first, last)
                )
                response = f"Phone: {result[0]}" if result else " Phone number not found."

            elif cmd == 'list_by_dept':
                dept_no = parts[1].strip()
                results = query_database(
                    "SELECT first, last, role FROM directory WHERE LOWER(dept_no)=LOWER(%s)",
                    (dept_no,),
                    fetch_all=True
                )
                response = '\n'.join([f"{f} {l} - Role: {r}" for f, l, r in results]) if results else "❌ No users in this department."

            else:
                response = " Invalid command."

            client_socket.send(response.encode())

    except Exception as e:
        print(f"[ERROR] {addr}: {e}")
    finally:
        print(f"[DISCONNECTED] {addr}")
        client_socket.close()

# Start server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 9999))
    server.listen(5)
    print(" Server running on port 9999...")

    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == '__main__':
    start_server()
