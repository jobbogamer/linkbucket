import requests
import json
from datetime import datetime

class Commit():
	sha1 = ''
	author = ''
	date = None
	message = ''
	url = ''
	
	def __init__(self, json_commit):
		self.sha1 = json_commit['sha']
		self.author = json_commit['commit']['author']['name']
		self.date = datetime.strptime(json_commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ')
		self.message = json_commit['commit']['message']
		self.url = json_commit['html_url']

class Tag():
	name = ''
	commit_url = ''

	def __init__(self, json_tag):
		self.name = json_tag['name']
		self.commit_url = json_tag['commit']['url']

def _make_request(endpoint):
	url = "https://api.github.com/" + endpoint
	response = requests.get(url)
	if (response.ok):
		result = json.loads(response.text or response.content)
		return result
	else:
		return null

def get_tags(owner, repo):
	return _make_request('repos/{0}/{1}/tags'.format(owner, repo))

def get_last_tag(owner, repo):
	tags = get_tags(owner, repo)
	greatest_name = 'v0.0.0'
	latest_tag = None
	for tag in tags:
		if tag['name'] > greatest_name:
			greatest_name = tag['name']
			latest_tag = tag
	return Tag(latest_tag)

def get_commits(owner, repo):
	commits = _make_request('repos/{0}/{1}/commits'.format(owner, repo))
	return commits

def get_latest_commit(owner, repo):
	commits = get_commits(owner, repo)
	latest_date = None
	latest_commit = None
	for commit in commits:
		if commit['commit']['author']['date'] > latest_date:
			latest_date = commit['commit']['author']['date']
			latest_commit = commit
	return Commit(latest_commit)