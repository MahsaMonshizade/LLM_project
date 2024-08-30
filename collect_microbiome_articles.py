from Bio import Entrez

# Set your email address to be used with the PubMed API
Entrez.email = "your_actual_email@example.com"

# Define your search query
query = "gut microbiome AND mental health"

# Perform the search
handle = Entrez.esearch(db="pubmed", term=query, retmax=100, retmode="xml", datetype="pdat", mindate="2019/01/01", maxdate="2024/01/01")
record = Entrez.read(handle)
id_list = record["IdList"]

# Fetch details for each article
handle = Entrez.efetch(db="pubmed", id=",".join(id_list), retmode="xml")
records = Entrez.read(handle)

# Store results in a structured format
articles = []
for article in records["PubmedArticle"]:
    title = article["MedlineCitation"]["Article"]["ArticleTitle"]
    abstract = article["MedlineCitation"]["Article"]["Abstract"]["AbstractText"][0] if "Abstract" in article["MedlineCitation"]["Article"] else "N/A"
    
    # Check if 'AuthorList' exists and extract authors
    if "AuthorList" in article["MedlineCitation"]["Article"]:
        authors = []
        for author in article["MedlineCitation"]["Article"]["AuthorList"]:
            last_name = author.get("LastName", "N/A")
            fore_name = author.get("ForeName", "N/A")
            authors.append(f"{last_name} {fore_name}")
    else:
        authors = ["N/A"]
    
    journal = article["MedlineCitation"]["Article"]["Journal"]["Title"]
    
    # Check if 'DateCompleted' exists
    if "DateCompleted" in article["MedlineCitation"]:
        date_completed = article["MedlineCitation"]["DateCompleted"]
        pub_date = f"{date_completed.get('Year', 'N/A')}-{date_completed.get('Month', 'N/A')}-{date_completed.get('Day', 'N/A')}"
    else:
        pub_date = "N/A"

    articles.append({
        "title": title,
        "abstract": abstract,
        "authors": authors,
        "journal": journal,
        "publication_date": pub_date
    })

# Print or save the articles
for article in articles:
    print(article)
