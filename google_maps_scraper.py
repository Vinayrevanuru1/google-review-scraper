import argparse
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    return driver

def get_html_content(driver, url):
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde")))
    return driver.page_source

def click_more_buttons(driver):
    more_buttons = driver.find_elements(By.CSS_SELECTOR, 'button.w8nwRe.kyuRq[aria-expanded="false"]')
    for button in more_buttons:
        driver.execute_script("arguments[0].click();", button)

def scroll_and_collect_reviews(driver):
    element = driver.find_element(By.CSS_SELECTOR, "div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde")
    last_height = driver.execute_script("return arguments[0].scrollHeight", element)
    while True:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", element)
        time.sleep(random.uniform(3, 4))  # Random sleep to mimic human behavior
        click_more_buttons(driver)
        new_height = driver.execute_script("return arguments[0].scrollHeight", element)
        if new_height == last_height:
            break
        last_height = new_height
        print("Scrolling...")

def scrape_google_maps_reviews(url):
    driver = setup_driver()
    html_content = get_html_content(driver, url)
    scroll_and_collect_reviews(driver)
    html = driver.page_source
    driver.quit()
    return html

def parse_google_maps_reviews(html):
    soup = BeautifulSoup(html, 'html.parser')
    reviews = soup.find_all('div', attrs={'data-review-id': True})

    data = []

    for review in reviews:
        review_id = review['data-review-id']
        reviewer_name = review.find('div', class_='d4r55').text if review.find('div', class_='d4r55') else None
        reviewer_profile_link = review.find('button', class_='WEBjve')['data-href'] if review.find('button', class_='WEBjve') else None
        review_date = review.find('span', class_='rsqaWe').text if review.find('span', class_='rsqaWe') else None
        rating_span = review.find('span', class_='kvMYJc')
        rating = int(rating_span['aria-label'].split()[0]) if rating_span and 'aria-label' in rating_span.attrs else None
        review_text = review.find('span', class_='wiI7pd').text if review.find('span', class_='wiI7pd') else None
        photo_count = len(review.find_all('button', class_='Tya61d'))
        like_count = None  # Assuming there's a method to extract this if available
        response = review.find('div', class_='wiI7pd', lang='en').text if review.find('div', class_='wiI7pd', lang='en') else None
        response_date = review.find('span', class_='DZSIDd').text if review.find('span', class_='DZSIDd') else None

        data.append({
            'Review ID': review_id,
            'Reviewer Name': reviewer_name,
            'Reviewer Profile Link': reviewer_profile_link,
            'Review Date': review_date,
            'Rating': rating,
            'Review Text': review_text,
            'Photo Count': photo_count,
            'Like Count': like_count,
            'Response from Owner': response,
            'Response Date': response_date
        })

    return data

def save_reviews_to_csv(reviews, restaurant_name):
    df = pd.DataFrame(reviews)
    df.to_csv(f'{restaurant_name}_google_reviews.csv', index=False)
    print(f'Reviews saved to {restaurant_name}_google_reviews.csv')

def main(url, restaurant_name):
    html = scrape_google_maps_reviews(url)
    reviews = parse_google_maps_reviews(html)
    save_reviews_to_csv(reviews, restaurant_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape Google Maps reviews.')
    parser.add_argument('--url', type=str, required=True, help='The URL of the Google Maps page.')
    parser.add_argument('--name', type=str, required=True, help='The name of the restaurant.')
    args = parser.parse_args()
    
    main(args.url, args.name)
