import requests
from bs4 import BeautifulSoup
import csv


def fetch_webpage(url):
    """
    Fetch the content of the webpage.

    Args:
    url (str): URL of the webpage to scrape.

    Returns:
    BeautifulSoup object: Parsed HTML content of the page.
    """
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None


def extract_books_data(soup):
    books_data = []
    books = soup.find_all('div', class_='book')

    for book in books:
        try:
            title = book.find('h2').text
            author = book.find('p', class_='author').text
            price = book.find('p', class_='price').text
            books_data.append({'Title': title, 'Author': author, 'Price': price})
        except AttributeError as e:
            print(f"Error parsing book data: {e}")

    return books_data


def save_to_csv(data, filename):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'Author', 'Price']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        print(f"Data has been written to {filename}")
    except IOError as e:
        print(f"Error writing to CSV file: {e}")


def main():
    url = 'http://example.com/books'
    soup = fetch_webpage(url)
    if soup:
        books_data = extract_books_data(soup)
        save_to_csv(books_data, 'books.csv')


if __name__ == '__main__':
    main()
