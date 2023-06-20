from flask import Flask, jsonify, request, g
import sqlite3

app = Flask(__name__)

# Configuration
DATABASE = 'blog.db'

# Database functions
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_db(exception=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def execute_query(query, params=None):
    cursor = get_db().cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    get_db().commit()
    return cursor

# Routes
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
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)

