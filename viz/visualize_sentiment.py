import json
import matplotlib.pyplot as plt
import seaborn as sns

results_path = 'data/results.json'  # JSON 파일 경로.

# JSON 파일 가져오기
with open(results_path, 'r', encoding='utf-8') as f:
    results = json.load(f)


### 감정별로 리뷰 수 카운트
sentiment_counts = {
    'Positive': 0,
    'Neutral': 0,
    'Negative': 0
}

for review_id, data in results.items():
    sentiment = data['감정분석결과']['document']['sentiment']
    
    if sentiment == 'positive':
        sentiment_counts['Positive'] += 1
    elif sentiment == 'neutral':
        sentiment_counts['Neutral'] += 1
    elif sentiment == 'negative':
        sentiment_counts['Negative'] += 1

# 감정별 리뷰 수 출력
print("Sentiment Counts:")
for sentiment, count in sentiment_counts.items():
    print(f"{sentiment}: {count}")



x_labels = ['Positive', 'Neutral', 'Negative']

### Bar Chart 그리기
def plot_bar_chart(sentiment_counts):
    plt.figure(figsize=(8, 6))
    sns.barplot(x=x_labels, y=list(sentiment_counts.values()), palette='Set2')
    plt.title("Review Lens")
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.show()


### Pie Chart 그리기
def plot_pie_chart(sentiment_counts):
    sizes = list(sentiment_counts.values())
    colors = ['#ff9999','#66b3ff','#99ff99']  # 색상 
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=x_labels, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.axis('equal')  
    plt.title("Review Lens")
    plt.show()


# 함수 호출
plot_bar_chart(sentiment_counts)
plot_pie_chart(sentiment_counts)