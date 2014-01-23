wordpress_fetch_images_to_local
===============================

This python script will scan all your wordpress post, download all 
linked images in your posts which are not stored on your blog host
to your blog media libarary and update the link to point to them. 
You need to install python-wordpress-xmlrpc 
(http://python-wordpress-xmlrpc.readthedocs.org )
to run this script.

You need to edit the following fields in the script before run it.

blog_url = "www.my_blog_address.com"

username = "username"

password = "xxxxxxxx"

number_of_post = 500


In case you have no idea how to run a python script you can follow these guides:

For Windows users:

http://docs.python.org/2/faq/windows

For Mac users:

http://docs.python.org/2/using/mac.html

For Linux users:

I bet you can figure it out by yourself eaily:)


