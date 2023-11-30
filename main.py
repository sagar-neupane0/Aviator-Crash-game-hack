from flask import Flask, render_template, request
import hashlib

app = Flask(__name__)

def generate_results(seed, round_value, round_number):
    try:
        # Generate the value for the next round
        result_next_round = (round_value * round_number) % 10.01
        
        # Generate the value for the second next round
        seed_concatenated = seed + str(result_next_round)
        hash_result = hashlib.sha512(seed_concatenated.encode()).hexdigest()
        result_next_round2 = int(hash_result, 16) % 10.01
        
        return result_next_round, result_next_round2
    except Exception as e:
        return f"Error: {str(e)}", None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            seed = request.form['seed']
            round_value = float(request.form['round_value'])
            round_number = int(request.form['round_number'])
            
            result_next_round, result_next_round2 = generate_results(seed, round_value, round_number)
            
            if result_next_round is not None and result_next_round2 is not None:
                return render_template('results.html', result_next_round=result_next_round, result_next_round2=result_next_round2)
            else:
                return render_template('error.html', error_message=result_next_round)
        except Exception as e:
            return render_template('error.html', error_message=f"Error: {str(e)}")
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)