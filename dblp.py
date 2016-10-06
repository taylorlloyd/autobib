import requests

def getConferenceEntry(author, conf, year):

  #Generate the full year
  if len(year) == 2:
    if year[0] == '9':
      year = "19"+year
    else:
      year = "20"+year

  #Query DBLP
  query = author + " " + conf + " " + year
  payload = {"q": query, "format": "json"}
  r = requests.get('http://dblp.uni-trier.de/search/publ/api', params=payload)

  #Parse the response
  response = r.json()["result"]
  if response["hits"]["@sent"] != "0":
    hitsarr = response["hits"]["hit"]

    # Put together the venue information if possible
    venue = getConference(hitsarr[0]["info"]["venue"])
    if venue != None:
      hitsarr[0]["info"]["venue"] = venue
    return hitsarr[0]

  return None

def getConference(venue):
  #Cleanup the venue
  venue = venue.split("@")[0].strip()

  payload = {"q": venue, "format": "json"}
  r = requests.get('http://dblp.uni-trier.de/search/venue/api', params=payload)
  response = r.json()["result"]
  if response["hits"]["@sent"] != "0":
    hitsarr = response["hits"]["hit"]
    for hit in hitsarr:
      if hit["info"]["acronym"] == venue:
        return hit

  return None
