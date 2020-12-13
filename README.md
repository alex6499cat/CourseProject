# Sentiment Analysis of Customer Service Tweets

Presentation: [https://youtu.be/wcCyMLzrOu8](https://youtu.be/wcCyMLzrOu8)

### Our goals

**Note**: it was not our intention to create any library or software, but instead to do a deep dive into a data set and present our findings. Because of this, our presentation is more about our findings instead of usage, and our "testable" code is more of a playground with limited functionality, running all code that we used to generate our findings could take days.

As discussed in our proposal, we set out to analyze 1 million customer service tweets. This analysis includes:
- Analysis of the overall sentiment change of a thread. That is, the difference in sentiment between the first and last tweet of one customer in a thread. This data was stratified by time and company to further compare and analyze how well the top companies stack up against each other.
- Analysis of common topics by company. With tweets being short and complaints not being too broad within the scope of one company, we found that a smaller amount of topics (_k_) tends to find more distinct topics. While these topics aren't given any human readable title, you can infer what a topic might be about based on its unigram language model.
- Analysis of successive sentiment. That is, the difference in sentiment of customer tweets that "sandwich" a customer service tweet. As opposed to the earlier mentioned sentiment analysis, this had the intention of finding successful language, instead of comparing companies against each other or themselves over time. But again with tweets being short and customer service responses tending to be formulaic, there wasn't much difference in language between successful and unsuccessful customer service responses.

### Testing/"Playground"

Along with python notebooks, we also have a well put together excel spreadsheet that includes data from our first goal and that also has several sheets you can interact with. That spreadsheet is found at `output/Sentiment summary by company and month.xlsx`

We have provided several playground files, or files meant for our tester to "test" our code with since they are more lightweight.
- Overall sentiment change 
  - tester files:
  - dependencies:
- Topic analysis:
  - tester files:
  - dependencies:
- Consecutive sentiment change (developed on python 3.7.3)
  - tester files: `Jupyter Notebooks/con_sent_tester.ipynb`
  - dependencies: pandas, gensim
