from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taller.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Servicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(10), nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_fin = db.Column(db.DateTime)
    
    # Servicios
    balanceo_ruedas = db.Column(db.Integer, default=0)  # 2 o 4 ruedas
    rectificacion_rines = db.Column(db.Integer, default=0)  # cantidad de rines
    valor_rectificacion = db.Column(db.Float, default=0.0)
    despiche = db.Column(db.Integer, default=0)  # cantidad
    montaje_llantas = db.Column(db.Integer, default=0)  # 1 a 5 llantas
    rotaciones = db.Column(db.Integer, default=0)  # 1 o 2 llantas
    nitrogeno = db.Column(db.Boolean, default=False)
    valvulas = db.Column(db.Integer, default=0)
    
    valor_total = db.Column(db.Float, default=0.0)
    
    def tiempo_servicio(self):
        if self.fecha_fin:
            return self.fecha_fin - self.fecha_inicio
        return datetime.utcnow() - self.fecha_inicio

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    servicios = Servicio.query.order_by(Servicio.fecha_inicio.desc()).all()
    return render_template('index.html', servicios=servicios)

@app.route('/nuevo_servicio', methods=['GET', 'POST'])
def nuevo_servicio():
    if request.method == 'POST':
        servicio = Servicio(
            placa=request.form['placa'],
            balanceo_ruedas=int(request.form.get('balanceo_ruedas', 0)),
            rectificacion_rines=int(request.form.get('rectificacion_rines', 0)),
            valor_rectificacion=float(request.form.get('valor_rectificacion', 0)),
            despiche=int(request.form.get('despiche', 0)),
            montaje_llantas=int(request.form.get('montaje_llantas', 0)),
            rotaciones=int(request.form.get('rotaciones', 0)),
            nitrogeno=bool(request.form.get('nitrogeno', False)),
            valvulas=int(request.form.get('valvulas', 0))
        )
        db.session.add(servicio)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('nuevo_servicio.html')

@app.route('/finalizar_servicio/<int:id>')
def finalizar_servicio(id):
    servicio = Servicio.query.get_or_404(id)
    servicio.fecha_fin = datetime.utcnow()
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)