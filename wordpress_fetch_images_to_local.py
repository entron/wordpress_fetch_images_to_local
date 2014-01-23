#! /usr/bin/env python
# -*- coding: utf-8 -*- 
"""
        wordpress_fetch_images_to_local.py
	
	entron@github 2014
        
        This script will scan all your wordpress post, download all 
        linked images in your post to local media libarary and update the 
	link to point to the local images. You need to install 
	python-wordpress-xmlrpc (http://python-wordpress-xmlrpc.readthedocs.org )
	to run this script.  
"""
#Replace the following parameters accroding to your blog
blog_url = "www.my_blog_address.com"  #No need to use the http:// prefiex
username = "username"
password = "xxxxxxxx"
number_of_post = 500

import random
import string
import urlparse
import urllib
from urllib2 import urlopen
from HTMLParser import HTMLParser
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import media
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost, EditPost
from wordpress_xmlrpc.compat import xmlrpc_client

url = "http://" + blog_url + "/xmlrpc.php"

class MyHTMLParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.images = []	
    
  def handle_starttag(self, tag, attrs):
    if tag == 'img':
      for attr in attrs:
        if attr[0] == 'src':
          self.images.append(attr[1])

def external_images(images):
  ex_images = []
  for image_url in images:
    o = urlparse.urlparse(image_url)
    if o.netloc != blog_url:
      ex_images.append(image_url)
  return ex_images
  
def url_fix(s, charset='utf-8'):
	"""Sometimes you get an URL by a user that just isn't a real
	URL because it contains unsafe characters like ' ' and so on.  This
	function can fix some of the problems in a similar way browsers
	handle data entered by the user:

	>>> url_fix(u'http://de.wikipedia.org/wiki/Elf (Begriffsklärung)')
	'http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29'

	:param charset: The target charset for the URL if the url was
					given as unicode string.
	"""
	if isinstance(s, unicode):
		s = s.encode(charset, 'ignore')
	scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
	path = urllib.quote(path, '/%')
	qs = urllib.quote_plus(qs, ':&=')
	return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))

def fetch_image(wp, image_url):
    image_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10)) #random image number of length 10
    image_name = image_name + '.jpg'
	# prepare metadata
    data = {'name': image_name, 'type': 'image/jpg'}
    # read the binary file and let the XMLRPC library encode it into base64
    input_url = url_fix(image_url) 
    img = urlopen(input_url)
    data['bits'] = xmlrpc_client.Binary(img.read())
    response = wp.call(media.UploadFile(data))
    #print response
    return response['url']


parser = MyHTMLParser()

wp = Client(url, username, password)
posts = wp.call(GetPosts({'number': number_of_post}))
print "Number of posts fetched: ", len(posts)

for post in posts:
  replaced = 0
  print(post.title)
  updated_post = post
  parser.images = []
  parser.feed(post.content)
  if parser.images:
    print parser.images
    to_be_fetched_images = external_images(parser.images)
    for image in to_be_fetched_images:
		if image:
		  print "Fetching image: ", image
		  local_url = fetch_image(wp, image)
		  print "Image saved to: ", local_url
		  updated_post.content = updated_post.content.replace(image, local_url)
		  replaced = 1
  if replaced:	  
    wp.call(EditPost(post.id, updated_post))

    
    



