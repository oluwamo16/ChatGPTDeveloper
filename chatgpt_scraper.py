import requests
from bs4 import BeautifulSoup
import sys

# Get the URL and file type from the command line arguments
if len(sys.argv) != 3:
    print("Error: missing arguments")
    sys.exit(1)
url = sys.argv[1]
file_type = sys.argv[2]

while True:
    try:
        # Send an HTTP GET request to the website
        response = requests.get(url)

        # Parse the HTML of the website
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all the links with the `movie-link` id
        links = soup.find_all("a", id="movie-link")

        # Download the links if they match the file type
        for link in links:
            if link["href"].endswith(file_type):
                # Get the file name from the link text
                file_name = link.text.strip()

                # Send an HTTP GET request to download the file
                file_response = requests.get(link["href"])

                # Save the file to the current directory
                open(file_name, "wb").write(file_response.content)

        # Find the next link to follow
        next_link = soup.find("a", class_="next-link")
        if next_link:
            # If a next link was found, follow it
            url = next_link["href"]
        else:
            # If no next link was found, stop the loop
            break
    except Exception as e:
        # Print the error and continue the loop
        print(f"Error: {e}")
        continue
