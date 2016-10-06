import re
from dblp import getConferenceEntry

def autocite(cite):
  # Turn the citation into usable search values

  # match citations of the form AuthorCONF06
  p = re.compile("([a-zA-Z][a-z]*)([A-Za-z]*)([0-9]*)")
  match = p.search(cite)
  author = match.group(1)
  conf = match.group(2)
  year = match.group(3)

  # Get the relevant conference paper
  paper = getConferenceEntry(author, conf, year)

  title = "{" + paper["info"]["title"][:-1] + "}"
  authors = formatAuthors(paper["info"]["authors"]["author"])
  year = paper["info"]["year"]
  pages = formatPages(paper["info"]["pages"])
  confname = paper["info"]["venue"]["info"]["venue"]
  confacronym = paper["info"]["venue"]["info"]["acronym"]
  booktitle = extractConferenceName(confname,confacronym)

  #TODO Clean names for conferences, and determine conference location

  # Append to the automatic bibliography
  with open("autobib.bib", "a") as file:
    file.write(unicodeToLatex("@inProceedings{"+cite+",\n"));
    file.write(unicodeToLatex("title = {" + title +"},\n"));
    file.write(unicodeToLatex("author = {" + authors +"},\n"));
    file.write(unicodeToLatex("year = {" + year +"},\n"));
    file.write(unicodeToLatex("booktitle = {" + booktitle +"},\n"));
    file.write(unicodeToLatex("pages = {" + pages +"},\n"));
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

def extractConferenceName(title, acronym):

  #Attempt to build a regex that would match the acronym
  pattern = [char+"[a-z]*" for char in acronym if char.isupper()]
  #Allow lower-case words between acronym words
  pattern = "\\W+([a-z]*\\W+)?".join(pattern)

  pattern = re.compile(pattern)
  match = pattern.search(title)
  if match:
    title = match.group(0)
  else:
    #Our regex attempt failed, try backup cleanup
    if "Symposium on " in title:
      # Drop ACM boilerplate
      title = title.split("Symposium on ")[1]
    if "Workshop on " in title:
      # Drop ACM boilerplate
      title = title.split("Workshop on ")[1]

    if title.startswith("the ") or title.startswith("The "):
      # Drop leading 'the'
      title = title[4:]

    if "(" in title:
      # Drop trailing parens
      title = title.split("(")[0]

  return title.strip()+" ({"+acronym+"})"

def unicodeToLatex(ustring):
  from unidecode import unidecode
  return unidecode(ustring)
