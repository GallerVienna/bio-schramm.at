import os
import jinja2
import webapp2
from google.appengine.ext import ndb
from google.appengine.api import mail


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}

        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))



# Article
class Article(ndb.Model):
    sent = ndb.StringProperty()
    title = ndb.StringProperty()
    title2 = ndb.StringProperty()
    pic = ndb.StringProperty()
    pic2 = ndb.StringProperty()
    pic3 = ndb.StringProperty()
    message = ndb.StringProperty()
    description1 = ndb.StringProperty()
    description2 = ndb.StringProperty()
    description3 = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)

class Admin(BaseHandler):
    def get(self):
        articles = Article.query(Article.deleted == False).fetch()
        params = {"articles": articles}
        return self.render_template("admin.html", params=params)

    def post(self):
        password = self.request.get("sent")
        title = self.request.get("title")
        title2 = self.request.get("title2")
        pic = self.request.get("pic")
        pic2 = self.request.get("pic2")
        pic3 = self.request.get("pic3")
        description1 = self.request.get("description1")
        description2 = self.request.get("description2")
        description3 = self.request.get("description3")
        message = self.request.get("message")

        if password != "PASSWORD": #That not anyone can post articles
            return self.write("Your are not authorised to post!")
        if "<script>" in message: #A little hacker protection
            return self.write("Can't hack me!")

        atc_object = Article(sent=passwort, title=title, title2=title2,
                             pic=pic, pic2=pic2, pic3=pic3, description1=description1, description2=description2,
                             description3=description3, message=message.replace("<script>", ""))
        atc_object.put()
        return self.redirect_to("admin-site")

class MainHandler(BaseHandler):
    def get(self):
        articles = Article.query(Article.deleted == False).order(-Article.created).fetch() # articles ordered by actual
        params = {"articles": articles}
        return self.render_template("main.html", params=params)

class Products(BaseHandler):
    def get(self):
            self.render_template("products.html")

class Contact(BaseHandler):
    def get(self):
            self.render_template("contact.html")

    def post(self):
        ### Send Request as Email###
        email = self.request.get("email")
        name = self.request.get("name")
        email_recipient = "example@gmail.com" # add here YOUR email address (the owner of the Site)
        tel = self.request.get("tel")
        street = self.request.get("street")
        city = self.request.get("city")
        email_body = self.request.get("message")
        # mail get sent
        mail.send_mail(sender=email_recipient,
                       to=email_recipient,
                       subject="Anfrage von " + name + "| www.bio-schramm.at",
                       body="Name: " + name + " Anschrift: " + street + city +
                            " Tel.: " + tel +
                            " Email: "+ email +
                            " Anfrage:" + email_body)

        return self.redirect_to("main-page")

class About(BaseHandler):
    def get(self):
            self.render_template("about.html")

class Feed(BaseHandler):
    def get(self):
        articles = Article.query(Article.deleted == False).order(-Article.created).fetch() # articles ordered by actual
        params = {"articles": articles}
        return self.render_template("feed.html", params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/admin', Admin, name="admin-site"),
    webapp2.Route('/products', Products, name="products"),
    webapp2.Route('/contact', Contact, name="contact-site"),
    webapp2.Route('/about', About, name="about-site"),
    webapp2.Route('/feed', Feed, name="feed-site"),
], debug=True)
