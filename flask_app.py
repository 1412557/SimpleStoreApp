from datetime import datetime


from domain import model, events, commands
from adapters import orm
from flask import Flask, request, jsonify, render_template
from service import messagebus, unit_of_work

orm.start_mappers()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
    try:
        command = commands.Allocate(
            request.json['orderid'], request.json['sku'],
            request.json['qty'],
        )
        result = messagebus.MessageBus(unit_of_work.SqlAlchemyUnitOfWork()).handle(command)
        batchref = result.pop(0)

    except model.OutOfStock as e:
        return jsonify({'message': str(e)}), 400
    return jsonify({'batchref': batchref}), 201


@app.route("/add_batch", methods=['POST'])
def add_batch():
    eta = request.form['eta']
    if eta is not None:
        try:
            eta = datetime.fromisoformat(eta).date()
        except ValueError:
            eta = None

    command = commands.CreateBatch(
        request.form['ref'], request.form['sku'],
        int(request.form['qty']), eta,
    )
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    messBus = messagebus.MessageBus(uow)
    messBus.handle(command)
    return 'OK', 201
