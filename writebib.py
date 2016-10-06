import re
from dblp import getConferenceEntry

def autocite(cite):
  # Turn the citation into usable search values

  # match citations of the form AuthorCONF06
  p = re.compile("([a-zA-Z][a-z]*)([A-Z]*)([0-9]*)")
  match = p.search(cite)
  author = match.group(1)
  conf = match.group(2)
  year = match.group(3)

  # Get the relevant conference paper
  paper = getConferenceEntry(author, conf, year)

  print(paper)
  title = "{" + paper["info"]["title"] + "}"
  authors = formatAuthors(paper["info"]["authors"]["author"])
  year = paper["info"]["year"]
  pages = formatPages(paper["info"]["pages"])

  #TODO Clean names for conferences, and determine conference location

  # Append to the automatic bibliography
  with open("autobib.bib", "a") as file:
    file.write("@inProceedings{cite,\n");
    file.write("title = {" + title +"},\n");
    file.write("author = {" + authors +"},\n");
    file.write("year = {" + year +"},\n");
    file.write("pages = {" + pages +"},\n");
    file.write("}\n");

def formatName(author):
  index = author.rfind(' ')
  lastName = author[index:].strip()
  firstName = author[:index].strip()
  return "{"+lastName+", "+firstName+"}"

def formatAuthors(authors):
  return " and ".join([formatName(a) for a in authors]);

def formatPages(pages):
  bounds = pages.split("-")
  return bounds[0].strip() + "--" + bounds[1].strip()
