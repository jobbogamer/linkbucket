import linkbucket
import utils
from external_apis import readability

db = linkbucket.db

##### Model classes #####

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
	embed_type = db.Column(db.Integer)

	def __init__(self, url, date):
		self.url = url
		self.date = date
		self.archived = False
		self.unread = True
		self.starred = False

		parsed = readability.parse(url)
		if parsed is None:
			self.title = "(No title)"
			self.domain = utils.find_domain(url)
		else:
			self.title = parsed.title
			self.domain = parsed.domain
			self.excerpt = parsed.excerpt
			self.word_count = parsed.word_count
			self.image_url = parsed.image_url

		self.embed_url, self.embed_type = _find_embed(url)

##### Private API #####

def _find_embed(url):
	url_l = url.lower()

	if 'youtube.com/watch?v' in url_l:
		if '&' in url_l:
			param_pos = url_l.find('&')
			return (url[:param_pos].replace('watch?v=', 'embed/'), 1)
		else:
			return (url.replace('watch?v=', 'embed/'), 1)

	elif 'youtu.be' in url_l:
		return (url.replace('.be', 'be.com/embed'), 1)

	elif 'yourepeat.com/watch?v' in url_l:
		return (url.replace('repeat', tube).replace('watch?v=', '/embed'), 1)

	elif url_l.endswith('.jpg') or url_l.endswith('.jpeg') or url_l.endswith('.png') or url_l.endswith('.gif'):
		if not ('dropbox.com' in url_l):
			return (url, 2)

	return ('', 0)

##### Public API #####

def add_link(url, date):
	new_link = Link(url, date)
	db.session.add(new_link)
	db.session.commit()
	return new_link

def archive_link(id):
	link = get_link_by_id(id)
	link.archived = True
	db.session.commit()

def create_tables():
	db.create_all()

def delete_link(id):
	link = get_link_by_id(id)
	db.session.delete(link)
	db.session.commit()

def edit_title(id, new_title):
	link = get_link_by_id(id)
	link.title = new_title
	db.session.commit()

def get_archived_links():
	links = Link.query.filter_by(archived = True).all()
	links = sorted(links, key=lambda link: link.date, reverse=True)
	return links

def get_link_by_id(id):
	link = Link.query.filter_by(id = id).first()
	return link

def get_links():
	links = Link.query.filter_by(archived = False).all()
	links = sorted(links, key=lambda link: link.date, reverse=True)
	return links

def mark_link_as_read(id):
	link = get_link_by_id(id)
	link.unread = False
	db.session.commit()

def mark_link_as_starred(id):
	link = get_link_by_id(id)
	link.starred = True
	db.session.commit()

def mark_link_as_unread(id):
	link = get_link_by_id(id)
	link.unread = True
	db.session.commit()

def mark_link_as_unstarred(id):
	link = get_link_by_id(id)
	link.starred = False
	db.session.commit()

def unarchive_link(id):
	link = get_link_by_id(id)
	link.archived = False
	db.session.commit()
