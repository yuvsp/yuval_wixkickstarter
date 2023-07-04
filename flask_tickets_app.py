from flask import Flask, jsonify, render_template
import pandas as pd
import json

app = Flask(__name__)


@app.route('/tickets', methods=['GET'])
def get_tickets():
    try:
        # Read the JSON file
        with open('data.json', 'r', encoding='utf-8') as f:
            tickets = json.load(f)

        # Organize the input data into a pandas data-frame
        df = pd.json_normalize(tickets)
        return render_template('dataframe.html',msg='',column_names=df.columns.values, row_data=list(df.values.tolist()),zip=zip)

    except Exception as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)


if __name__ == '__main__':
    app.run()
