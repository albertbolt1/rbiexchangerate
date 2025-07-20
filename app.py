from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Read with custom date format
df = pd.read_csv('euro.csv', dayfirst=True)
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
df.set_index('Date', inplace=True)

@app.route('/euro')
def get_euro():
    date_str = request.args.get('date')  # ?date=01/07/2025
    try:
        date = pd.to_datetime(date_str, dayfirst=True)
    except:
        return jsonify({'error': 'Invalid date format. Use DD/MM/YYYY.'}), 400

    if date in df.index:
        euro_value = df.loc[date, 'EURO']
        return jsonify({'date': date_str, 'euro': euro_value})
    else:
        return jsonify({'error': 'Date not found in data.'}), 404

if __name__ == '__main__':
    app.run(debug=True)