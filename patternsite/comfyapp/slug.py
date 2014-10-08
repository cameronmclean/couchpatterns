import re

def slug(string_to_slug):
	words = str(string_to_slug)
	lower = words.lower().replace(' ', '-')
	slugged = re.sub(r'[^a-z0-9-]+', '', lower)
	return slugged
