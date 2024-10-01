### 워드클라우드 생성
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# JSON 파일 가져옴
with open('data/results.json', 'r', encoding='utf-8') as f:
  results = json.load(f)

# 각 감정에 대한 리뷰를 저장할 리스트
positive_reviews = []
neutral_reviews = []
negative_reviews = []

# 리뷰와 감정 분석 결과를 분류
for review_id, data in results.items():
    sentiment = data['감정분석결과']['document']['sentiment']
    review_text = data['리뷰']
    
    if sentiment == 'positive':  # 긍정적인 리뷰
        positive_reviews.append(review_text)
    elif sentiment == 'neutral':  # 중립적인 리뷰
        neutral_reviews.append(review_text)
    elif sentiment == 'negative':  # 부정적인 리뷰
        negative_reviews.append(review_text)
        
# 모든 리뷰에서 긍정적인 리뷰만을 모아서 텍스트 추출
positive_reviews = []
for review_id, data in results.items():
    sentiment = data['감정분석결과']['document']['sentiment']
    if sentiment == 'positive':  # 긍정적인 리뷰만
        positive_reviews.append(data['리뷰'])

# 워드클라우드를 위한 텍스트 결합
text = ' '.join(positive_reviews)

# 워드클라우드 생성 
font_path = 'viz/NanumGothic.TTF'  # 한글 폰트 경로 설정 - C:/Windows/Fonts 안에 있는 거 폴더에 복붙해줌.
wordcloud = WordCloud(font_path=font_path, background_color='white', width=800, height=600).generate(text)

# 워드클라우드 시각화
plt.figure(figsize=(10, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()