import os
import cgi
import webapp2
import jinja2
import datetime 
import time
from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class BlogPost(db.Model):
  subject=db.StringProperty( required = True )
  content=db.TextProperty( required = True )
  postId=db.StringProperty( required = True)
  datestr = db.StringProperty( required = True )
  created=db.DateTimeProperty( auto_now_add = True )

class MainPage(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)
  
  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)
  
  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))
  
  def render_page(self):
    self.render("index.html")
  
  def get(self):
    self.render_page()

class BlogPage(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)
  
  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)
  
  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))
  
  def render_page(self):
    blogs = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC")
    self.render("front.html",blogs=blogs)
  
  def get(self):
    self.render_page()
      
class NewPost(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)
  
  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)
  
  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))
  
  def render_page(self,subject="",content="",error=""):
    self.render("newpost.html",subject=subject,content=content,error=error)
  
  def get(self):
    self.render_page()
  
  def post(self):
    sec_key = self.request.get("sec_key")
    subject = self.request.get("subject")
    content = self.request.get("content")
    d=str(datetime.datetime.now())
    d=d.replace("-","0")
    d=d.replace(" ","0")
    d=d.replace(":","0")
    d=d.replace(".","0")
    datestr = time.strftime("%A,%d %b %Y")
    if subject and content and sec_key == "thisisthepassword" :
      b=BlogPost(subject=subject,content=content,postId=d,datestr=datestr)
      b.put()
      d=str(b.key().id())
      time.sleep(2)
      self.redirect("/blog/"+d)
    else:
      self.render_page(subject,content,error="Enter both title and blog and correct security key")

class Acknowledge(webapp2.RequestHandler):
  def get(self,post_id):
    #b = db.GqlQuery("SELECT * FROM BlogPost")
    x=BlogPost.get_by_id(int(post_id))
    #for x in b:
      #if x.postId==post_id:
    html="""
          <html><body><h2>%s</h2><div><pre>%s</pre></div><br>
          <div><a href="http://abhishek-blog.appspot.com/blog">Go back to blog</a></div>
          </body></html>""" % ( cgi.escape(x.subject,quote=True), cgi.escape(x.content,quote=True))
        #break
    self.response.out.write(html)
    
app = webapp2.WSGIApplication([('/page',MainPage),('/blog', BlogPage),('/newpost',NewPost),('/blog/(\d+)',Acknowledge)],
                              debug=True)
