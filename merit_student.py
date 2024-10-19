import pandas as pd
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    overall_score = db.Column(db.Float)
    year = db.Column(db.Integer)

    def __repr__(self):
        return f"<Student {self.name}>"

# Load the Excel file
df = pd.read_excel('student_performance.xlsx')

# Define the weights for each column
weights = {
    'cgpa': 0.3,
    'academic_performance': 0.2,
    'core_courses_performance': 0.2,
    'hackathon_participation': 0.1,
    'paper_presentations': 0.1,
    'contributions': 0.1
}

# Normalize the values in each column to a common scale (0-100)
for col in weights:
    df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min()) * 100

# Calculate the weighted sum of the normalized values for each student
df['overall_score'] = sum(df[col] * weight for col, weight in weights.items())

# Populate the database with the DataFrame
valid_years = [1, 2, 3, 4]
df_filtered = df[df['year'].isin(valid_years)]

for _, row in df_filtered.iterrows():
    new_student = Student(
        name=row['id'],
        overall_score=row['overall_score'],
        year=row['year']
    )
    db.session.add(new_student)
db.session.commit()
@app.route('/rank_students', methods=['GET'])
def rank_students():
    year = request.args.get('year', type=int)
    print(f"Received request for year: {year}")  # Debugging
    if year and year in valid_years:
        year_df = df_filtered[df_filtered['year'] == year]
        if not year_df.empty:
            top_students = year_df.nlargest(3, 'overall_score')
            top_students_ids = top_students['id'].tolist()
            print(f"Top students: {top_students_ids}")  # Debugging
            return jsonify(top_students_ids)
        return jsonify({'message': 'No students found for the given year.'})
    return jsonify({'message': 'Invalid year entered. Please enter a year between 1 and 4.'})



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
