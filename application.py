from flask import Flask, render_template, request
import pickle
import pandas as pd
from keyword_extractor import get_trending_searches
import logging

# Configure logging
logging.basicConfig(filename='app_log.log', level=logging.DEBUG)

phrase_generator = pickle.load(open("/config/workspace/model/keyword_extractor.pkl", "rb"))
application = Flask(__name__)
app = application

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/generate_data', methods=['GET', 'POST'])
def gen_data():
    result = None

    try:
        if request.method == 'POST':
            keyword = str(request.form.get("keyword"))
            location = str(request.form.get("location"))
            timeframe = str(request.form.get("timeframe"))

            top_trending_results = phrase_generator(keyword, location, timeframe)

            try:
                if top_trending_results is not None:
                    result = pd.DataFrame(top_trending_results).to_dict(orient='records')
                    logging.info("Generated data successfully.")
                else:
                    result = 'No data'
                    logging.warning("No data found for the specified parameters.")

                return render_template('single_prediction.html', result=result)

            except Exception as e:
                logging.error(f"Error while processing results: {str(e)}")
                return "An error occurred while processing results."

        else:
            return render_template('home.html')

    except Exception as e:
        logging.error(f"Error in data generation: {str(e)}")
        return "An error occurred during data generation."

if __name__ == "__main__":
    app.run(host="0.0.0.0")
