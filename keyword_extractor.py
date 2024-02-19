from pytrends.request import TrendReq
import time
import logging

# Configure logging
logging.basicConfig(filename='keyword_extractor_log.log', level=logging.DEBUG)

def get_trending_searches(keyword, location, timeframe):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=location, gprop='youtube')

    # Introduce a delay to avoid rate limiting issues
    time.sleep(2)

    try:
        trending_data = pytrends.related_queries()

        if trending_data is not None and keyword in trending_data and trending_data[keyword]['top'] is not None:
            top_trending = trending_data[keyword]['top'].head(20).reset_index(drop=True)
            top_trending['date'] = pytrends.interest_over_time().index.strftime('%Y-%m-%d')[0]
            logging.info(f"Retrieved top trending queries for {keyword}.")
            return top_trending
        else:
            logging.warning(f"No top trending queries found for {keyword} in the specified timeframe and location.")
            return None

    except Exception as e:
        logging.error(f"Error in get_trending_searches: {str(e)}")
        return None
