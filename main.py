import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import csv

# URL of the website
#url = input("Enter Website Link: ")
#url = "https://www.dupontregistry.com/autos/results/audi/r8"
#url = "https://www.dupontregistry.com/autos/results/audi/r8/filter:page_start=2"

# Function to clean and split input URLs
def clean_split_urls(urls_input):
    # Remove white spaces around URLs and split by commas
    urls = [url.strip() for url in urls_input.split(',') if url.strip()]
    print(urls)
    return urls

# Input multiple website links separated by commas
urls_input = input("Enter Website Links separated by commas: ")

# Clean and split the input URLs
urls = clean_split_urls(urls_input)

totalPrice = 0
averagePrice = 0
totalMiles = 0
averageMiles = 0
rowCounter = 0
yearArray = []

with open('cars_info.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # Define the CSV writer
    writer = csv.writer(csvfile)
    # Write header row
    writer.writerow(['Year', 'Make & Model', 'Price', 'Mileage', 'City', 'Dealer'])
    
    for url in urls:
        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all elements with class "LilCards-module_bold__2a4-N" and data-test="price"
        price_elements = soup.find_all('span', class_='LilCards-module_bold__2a4-N', attrs={'data-test': 'price'})

        # Find all elements with data-test="mileage"
        mileage_elements = soup.find_all('span', id='miles', attrs={'data-test': 'mileage'})

        # Find all elements with data-test="city"
        city_elements = soup.find_all('div', class_='LilCards-module_grey_text__QyaiZ', attrs={'data-test': 'city'})

        # Find all elements with class "LilCards-module_product_item_h3__879c7" for dealer info
        dealer_elements = soup.find_all('h3', class_='LilCards-module_grey_text__QyaiZ LilCards-module_product_item_h3__879c7')

        # Find all elements with class "LilCards-module_title__Rnfg5" for car title and link
        title_elements = soup.find_all('a', class_='LilCards-module_title__Rnfg5')

        # Extract and write the title, price, mileage, city, and dealer for each element
        for title_element, price_element, mileage_element, city_element, dealer_element in zip(title_elements, price_elements, mileage_elements, city_elements, dealer_elements):
            title_parts = title_element.span.get_text(strip=True).split(' ')
            year = title_parts[0]
            make_model = ' '.join(title_parts[1:])
            price = price_element.get_text(strip=True)
            mileage = mileage_element.get_text(strip=True)
            if mileage == "Call for":
                mileage = "NA"
            city = city_element.get_text(strip=True)
            dealer = dealer_element.get_text(strip=True)
            # Write year, make_model, price, mileage, city, and dealer to the CSV file
            
            if city != "":
                writer.writerow([year, make_model, price, mileage, city, dealer])
                
                priceInt = float(price.replace(",", ""))
                totalPrice += priceInt
                
                if mileage != "NA":
                    mileageInt = float(mileage.replace(",", ""))
                    totalMiles += mileageInt
                    yearArray.append({'year': year, 'price': priceInt, 'mileage': mileageInt})
                else:
                    yearArray.append({'year': year, 'price': priceInt, 'mileage': -1})
                    
                rowCounter += 1
            

#averagePrice = totalPrice / rowCounter
#averageMiles = totalMiles / rowCounter

#print("averagePrice: ", averagePrice)
#print("averageMiles", averageMiles)

for item in yearArray:
    print("{year: \"" + item['year'] + "\", price: \"" + str(item['price']) + "\", mileage: \"" + str(item['mileage']) + "\"}")
    

# Dictionary to store total price, total mileage, and count for each year
year_stats = defaultdict(lambda: {'total_price': 0, 'total_mileage': 0, 'count': 0})

# Iterate through the yearArray
for item in yearArray:
    # Add the price to the total price for the corresponding year
    year_stats[item['year']]['total_price'] += item['price']
    # Add the mileage to the total mileage for the corresponding year
    if item['mileage'] != -1:  # Check if mileage is not NA
        year_stats[item['year']]['total_mileage'] += item['mileage']
    # Increment the count for the corresponding year
    year_stats[item['year']]['count'] += 1

# Dictionary to store average price and mileage for each year
average_stats = {}

# Calculate the average price and mileage for each year
for year, stats in year_stats.items():
    # If count is not zero, calculate average price and mileage
    if stats['count'] != 0:
        average_stats[year] = {
            'average_price': stats['total_price'] / stats['count'],
            'average_mileage': stats['total_mileage'] / stats['count']
        }

# Print the average price and mileage for each year
for year, avg_stats in average_stats.items():
    print("Year:", year)
    print("Average Price:", avg_stats['average_price'])
    print("Average Mileage:", avg_stats['average_mileage'])
    print()
    
# Re-open the CSV file in append mode
with open('cars_info.csv', 'a', newline='', encoding='utf-8') as csvfile:
    # Define the CSV writer
    writer = csv.writer(csvfile)

    # Calculate the average price and mileage for each year
    for year, stats in year_stats.items():
        # If count is not zero, calculate average price and mileage
        if stats['count'] != 0:
            average_price = stats['total_price'] / stats['count']
            average_mileage = stats['total_mileage'] / stats['count']
            # Write year, make_model, average price, and average mileage to the CSV file
            writer.writerow([year, 'Average', average_price, average_mileage, '', ''])


    
    
    
# # Find the index of the h2 element with class "Autos_page_title__ztS9c"
# h2_index = -1
# for index, element in enumerate(soup.find_all('h2', class_='Autos_page_title__ztS9c')):
#     if "Most Expensive" in element.text:
#         h2_index = index
#         break

# # If h2_index is found, filter the price, mileage, city, dealer, and title elements
# if h2_index != -1:
#     price_elements = price_elements[h2_index:]
#     mileage_elements = mileage_elements[h2_index:]
#     city_elements = city_elements[h2_index:]
#     dealer_elements = dealer_elements[h2_index:]
#     title_elements = title_elements[h2_index:]