import nltk 
nltk.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer

def getSentiment(feedbackString):
    sid = SentimentIntensityAnalyzer()
    score = sid.polarity_scores(feedbackString)
    score = score['compound']
    #returns a score of -100 to 100 based on string 
    normalized_value = int(score  * 100)
    normalized_value = normalized_value/100
    return normalized_value

#feedback list and message 
def getRating(feedbackLst, msg):
    for i in range(len(feedbackLst)):
        feedbackLst[i] = int(feedbackLst[i])
    ratingScore= 0 
    for i in range(len(feedbackLst)): 
        ratingScore += feedbackLst[i]*.03
    print("RATING SCORE WITHOUT SENTIMENT" , ratingScore)
    ratingScore += getSentiment(msg)*.25
    #in range of 0 to 1
    print("RATING SCORE WITH SENTIMENT" , ratingScore)
    normalize_rating = ratingScore*5
    return normalize_rating