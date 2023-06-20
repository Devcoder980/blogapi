from flask import Flask, jsonify, request
import sqlite3
import threading

app = Flask(__name__)

# Create SQLite database and table
def get_connection():
    if 'connection' not in threading.current_thread().__dict__:
        threading.current_thread().connection = sqlite3.connect('blog.db')
    return threading.current_thread().connection

def get_cursor():
    if 'cursor' not in threading.current_thread().__dict__:
        threading.current_thread().cursor = get_connection().cursor()
    return threading.current_thread().cursor

def close_connection(exception):
    connection = threading.current_thread().connection
    connection.close()

app.teardown_appcontext(close_connection)

with app.app_context():
    cursor = get_cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    get_connection().commit()

# Helper function to execute SQL queries
def execute_query(query, params=None):
    cursor = get_cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    get_connection().commit()
    return cursor

@app.route('/posts', methods=['GET'])
def get_posts():
    query = 'SELECT * FROM posts'
    result = execute_query(query).fetchall()
    posts = [{'id': row[0], 'title': row[1], 'content': row[2]} for row in result]
    return jsonify(posts)

@app.route('/posts', methods=['POST'])
def create_post():
    title = request.json['title']
    content = request.json['content']
    query = 'INSERT INTO posts (title, content) VALUES (?, ?)'
    params = (title, content)
    execute_query(query, params)
    post_id = cursor.lastrowid
    new_post = {'id': post_id, 'title': title, 'content': content}
    return jsonify(new_post), 201

@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    query = 'SELECT * FROM posts WHERE id = ?'
    params = (post_id,)
    result = execute_query(query, params).fetchone()
    if result:
        post = {'id': result[0], 'title': result[1], 'content': result[2]}
        return jsonify(post)
    return jsonify({'error': 'Post not found'}), 404

@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    query = 'SELECT * FROM posts WHERE id = ?'
    params = (post_id,)
    result = execute_query(query, params).fetchone()
    if result:
        title = request.json['title']
        content = request.json['content']
        query = 'UPDATE posts SET title = ?, content = ? WHERE id = ?'
        params = (title, content, post_id)
        execute_query(query, params)
        updated_post = {'id': post_id, 'title': title, 'content': content}
        return jsonify(updated_post)
    return jsonify({'error': 'Post not found'}), 404

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    query = 'SELECT * FROM posts WHERE id = ?'
    params = (post_id,)
    result = execute_query(query, params).fetchone()
    if result:
        query = 'DELETE FROM posts WHERE id = ?'
        params = (post_id,)
        execute_query(query, params)
        return jsonify({'message': 'Post deleted'})
    return jsonify({'error': 'Post not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
