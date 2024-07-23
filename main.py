from google_maps_scraper import scrape_google_maps_reviews, parse_google_maps_reviews, save_reviews_to_csv

# Define the restaurant URL and name
url = r"https://www.google.com/maps/place/Maguire's/@33.3011198,-84.5571668,17z/data=!4m8!3m7!1s0x88f494dcba4b9453:0x8c5c1f45f32681e0!8m2!3d33.3011153!4d-84.5545865!9m1!1b1!16s%2Fg%2F1td019vt?entry=ttu"
restaurant_name = 'maguires-family-restaurant'  # Enter the name of the restaurant here

# Scrape the reviews
html = scrape_google_maps_reviews(url)

# Parse the reviews
reviews = parse_google_maps_reviews(html)

# Save the reviews to a CSV file
save_reviews_to_csv(reviews, restaurant_name)
