#!/usr/bin/env python
# *_* coding: utf-8 *_*
from core.web.encrypt import md5

class Gravatar(object):
   """
   Simple object for create gravatar link

   gravatar = Gravatar(size=100, rating='g', default='retro', force_default=False, force_lower=False)
   """

   def __init__(self, size=100, rating='g', default='mm', force_default=False, force_lower=False):
       """
       
       Arguments:
       - `size`: default size for avatar
       - `rating`: default rating
       - `default`: default type for unregistred email
       - `force_default`:  build only default avatars
       - `force_lower`: make email.lower() before build link
       """
       self.size = size
       self.rating = rating
       self.default = default
       self.force_default = force_default
       self.force_lower = force_lower

   def __call__(self, email, size=None, rating=None, default=None, force_default=None, force_lower=True):
       if size is None:
           size = self.size

       if rating is None:
           rating = self.rating

       if default is None:
           default = self.default

       if force_default is None:
           force_default = self.force_default

       if force_lower:
           email = email.lower()

       hash = md5(email)

       link = 'http://www.gravatar.com/avatar/{hash}'\
              '?s={size}&d={default}&r={rating}'.format(**locals())

       if force_default:
           link = link + '&f=y'

       return link
       

