from flask import Flask
from flask import jsonify,render_template, request, redirect


from .utils.selectors import Selector

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    return redirect('home')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    
    
@app.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
        
        # Validacion de Query.
        query = request.args['query']

        # Validacion de cant_documentos.
        cant_documentos = request.args['cant_documentos']

        # Validacion de google_chkbx.
        google_chkbx = request.args['google_chkbx']
        # Validacion de yahoo_chkbx.
        yahoo_chkbx = request.args['yahoo_chkbx']


        print('Data -> ', type(cant_documentos))

        if query == '':
            return jsonify({'rsp':'Query Missing'})
        
        if cant_documentos == '0':
            return jsonify({'rsp':'Docs count is 0'})
        
        if google_chkbx == '0' and yahoo_chkbx == '0':
            return jsonify({'rsp':'Motor Missing'})
        

        search = Selector(query, cant_documentos, google_chkbx, yahoo_chkbx)
        print('Selecting Motors...')
        selected_motors = search.seleccionar_motores()
        print('Motors Selected')

        print('Selecting Documents...')
        selected_documents = search.seleccionar_documentos()
        print(selected_documents)
        print('Documents Selected')
        
        print('Dispatching querys...')
        query_dispatch = search.query_dispatch()
        print(query_dispatch)
        print('Querys dispatched')

        print('Mixing results...')
        result_mix = search.results_mixer()
        print(result_mix)
        print('Results Mixed')

        return jsonify(result_mix)
        