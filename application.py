from static.partial import _, _1
from static.db_config import db_config
from sanic import Sanic
from sanic import response
from asyncpg import create_pool

res = response
app = Sanic(__name__)

app.static('/', './static')

@app.listener('before_server_start')
async def cr_pool(app, loop):
  app.db = await create_pool(**db_config)

@app.route("/")
async def home(req):
  return _.go(open('./index.html', 'r').read(), res.html)

@app.route('/todos', methods=['POST'])
async def post_todos(req):
  return await _.asy.go(
    req.json,
    _(app.db.fetchrow, 'INSERT INTO todo (body) VALUES ($1) RETURNING *'),
    dict,
    res.json)

@app.route('/todos')
async def get_todos(req):
  return await _.asy.go(
    'SELECT id, body, completed FROM todo ORDER BY id DESC',
    app.db.fetch,
    _.map(_1(dict)),
    res.json)

# //clear_completed
@app.route('/clear_completed', methods=['POST'])
async def clear_completed(req):
  return await _.asy.go(
    app.db.execute('DELETE FROM todo WHERE completed=TRUE'),
    res.json)

# //remove/todos/:id
@app.route('/remove/todos/<id>', methods=['POST'])
async def remove_todos(req, id):
  return await _.asy.go(
    app.db.execute('DELETE FROM todo WHERE id=$1', int(id)),
    res.json)

@app.route('/todos/<id>', methods=['POST'])
async def update_todos(req, id):
  return await _.asy.go(
    app.db.execute('UPDATE todo SET completed = $1 WHERE id=$2', req.json, int(id)),
    res.json)

app.run()