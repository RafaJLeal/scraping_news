import math
import requests
import os
import shutil

from bs4 import BeautifulSoup
from datetime import timedelta, timezone, datetime
from tempfile import NamedTemporaryFile
from urllib.request import urlopen

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.shortcuts import render, redirect

from news.models import Headline, UserProfile


requests.packages.urllib3.disable_warnings()


@login_required(login_url='/login')
def home(request):
	user_p = UserProfile.objects.get(user=request.user)
	now = datetime.now(timezone.utc)
	time_difference = now - user_p.last_scrape
	time_difference_in_hours = time_difference / timedelta(minutes=60)
	next_scrape = 24 - time_difference_in_hours

	headlines = Headline.objects.filter(userprofile=user_p)

	if not headlines:
		hide_me = False
	else:
		if time_difference_in_hours <= 24:
			hide_me = True
		else:
			hide_me = False

	context = {
		'object_list': headlines,
		'hide_me': hide_me,
		'next_scrape': math.ceil(next_scrape)
	}

	return render(request, "news/home.html", context)


def scrape(request):
	user_p = UserProfile.objects.filter(user=request.user).first()
	user_p.last_scrape = datetime.now(timezone.utc)
	user_p.save()

	session = requests.Session()
	session.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"}
	url = 'https://elpais.com/'

	content = session.get(url, verify=False).content

	soup = BeautifulSoup(content, "html.parser")

	posts = soup.find_all('article', {'class':'articulo'})

	for i in posts:
		try:
			link = i.find_all('a')[1]['href']
			title = i.find_all('a')[1].text
			if title == "\n\n\n\n\n" or title == "\n\n\n\n\n\n":
				title = i.find_all('a')[2].text
			image_source = 'http:' + i.find('img')['data-src']

			# stackoverflow solution

			media_root = settings.MEDIA_ROOT
			local_filename = user_p.user.username + '_' + image_source.split('/')[-1].split("?")[0]
			r = session.get(image_source, stream=True, verify=False)
			with open(local_filename, 'wb') as f:
				for chunk in r.iter_content(chunk_size=1024):
					f.write(chunk)

			current_image_absolute_path = os.path.abspath(local_filename)
			shutil.move(current_image_absolute_path, media_root)

			# end of stackoverflow

			new_headline = Headline()
			new_headline.title = title
			new_headline.url = link
			new_headline.image = local_filename
			new_headline.userprofile = user_p
			new_headline.save()
		except:
			pass
		
	return redirect('/')