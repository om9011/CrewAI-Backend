from scholarly import scholarly


def fetch_and_display_publications(author_id):

    author = scholarly.search_author_id(author_id)
    detailed_author = scholarly.fill(author)

    author_name = detailed_author.get('name', 'Unknown Author')
    author_affiliation = detailed_author.get('affiliation', 'Unknown Affiliation')
    # print(detailed_author)

    publications = []
    if 'publications' in detailed_author:
        # print("Publications:")
        for publication in detailed_author['publications']:
            title = publication['bib'].get('title', 'No Title')
            year = publication['bib'].get('pub_year', 'N/A')
            citation = publication['bib'].get('citation', 'N/A')
            num_citations = publication['bib'].get('num_citations', 0)
            publications.append({"Title": title, "Year": year, "Citation" : citation, "Num_citations" : num_citations})

    # Return author details and publications
    return {
        "Author Name": author_name,
        "Affiliation": author_affiliation,
        "Publications": publications
    }


# Example usage
# print(fetch_and_display_publications(author_id="xYE0PuUAAAAJ"))
