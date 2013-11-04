bearRec - Berkeley Course Recommender
=====================================

### Introduction
Have you ever had difficulty searching for a class related to a topic 
that you're interested in? Or spending hours searching on schedule.berkeley.edu? 
No more of that pain with [bearRec](https://bearrec.herokuapp.com/)!

### Versions
* 0.1.1 (09/29/2013) - Users can now select the number or results they want to show. Add detailed README instuctions and toggle highlight        
* 0.1.0 (09/28/2013) - First version! Demonstrated this hack at HackJam

### Installation
```bash
git clone https://github.com/kqdtran/bearRec.git      
pip install -r requirements.txt
```    

Run locally in port 5000 by:    

```python
python run.py
```

### Implementation
We first scrape the courses from the Berkeley catalog. Then, we construct a document-term 
matrix, where each course is a document, and apply the [TF-IDF algorithm](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) 
on the matrix to weight the important features for calculating similarity.     

Finally, we apply the [cosine distance similarity algorithm](https://en.wikipedia.org/wiki/Cosine_similarity) 
between the queries and every row of the matrix to retrieve similarity scores. 
We then rank them from top to bottom, and output the top results as the 
courses that are related to the search term(s).    

### Wish List
Please send us a pull request if you would like to contribute! There are many awesome features 
that we could certainly extend to this project. Some of them are:    

* [DeCal](http://www.decal.org/) - Student-taught classes support
* Link to the current schedule/catalog so people can find course description
* Make the output a bit more user-friendly
* Clustering related courses
* Visualization, as a graph perhaps, where each vertex is a course, and the edge 
weight between every two vertices is their similarity score

### Related Resources
* [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/)   
* [Flask](http://flask.pocoo.org/)
* [Requests](http://docs.python-requests.org/en/latest/)
* [Pattern](http://www.clips.ua.ac.be/pattern)   
* [NetworkX](http://networkx.github.io/)   
