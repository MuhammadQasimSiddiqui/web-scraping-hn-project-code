# CREATING A WEB SCRAPE PROJECT THAT ONLY DISPLAYS US THE HACKER NEWS CONTENT FROM THE FIRST 2 NEWS PAGE THAT HAVE MORE THAN OR EQUAL TO ATLEAST A 100 VOTES. SO THAT WE FOCUS ONLY ON THE IMPORTANT CATRGORIZED NEWS

# Importing the required modules
import requests
import pprint
from bs4 import BeautifulSoup

# requesting the data from hacker news
res = requests.get('https://news.ycombinator.com/news')
res2 = requests.get('https://news.ycombinator.com/news?p=2')
print(f'The response from the hacker news server page 1 is {res.status_code}')
print(f'The response from the hacker news server page 2 is {res2.status_code}')

# creating the soup object via soup variable
soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

# using css selectors to grab the required classes
links = soup.select('.titleline > a')
links2 = soup2.select('.titleline > a')
subtext = soup.select('.subtext')
subtext2 = soup2.select('.subtext')

# merging the two pages together
merged_links = links + links2
merged_subtext = subtext + subtext2

# creating a simple function that returns highest voted title first and then the least with a minimum of 100 votes
def sorted_points_wise_fn(hnlist):
	return sorted(hnlist, key = lambda k: k['total_votes'], reverse = True)

# creating a function to make the custom hacker news with minimum of a 100 votes 
def create_custom_hacker_news(merged_links, merged_subtext):
	hn = [] # we will append to this empty list our custom news
	for indx, items in enumerate(merged_links):
		title = items.getText()
		href = items.get('href', None)
		vote = merged_subtext[indx].select('.score')
		# now checking if votes exist
		if len(vote):
			points = int(vote[0].getText().replace(' points', ''))
			# only selecting links with minimum or equal to 100 points
			if points > 99:
				hn.append({'title': title, 'title_link': href, 'total_votes': points})

	return sorted_points_wise_fn(hn)

# calling the function and pretty printing the results
pprint.pprint(create_custom_hacker_news(merged_links, merged_subtext))