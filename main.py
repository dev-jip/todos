from sanic import Sanic
from sanic import response
from partial import _, __, ___, _1
from pg import db_config

app = Sanic(__name__)

app.static('/', './static')

@app.listener('before_server_start')
async def cr_pool(app, loop):
  app.db = await db_config()

@app.route("/")
async def home(req):
  return _.go(open('./index.html', 'r').read(), response.html)

@app.route('/todos', methods=['POST'])
async def post_todos(req):
  return await _.asy.go(
    req.json,
    _(app.db.fetchrow, 'INSERT INTO todo (body) VALUES ($1) RETURNING *'),
    dict,
    response.json)

@app.route('/todos')
async def get_todos(req):
  return await _.asy.go(
    'SELECT id, body, completed FROM todo ORDER BY id DESC',
    app.db.fetch,
    _.map(_1(dict)),
    response.json)

# //clear_completed
@app.route('/clear_completed', methods=['POST'])
async def clear_completed(req):
  return await _.asy.go(
    app.db.execute('DELETE FROM todo WHERE completed=TRUE'),
    response.json)

# //remove/todos/:id
@app.route('/remove/todos/<id>', methods=['POST'])
async def remove_todos(req, id):
  return await _.asy.go(
    app.db.execute('DELETE FROM todo WHERE id=$1', int(id)),
    response.json)

@app.route('/todos/<id>', methods=['POST'])
async def update_todos(req, id):
  return await _.asy.go(
    app.db.execute('UPDATE todo SET completed = $1 WHERE id=$2', req.json, int(id)),
    response.json)

app.run(host="0.0.0.0", port=8001, debug=True)