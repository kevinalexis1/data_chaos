from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_results.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de la base de datos para los resultados del cuestionario
class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    openness = db.Column(db.Integer)
    conscientiousness = db.Column(db.Integer)
    extraversion = db.Column(db.Integer)
    agreeableness = db.Column(db.Integer)
    neuroticism = db.Column(db.Integer)

    def to_dict(self):
        return {
            'openness': self.openness,
            'conscientiousness': self.conscientiousness,
            'extraversion': self.extraversion,
            'agreeableness': self.agreeableness,
            'neuroticism': self.neuroticism
        }

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    data = request.json
    new_result = QuizResult(
        openness=data.get('openness'),
        conscientiousness=data.get('conscientiousness'),
        extraversion=data.get('extraversion'),
        agreeableness=data.get('agreeableness'),
        neuroticism=data.get('neuroticism')
    )
    db.session.add(new_result)
    db.session.commit()
    return jsonify({"message": "Quiz results stored successfully!"}), 201


@app.route('/results', methods=['GET'])
def get_results():
    results = QuizResult.query.all()
    return jsonify([result.to_dict() for result in results])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Mueve la creación de las tablas aquí
    app.run(debug=True)
