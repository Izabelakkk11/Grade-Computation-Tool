from flask import Flask, render_template_string, request

app = Flask(__name__)

# HTML and CSS content as a multi-line string
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grade Calculator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #CBC3E3;
            margin: 0;
            padding: 0;
        }
        .container {
            width: 80%;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ADD8E6;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #000000;
        }
        form {
            display: flex;
            flex-direction: column;
        }
        label {
            margin-bottom: 10px;
            font-size: 1.2em;
            color: #000000;
        }
        input[type="text"] {
            padding: 10px;
            font-size: 1em;
            border: 1px solid #ccc;
            border-radius: 4px;
            margin-bottom: 20px;
        }
        button {
            padding: 10px 20px;
            font-size: 1em;
            color: #fff;
            background-color: #007bff;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        p {
            font-size: 1.1em;
            color: #333;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Grade Calculator</h1>
        <form method="post">
            <label for="prelim_grade">Enter your Prelim grade:</label>
            <input type="text" id="prelim_grade" name="prelim_grade" required>
            <button type="submit">Calculate</button>
        </form>
        {% if result %}
        <p>{{ result }}</p>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def calculate_grades():
    result = None
    if request.method == 'POST':
        try:
            # Get the Prelim grade from the user
            prelim_grade = float(request.form['prelim_grade'])
            
            if prelim_grade < 0 or prelim_grade > 100:
                result = "Error: Prelim grade must be between 0 and 100."
            else:
                # Calculate remaining marks needed to pass
                min_midterm = (75 - (0.20 * prelim_grade) - (0.50 * 100)) / 0.30
                min_final = (75 - (0.20 * prelim_grade) - (0.30 * 100)) / 0.50

                # Check if it's possible to pass
                if prelim_grade * 0.20 + 100 * 0.30 + 100 * 0.50 < 75:
                    result = f"Based on your Prelim grade of {prelim_grade}, it's impossible to pass."
                else:
                    result = f"To pass, you need at least a Midterm grade of {max(0, min_midterm):.2f} and a Final grade of {max(0, min_final):.2f}."
        
        except ValueError:
            result = "Error: Please enter a valid numerical Prelim grade."
    
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    app.run(debug=True)