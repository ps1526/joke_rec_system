### Joke Recommender System
since I am pitifully unfunny

**Goal** is to create recommender system for jokes scraped through various APIs and build good node features to create a graph representation of jokes to stop cold-start problem.

Pipeline:
CSV -> Joke Sampling -> Graph Representation of Node Features(SentenceBert Embedding, Content, Category, etc.). Looking into better features to encapsulate humor -> PyG HeteroData Object -> 
HGT Implementation 

Next Steps: CLI + saveable user preferences, Deploy model and test on more data
