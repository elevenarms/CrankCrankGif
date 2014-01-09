#coding: utf-8
from bottle import route, error, post, get, run, static_file, abort, redirect, response, request, template
from os import listdir
from os.path import isfile, join

@route('/')
@route('/index.html')
def index():
    return '<a href="/hello">Go to Hello World page</a>'
 
@route('/hello')
def hello():
    return '<h1>HELLO WOLRD</h1>'


@route('/hello')
def hello():
    mypath = '/home/pi/crank/gifs'
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    return '<h1>HELLO WOLRD</h1>'


@route('/hello/:name')
def hello_name(name):
    page = request.GET.get('page', '1')
    return '<h1>HELLO %s <br/>(%s)</h1>' % (name, page)
 
@route('/static/:filename')
def serve_static(filename):
    return static_file(filename, root='/home/arthur/workspace/my_python_codes/src/')
 
@route('/raise_error')
def raise_error():
    abort(404, "error...")
 
@route('/redirect')
def redirect_to_hello():
    redirect('/hello')
 
@route('/ajax')
def ajax_response():
    return {'dictionary': 'you will see ajax response right? Content-Type will be "application/json"'}
 
@error(404)
def error404(error):
    return '404 error !!!!!'
 
@get('/upload')
def upload_view():
    return """
        <form action="/upload" method="post" enctype="multipart/form-data">
          <input type="text" name="name" />
          <input type="file" name="data" />
          <input type="submit" name="submit" value="upload now" />
        </form>
        """    
 
@post('/upload')
def do_upload():
    name = request.forms.get('name')
    data = request.files.get('data')
    if name is not None and data is not None:
        raw = data.file.read() # small files =.=
        filename = data.filename
        return "Hello %s! You uploaded %s (%d bytes). %s" % (name, filename, len(raw), raw)
    return "You missed a field."
 
@route('/tpl')
def tpl():
    return template('test')
 
run(host='0.0.0.0', port=80, reloader=True)