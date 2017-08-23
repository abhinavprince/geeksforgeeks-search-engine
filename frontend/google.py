from googleapiclient.discovery import build
import pprint

my_api_key = "AIzaSyDSV7sQTiD3ztijF4lDaWrJf06mdf0w6aA"
my_cse_id = "008408648827036128353:hfsq9opynu4"


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']


results = google_search('chamber of secrets', my_api_key, my_cse_id, num=10)


output = open("google_results.txt", "w+")

listy=[]

for result in results:
	listy.append(result['formattedUrl'])
	output.write(str(result) + "\n\n\n")
	pprint.pprint(result)

print listy
