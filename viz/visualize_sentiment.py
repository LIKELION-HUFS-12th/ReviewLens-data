import json
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

results_path = 'data/results.json' # JSON 파일 경로.

# JSON 파일 가져옴
with open('data/results.json', 'r', encoding='utf-8') as f:
  results = json.load(f)

# 감정별로 리뷰 분류
positive_reviews = []
neutral_reviews = []
negative_reviews = []

for review_id, data in results.items():
    sentiment = data['감정분석결과']['document']['sentiment']
    review_text = data['리뷰']
    
    if sentiment == 'positive':
        positive_reviews.append(review_text)
    elif sentiment == 'neutral':
        neutral_reviews.append(review_text)
    elif sentiment == 'negative':
        negative_reviews.append(review_text)

# 감정별 리뷰 수 계산
sentiment_counts = {
    'Positive': len(positive_reviews),
    'Neutral': len(neutral_reviews),
    'Negative': len(negative_reviews)
}



### Bar Chart
def plot_bar_chart(sentiment_counts):
    plt.figure(figsize=(8, 6))
    sns.barplot(x=list(sentiment_counts.keys()), y=list(sentiment_counts.values()), palette='Set2')
    plt.title("Sentiment Counts")
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.show()

# 바 차트 그리기 함수 호출
plot_bar_chart(sentiment_counts)