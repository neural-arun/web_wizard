# import the libraries request and from bs4 import BeautifulSoup

# make a class BooksScraper
# inside init method give it a parameter name base_url
# make the self.base_url = base_url
# give the headers to the init method as well. self.headers = {put the headers in here}
#user-agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36

# accept language not available for this specific website.
# method fetch_html
# def a method to fetch the url and give it a parameter url
# it will only give url
# method parse_html
# def a method to parse the url it only make it a tree out of beautiful soup.
# method extract_data
# use a for loop for these data and store them in prper variable name.
# the parent of the record is : tag = "article", class = "product_pod"
# inside the parent i need to scrape child: tag = "p" , class = "star-rating one " and similarly 
# there is a star rating of two three and four and five.
# for name of the book i need tag = "a" and i need text of the title.
# and then i need the price. tag  = "p" class = price_color
# and fromt the same parent i need tag = "p" class = "instock availability."

# method extract_all_pages:
# use a while loop to check and extract all page data.
# while True:
# fetch_html
# parse_html using the above method
# extract data

#for pagination i have next line as tag "a" and for link href = "page-2.html"
# current_url = base_url + next link
# put this current url in the fetch html again and start the loop again 
# if current_url is None:
# break the loop 
# 


#
