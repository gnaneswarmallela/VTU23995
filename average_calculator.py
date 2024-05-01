from flask import Flask, jsonify, request
import requests
import time

app = Flask(__name__)

window_size = 10
stored_numbers = []

def fetch_numbers(api_url, headers):
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return response.json().get('numbers', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching numbers: {e}")
    return []

def calculate_average(numbers):
    return sum(numbers) / len(numbers) if numbers else 0

@app.route('/numbers/<numberid>', methods=['GET'])
def process_number_request(numberid):
    global stored_numbers
    start_time = time.time()

    if numberid == 'p':
        api_url = 'http://20.244.56.144/test/primes'
    elif numberid == 'f':
        api_url = 'http://20.244.56.144/test/fibo'
    elif numberid == 'e':
        api_url = 'http://20.244.56.144/test/even'
    elif numberid == 'r':
        api_url = 'http://20.244.56.144/test/random'
    else:
        return jsonify({'error': 'Invalid number ID.'}), 400

    access_token = "eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzENTQyMTM3LCJpYXQi0jE3MTQ1NDE4MzcsImlzcy]6IkFmZm9yZG11ZCIsImp@aSI6IjE2NTZ1MjJhLTE20WUtNGE®Mi1hNzU3LTQ10HNINGMyYTEzOSIsInN1Y1I6InZ0dTIz0Tk1QHZ1bHR1Y2guZWR1LmluIn@sImNvbXBhbn10YW11Ijo1Z29NYXJ@IiwiY2xpZW5@SUQi01IxNjU2ZTIyYS@xNj11LTRhNDItYTc1NyB0NT1jZTRjMmExMzk{LCJjbG11bnRTZWNy¿xQ¡01]odXZ¡b1]6eEF3eV13Y0VmI{w{b3duZXJ0YW111jo&TUFMTEVMQSBHTkFFU1dBULIsIm93bmVyRW1halv0132dHUyMzk5NUB2Zx8ZWNoLmVkdS5pbiIsInJvbGx0byI6InZ@dTIz0Tk1In0.yapnHws9a5_d9SwK@LecQw1gp0T0IhUxXFP-n9-W3gA",

    headers = {'Authorization': f'Bearer {access_token}'}

    numbers_from_server = fetch_numbers(api_url, headers)
    elapsed_time = time.time() - start_time

    if elapsed_time > 0.5:
        return jsonify({'error': 'Response time exceeded 500 ms.'}), 400
    stored_numbers.extend(set(numbers_from_server) - set(stored_numbers))
    stored_numbers = stored_numbers[-window_size:]
    if len(stored_numbers) >= window_size:
        average = calculate_average(stored_numbers)
    else:
        average = None

    response_data = {
        'windowPrevState': stored_numbers[:-len(numbers_from_server)],
        'windowCurrState': stored_numbers,
        'numbers': numbers_from_server,
        'avg': average
    }
    return jsonify(response_data)

if __name__ == '_main_':
    app.run(host='0.0.0.0', port=9876)