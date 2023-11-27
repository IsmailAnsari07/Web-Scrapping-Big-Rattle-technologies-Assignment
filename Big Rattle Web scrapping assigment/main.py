import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function to scrape data from an individual notice page
def scrape_notice(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extracting relevant information
        name_element = soup.find('span', {'class': 'heading-h3'})
        name = name_element.text.strip() if name_element else None

        wanted_by_element = soup.find('div', {'class': 'clearfix wanted-by'})
        wanted_by = wanted_by_element.text.strip() if wanted_by_element else None

        identity_particulars_element = soup.find('div', {'class': 'identity-particulars-content'})
        identity_particulars = identity_particulars_element.text.strip() if identity_particulars_element else None

        details_element = soup.find('div', {'class': 'details-content'})
        details = details_element.text.strip() if details_element else None

        charges_element = soup.find('div', {'class': 'charges-content'})
        charges = charges_element.text.strip() if charges_element else None

        # Extracting images
        images = [img['src'] for img in soup.find_all('img', {'class': 'img-responsive'})]

        print(f"Debug: Extracted data for {url}: {name}, {wanted_by}, {identity_particulars}, {details}, {charges}, {images}")

        return {'Name': name, 'Wanted By': wanted_by, 'Identity Particulars': identity_particulars,
                'Details': details, 'Charges': charges, 'Images': images}
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

# Function to scrape all notices
def scrape_all_notices(base_url, total_notices, delay=1):
    all_data = []
    for notice_id in range(1, total_notices + 1):
        notice_url = f'{base_url}#{notice_id}'
        notice_data = scrape_notice(notice_url)

        if notice_data is not None:
            all_data.append(notice_data)
            print(f'Scraped data for notice {notice_id}')

        time.sleep(delay)  # Introduce a delay between requests to be polite to the server

    return all_data

# Main function to run the scraper
def main():
    base_url = 'https://www.interpol.int/en/How-we-work/Notices/View-Red-Notices'
    total_notices = 7000

    # Scraping all notices with a delay of 1 second between requests
    all_data = scrape_all_notices(base_url, total_notices, delay=1)

    # Creating a pandas DataFrame
    df = pd.DataFrame(all_data)

    # Saving data to a CSV file
    csv_file_path = 'interpol_notices.csv'
    df.to_csv(csv_file_path, index=False)
    print(f'Data saved to {csv_file_path}')

if __name__ == "__main__":
    main()
