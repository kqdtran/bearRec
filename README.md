bearRec - Berkeley Course Recommender
=====================================

### Introduction
Have you ever had lots of difficulty searching for a class on a topic 
you're interested in? Or spent hours hopping between pages on schedule.berkeley.edu? 
With [bearRec](https://bearrec.herokuapp.com/), we hope you would never have to do 
that again!

### Versions
* 0.2.0 (11/08/2013) - Rewrote the app using the Berkeley API from [Berkeley Developers](https://developer.berkeley.edu)! 
Added more information on class location, instructors, etc. and improve search UI 
* 0.1.1 (09/29/2013) - Users can now select the number or results they want to show. 
Added detailed README instuctions and toggle highlight        
* 0.1.0 (09/28/2013) - First version! Demonstrated this hack at HackJam

### If you plan to break it...
```bash
git clone https://github.com/kqdtran/bearRec.git      
pip install -r requirements.txt
```    

Next, go to the [Berkeley Developers](https://developer.berkeley.edu) website and acquire an app key. 
Berkeley hackers can get one by simply logging in with their CalNet ID and generate a key 
for this app. If you are not affiliated with Berkeley, please contact them for more information.   

Then, inside bearRec, create a file called `auth.py`. The structure should look something like this:   

```python
def authenticate():
  appID = 'XXXXXXX' # your App ID
  appKey = 'YYYYYYYYYYYYYYY' # your App Key
  return appID, appKey
```

You should then be able to log in and make requests! 

Run locally in port 5000 by:    

```python
python run.py
```

### Implementation
~~We first scrape the courses from the Berkeley catalog~~. No more scraping, we now use the Berkeley API to GET 
the request from the school's catalog/schedule of classes. Then, we construct a document-term 
matrix, where each course is a document, and apply the [TF-IDF algorithm](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) 
on the matrix to weight important features for calculating similarity.     

Finally, we apply the [cosine distance similarity algorithm](https://en.wikipedia.org/wiki/Cosine_similarity) 
between the queries and every row of the matrix to retrieve similarity scores. 
We then rank them from top to bottom, and output the top results as the 
courses that are related to the search term(s).    

### Wish List
Please send us a pull request if you would like to contribute! There are many awesome features 
that we could certainly extend to this project. Some of them are:    

* It currently doesn't support any of the 19x classes, since they are Special Topic classes. 
We might have to scrape schedule.berkeley.edu for those.
* Add support for [DeCal](http://www.decal.org/) - student-taught classes
* Cluster related courses
* Visualization (D3, NetworkX, etc.)
* If we could get our hands on student's registration data from the Registrar, 
wouldn't it be so cool to build a recommender system like Amazon? xD 
Imagine something like "457 other CS majors recently took this class"

### Related Resources
* [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/)   
* [Flask](http://flask.pocoo.org/)
* [Requests](http://docs.python-requests.org/en/latest/)
* [Pattern](http://www.clips.ua.ac.be/pattern)     
