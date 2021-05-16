#!/usr/bin/env python
# coding: utf-8

# In[406]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re
import time


# In[553]:


# Set up executeable path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[543]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page - searching for elements with div tag and (list_text) attribute
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[488]:


# set up html parser

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[489]:


# 10.3.3
slide_elem.find('div', class_='content_title')


# In[490]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[491]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[492]:


# 10.3.4 Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[493]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[494]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[495]:


# Find the relative image url - note the url is incomplete, only partial
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[496]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[497]:


# 10.3.5 Scrape Mars Data: Mars fact
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[498]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# 
# ### Hemispheres

# In[554]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)
html = browser.html

image_soup1 = soup(html, 'html.parser')
results = image_soup1.find_all('div', class_='description')



# In[555]:


# 2. Create a list to hold the images and titles.

hemisphere_image_urls = []
image_title = []
image_urls = []
url_list = []
hemisphere_urls = []


# In[556]:


# 3. Write code to retrieve the image urls and titles for each hemisphere.

for result in results:
    title = result.find('h3').text
    image_title.append(title)
       
print(image_title)

    


# In[557]:


# Retrieve the partial url link for each hemisphere
for text in image_soup1.find_all('div', class_='description'):
    for link in text.find_all('a'):
        url_list.append(link.get('href'))

# Get the absolute url for each hemisphere
for i in url_list:
    url_list = ((url)+(i))
    hemisphere_urls.append(url_list)
         
print('---------------------------') 
print(hemisphere_urls)


# In[558]:


# Visit the url for each hemisphere and get the url of each full image to add to a list
for url in hemisphere_urls:
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')
    img_url_partial = hemisphere_soup.find('img', class_='wide-image').get('src')
    image_urls.append(f'https://marshemispheres.com/{img_url_partial}')
    browser.back()
   


# In[559]:


# Combine the image_title and image_urls into a dictionary
full_image_urls = dict(zip(image_title, image_urls))

# Makes a copy of the dictionary and append to a list
full_image_urls_copy = full_image_urls.copy()
hemisphere_image_urls.append(full_image_urls_copy)


# In[560]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[561]:


# 5. Quit the browser
browser.quit()


# In[ ]:




