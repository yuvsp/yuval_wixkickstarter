from flask import Flask, jsonify, render_template, request
import pandas as pd
import json
from datetime import datetime

app = Flask(__name__)

def json_to_dataframe(file):
    # Read the JSON file
    with open(file, 'r', encoding='utf-8') as f:
        tickets = json.load(f)

    # Organize the input data into a pandas data-frame
    df = pd.json_normalize(tickets)

    # Extract epoc time string data from creationTime column to consist of meaningful time object
    df['creationTime'] = pd.to_datetime(df['creationTime'], unit='ms')
    return df


@app.route('/tickets', methods=['GET'])
def get_tickets():
    try:
        # Read and Organize the JSON file
        tickets = json_to_dataframe('data.json')
        return render_template('dataframe.html',msg='',column_names=tickets.columns.values, row_data=list(tickets.values.tolist()),zip=zip)

    except Exception as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)


@app.route('/tickets/title', methods=['GET'])
def filter_tickets_title():
    try:
        # Read and Organize the JSON file
        filtered_tickets = json_to_dataframe('data.json')

        # Get query parameters from the request
        title = request.args.get('title')

        # Apply filters to the DataFrame
        if title:
            filtered_tickets = filtered_tickets[filtered_tickets['title'] == title]

        return render_template('dataframe.html',msg='',column_names=filtered_tickets.columns.values, row_data=list(filtered_tickets.values.tolist()),zip=zip)

    except Exception as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)

@app.route('/tickets/date', methods=['GET'])
def filter_tickets_date():
    try:
        # Read and Organize the JSON file
        filtered_tickets = json_to_dataframe('data.json')

        # Get query parameters from the request
        fromdate = request.args.get('from')
        todate = request.args.get('to')

        # fromdate = datetime.strptime(fromdate, '%Y-%m-%d')
        # todate = datetime.strptime(todate, '%Y-%m-%d')

        # Apply filters to the DataFrame
        if fromdate:
            filtered_tickets = filtered_tickets[filtered_tickets['creationTime'] >= fromdate]
        if todate:
            filtered_tickets = filtered_tickets[filtered_tickets['creationTime'] <= todate]

        return render_template('dataframe.html',msg='',column_names=filtered_tickets.columns.values, row_data=list(filtered_tickets.values.tolist()),zip=zip)

    except Exception as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run()
