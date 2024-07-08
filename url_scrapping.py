from urllib.parse import urljoin
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from bs4 import BeautifulSoup


def extract_urls(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    
    anchor_tags = soup.find_all('a', href=True)
    
    # Extract and normalize URLs
    urls = [urljoin(base_url, anchor['href']) for anchor in anchor_tags]
    
    return urls

website_url = 'https://teamfoxtrot.pk'


loader = AsyncChromiumLoader([website_url])
html_content = loader.load()

bs_transformer = BeautifulSoupTransformer()
docs_transformed = bs_transformer.transform_documents(html_content)

# Extractigg  the dasd  uRLs from the first page (you can loop through all pages if needed)
urls_on_first_page = extract_urls(docs_transformed[0].page_content, website_url)

# Print the extracted URLs
for url in urls_on_first_page:
    print(url)
