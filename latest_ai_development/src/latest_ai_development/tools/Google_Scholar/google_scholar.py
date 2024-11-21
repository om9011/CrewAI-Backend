from scholarly import scholarly
from langchain_core.tools import tool

@tool
def fetch_and_display_publications(author_id):
    """
    Fetch an author's profile and publications using Google_Scholar, then display them.

    Args:
    - author_id (str): The unique Google_Scholar ID for the author.

    Returns:
    - dict: A dictionary containing the author's details and their publications.
    """
    try:
        # Fetch the author's profile using their Google_Scholar ID
        # print(f"Fetching publications for author ID: {author_id}\n")
        author = scholarly.search_author_id(author_id)
        detailed_author = scholarly.fill(author)  # Fill in detailed information

        # Display author details
        author_name = detailed_author.get('name', 'Unknown Author')
        author_affiliation = detailed_author.get('affiliation', 'Unknown Affiliation')

        # Collect publications
        publications = []
        if 'publications' in detailed_author:
            # print("Publications:")
            for publication in detailed_author['publications']:
                title = publication['bib'].get('title', 'No Title')
                year = publication['bib'].get('pub_year', 'N/A')
                publications.append({"Title": title, "Year": year})
                # print(f"- {title} ({year})")

        # Return author details and publications
        return {
            "Author Name": author_name,
            "Affiliation": author_affiliation,
            "Publications": publications
        }

    except Exception as e:
        # print(f"Error fetching author data: {e}")
        return {"error": str(e)}


# Example usage
# print(fetch_and_display_publications(author_id="xYE0PuUAAAAJ"))
