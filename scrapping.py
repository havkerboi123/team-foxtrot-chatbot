from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from bs4 import BeautifulSoup
from langchain.text_splitter import CharacterTextSplitter

def scrape_and_save_content(urls, file_path):
    # Loop through each URL
    content_list = []
    for url in urls:
        # Load HTML content
        loader = AsyncChromiumLoader([url])
        html_content = loader.load()

        # Transform the document with BeautifulSoup
        bs_transformer = BeautifulSoupTransformer()
        docs_transformed = bs_transformer.transform_documents(html_content)

        # Extract text content from the first page
        text_content = BeautifulSoup(docs_transformed[0].page_content, 'html.parser').get_text()
        content_list.append(text_content)

    # Save the content to the specified file path
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(content_list))

# List of URLs
urls = ["https://teamfoxtrot.pk", "https://teamfoxtrot.pk/about-us.html", "https://teamfoxtrot.pk/our-team.html", "https://teamfoxtrot.pk/blogs.html", "https://teamfoxtrot.pk/contact-us.html"]

# Specify the file path where you want to save the content
file_path = "/Users/muhammadahmed/Desktop/Projects/foxtrot/scrape.txt"

# Call the function to scrape and save content
scrape_and_save_content(urls, file_path)
