from external_apis import readability
from database import db

class Link(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	url = db.Column(db.String)
	title = db.Column(db.String)
	date = db.Column(db.DateTime)

	archived = db.Column(db.Boolean)
	unread = db.Column(db.Boolean)
	starred = db.Column(db.Boolean)

	domain = db.Column(db.String)
	excerpt = db.Column(db.String)
	word_count = db.Column(db.Integer)
	image_url = db.Column(db.String)
	embed_url = db.Column(db.String)

	def __init__(self, url, date):
		self.url = url
		self.date = date
		self.archived = False
		self.unread = True
		self.starred = False

		parsed = readability.parse(url)
		if not (parsed is None):
			self.title = parsed.title
			self.domain = parsed.domain
			self.excerpt = parsed.excerpt
			self.word_count = parsed.word_count
			self.image_url = parsed.image_url

		self.embed_url = _find_embed_url(url)


def _find_embed_url(url):
	url = url.lower()

	if 'youtube.com/watch?v' in url:
		if '&' in url:
			param_pos = url.find('&')
			return url[:param_pos].replace('watch?v=', 'embed/')
		else:
			return url.replace('watch?v=', 'embed/')

	elif 'youtu.be' in url:
		return url.replace('.be', 'be.com/embed')

	elif 'yourepeat.com/watch?v' in url:
		return url.replace('repeat', tube).replace('watch?v=', '/embed')

	elif url.endswith('.jpg') or url.endswith('.jpeg') or url.endswith('.png') or url.endswith('.gif'):
		if not ('dropbox.com' in url):
			return url

	return ''
