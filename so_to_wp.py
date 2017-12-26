from stackapi import StackAPI
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from datetime import datetime,timedelta
import getpass

##Enter the wordpress blog details. The wp_blogname will be just the name of the blog without wordpress.com.
## Ex: If blogname is https://linuxknows.wordpress.com the user will have to enter: linuxknows
##The password input will not be visible to the user
wp_blogname=input("Enter the wordpress blogname: ")
wp_username=input("Enter the wordpress username: ")
wp_password=getpass.getpass("Enter the wordpress password: ")

##Set the WP credentials to the WP client
wp = Client('https://'+wp_blogname+'.wordpress.com/xmlrpc.php', str(wp_username), str(wp_password))
post = WordPressPost()

SITE = StackAPI('stackoverflow')

##The topics for which questions will be searched on stackoverflow
topics=["java","python","linux","cloud","aws","jenkins"]

for topic in topics:
  SITE.max_pages=1
  ##Fetch the questions tagged with topic.
  questions = SITE.fetch('questions',filter='withbody' ,fromdate=(datetime.now()-timedelta(hours = 24)), todate=datetime.now(), sort='votes', tagged=topic)
  i = 0
  for item in questions['items']:
      ##Only select the top 5 voted and answered questions.
      if item['is_answered'] == True and 'accepted_answer_id' in item and i < 5:
        try:
          post.title = item['title']
          print("Posting: "+item['title'])
          answer=SITE.fetch('answers', filter='withbody', ids=[item['accepted_answer_id']])
          post.content=item['body']+"\n\n\n <b>Solution:</b>\n"+answer['items'][0]['body']
          post.terms_names = {
           'post_tag': item['tags'],
           'category': [topic]
          }
          post.post_status='publish'
          wp.call(NewPost(post))
          i=i+1
        except Exception as e:
            print("Exception occured"+str(e))
            pass
