import re
import requests
from datetime import date
from gzip import decompress
import asyncio
import os
# from playwright.async_api import async_playwright, Browser, Playwright, Page, APIResponseAssertions
from bs4 import BeautifulSoup


# %%
# bs_xml = BeautifulSoup(bs_data, 'xml')

# # need to figure out which tag we're looking for

# # finds all instance of the tag
# b_unique = bs_xml.find_all('loc')

# #extracts attribute of the first instance of the tag
# b_name = bs_xml.find('child', {'name': 'grid_block?'})

# # extracting data stored in a specific attribute of the child
# data_info = b_name.get('data-tc-analytics')
# %%
# r = requests.get('https://www.farfetch.com/sitemaps/sitemaps-farfetch-com/us-sitemap-products-1.xml.gz')
# bs_xml = BeautifulSoup(decompress(r.content), 'xml')

# # product_list = []

# loc_elements = bs_xml.find_all('loc')
# print(loc_elements[0])
# print(len(loc_elements))
# # for i in range(1:len(xmlfile)):
# #     b_unique = bs_xml.find_all('loc')
# %%
def get_public_ip():
    params = {
        'format': 'json',
    }

    response = requests.get('https://api.ipify.org', params=params)
    return response.body


# %%
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
url = 'https://www.farfetch.com/sitemaps/sitemaps-farfetch-com/us-sitemap-products-1.xml.gz'
r = requests.get(url, headers=headers)

print(get_public_ip())
if r.status_code == 200:
    # Decompress the gzip content
    content = decompress(r.content)

    # Parse the XML content with BeautifulSoup
    bs_xml = BeautifulSoup(content, 'lxml')

    # Find all 'loc' elements
    loc_elements = bs_xml.find_all('loc')

    # Optional: Print the first 'loc' element and the total number of 'loc' elements
    if loc_elements:
        print(loc_elements[0].text)
    print(len(loc_elements))
else:
    print("Failed to retrieve the data")
    print(r.status_code)

# %%
small_loc_elements = loc_elements[4]

tags = ['a', 'p', 'li']

for element in small_loc_elements:
    print(element)
    print(get_public_ip())
    r = requests.get(element.text, headers=headers)
    print(r.status_code)
    variable = r.content

    html_string = variable.decode('utf-8')
    soup = BeautifulSoup(html_string, 'html.parser')
    # s = soup.find('div', class_ = 'ltr-1vr8bhw')
    s = soup.find('div', class_='ltr-ukwwcv')
    s2 = s.find('div', class_='ltr-1vr8bhw')

    if s2 is not None:
        lines = s2.find_all(tags)
        for index, line in enumerate(lines):
            print(str(index) + line.text)
    else:
        print("Div not found for URL:", element.text)

    # lines = s.find_all(tags)
    # for line in lines:
    #     print(line.text)

    # print(html_string)
    # fullname = 'ooogabooga.txt'
    # open(f'{fullname}','w',encoding='utf-8').write(html_string)


# %%
# import requests
# from bs4 import BeautifulSoup

# small_loc_elements = loc_elements[1]  # Assuming loc_elements is already defined
# tag_contents = {tag: [] for tag in tags}  # Dictionary to store text by tags


def tag_content_creator(tags, elements_list):
    # tag_contents = {tag: [] for tag in tags}  # Dictionary to store text by tags
    # cwd = os.getcwd()
    for element in elements_list:
        r = requests.get(element.text, headers=headers)
        print(r.status_code)
        response = r.content  # Fetch the page content
        html_string = response.decode('utf-8')  # Decode the content to string
        soup = BeautifulSoup(html_string, 'html.parser')  # Parse HTML
        # print(html_string.status_code)
        target_div = soup.find('div', class_='ltr-ukwwcv')  # Find the specific div
        target_div_child = target_div.find('div', class_='ltr-1vr8bhw')
        # print(response.status_code)

        if target_div_child:  # Check if the target div is found
            for tag in tags:
                lines = target_div_child.find_all(tag)  # Find all elements for each tag
                for line in lines:
                    with open('farfetch_info.tsv', 'w', encoding='utf-8') as f:
                        if 'Sorry' in line.text:
                            f.write(element + '\t' + 'Sold Out' + '\n')
                        else:
                            f.write(element + '\t' + line.text + '\n')

    return
    #                 tag_contents[tag].append(line.text)  # Append the text to the respective tag list
    # return tag_contents


# %%
tags = ['a', 'p', 'li']

print(tag_content_creator(tags, small_loc_elements))

# %%
small_loc_elements = loc_elements[0:3]
# %%
print(small_loc_elements)
# %%
from bs4 import BeautifulSoup

# Example HTML content in bytes
html_bytes = b"<html><head><title>Example Page</title></head><body><p>Hello, world!</p></body></html>"

# Decode the bytes to a string, assuming the encoding is UTF-8
html_string = html_bytes.decode('utf-8')

# Parse the string using BeautifulSoup
soup = BeautifulSoup(html_string, 'html.parser')

# Now you can work with `soup` to find elements, navigate the tree, etc.
print(soup.title.text)  # Output: Example Page

# %%
# import requests
# from bs4 import BeautifulSoup
# import gzip
# from io import BytesIO

# # Send a GET request to the URL
# url = 'https://www.farfetch.com/sitemaps/sitemaps-farfetch-com/us-sitemap-products-1.xml.gz'
# print(f"Sending request to {url}")

# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
# r = requests.get(url, headers=headers)
# print(f"Received response with status code: {r.status_code}")

# # Check if the response was successful
# if r.status_code == 200:
#     print("Decompressing the content")
#     # Decompress the gzip content
#     content = gzip.decompress(r.content)
#     print(f"Decompressed content length: {len(content)}")

#     # Parse the XML content with BeautifulSoup
#     print("Parsing content with BeautifulSoup")
#     bs_xml = BeautifulSoup(content, 'lxml')

#     # Find all 'loc' elements
#     print("Finding all 'loc' elements")
#     loc_elements = bs_xml.find_all('loc')

#     # Print the first 'loc' element, if it exists
#     if loc_elements:
#         print(f"First 'loc' element: {loc_elements[0].text}")
#     else:
#         print("No 'loc' elements found")

#     # Print the total number of 'loc' elements found
#     print(f"Total number of 'loc' elements found: {len(loc_elements)}")
# else:
#     print("Failed to retrieve the data")

# %%
tag_contents = {tag: [] for tag in tags}  # Dictionary to store text by tags
for element in small_loc_elements:
    response = requests.get(element.text, headers=headers)  # Fetch the page content
    html_string = response.content.decode('utf-8')  # Decode the content to string
    soup = BeautifulSoup(html_string, 'html.parser')  # Parse HTML
    target_div = soup.find('div', class_='ltr-1vr8bhw')  # Find the specific div

    if target_div:  # Check if the target div is found
        for tag in tags:
            lines = target_div.find_all(tag)  # Find all elements for each tag
            for line in lines:
                tag_contents[tag].append(line.text)  # Append the text to the respective tag list

print(tag_contents)
# %%
tags = ['a', 'p', 'li']

element_range = [i for i in range(len(small_loc_elements))]

farf_link_dict = {n: tag_content_creator(tags, small_loc_elements) for n in element_range}

print(farf_link_dict)

# for i in range(len(small_loc_elements)):
#     print(i)
# %% md

# %%
def create_value_dict(number):
    return {'square': number ** 2, 'cube': number ** 3}


numbers = [1, 2, 3, 4, 5]  # This is the list of numbers

# Using dictionary comprehension with a function
result_dict = {n: create_value_dict(n) for n in numbers}

print(result_dict)


# https: // mattermost.com / blog / how - to - scrape - website - data - using - python /
#
# Python
# Tutorial: Web
# Scraping
# with Requests - HTML --> https://
#     www.youtube.com / watch?v = a6fIbtFB46g
#
# Python
# Requests
# Tutorial: Request
# Web
# Pages, Download
# Images, POST
# Data, Read
# JSON, and More --> https: // www.youtube.com / watch?v = tb8gHvYlCFs