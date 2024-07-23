import argparse
from google_maps_scraper import scrape_google_maps_reviews, parse_google_maps_reviews, save_reviews_to_csv

def main(url, restaurant_name):
    # Scrape the reviews
    html = scrape_google_maps_reviews(url)

    # Parse the reviews
    reviews = parse_google_maps_reviews(html)

    # Save the reviews to a CSV file
    save_reviews_to_csv(reviews, restaurant_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape Google Maps reviews.')
    parser.add_argument('--url', type=str, required=True, help='The URL of the Google Maps page.')
    parser.add_argument('--name', type=str, required=True, help='The name of the restaurant.')
    args = parser.parse_args()
    
    main(args.url, args.name)
