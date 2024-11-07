import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 예시 데이터 500개
"""
summary = [
    {
        "product_name": "OO초**비비크림SPF30PA++4종",
        "original_content": "OO 이 비비가 좋다길래 사봤어요...원래 피부가 어두워 22호 선택했는데...적당한것 같구요.. 화장을 잘 안하는 편이라..이거라도 발라볼까 하고 샀는데 ;; 아직 한번밖에 안써봤네요 ㅋ 공기가 많이 들어있는지... 첨에 펌프 엄청 많이 눌러야 나와요...그래서 용기가 저만큼이나 쪼그라듬...한번밖에 안썼는데 말이죠...",
        "combined_content": "OO 비비가 좋다길래 사봤어요 원래 피부가 어두워 22호 선택했는데적당한것 같구요  화장을 잘 안하는 편이라이거라도 발라볼까 하고 샀는데 아직 한번밖에 안써봤네요  공기가 많이 들어있는지 첨에 펌프 엄청 많이 눌러야 나와요 그래서 용기가 저만큼이나 쪼그라듬한번밖에 안썼는데 말이죠",
        "document_sentiment": "negative"
    },
    {
        "product_name": "OO그**썬스틱6개+달팽이마스크팩2박스(총10매)",
        "original_content": "광고 보다 별로 입니다 유분도 여름에 사용하기에 너무많아서 끈적여요 잘못구매 하것ㅈ같아요",
        "combined_content": "광고 보다 별로 입니다  유분도 여름에 사용하기에 너무많아서 끈적여요  잘못구매 하것같아요",
        "document_sentiment": "negative"
    },
"""

import sys
import io
import pandas as pd
import re
import json
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 파이썬 stdout 인코딩 설정 (출력 한글 깨짐 방지)
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
results_path = 'ReviewLens-data/data/results_3.json'  # JSON 파일 경로
# JSON 파일 가져오기
with open(results_path, 'r', encoding='utf-8') as f:
    results = json.load(f)

summary = []

for key, value in results.items():
    summary_b = {
        "product_name": value["상품명"].replace(" ", ""),  # 공백 제거
        "original_content": "", #무시
        "combined_content": value["리뷰"].replace(" ", ""),  # 공백 제거
        "document_sentiment": value["감정분석결과"]["document"]["sentiment"]
    }
    summary.append(summary_b)

# 결과 출력
print(json.dumps(summary, ensure_ascii=False, indent=4))

# 긍정적인 리뷰만 필터링 (상품명을 포함)
def filter_positive_reviews(summary):
    positive_reviews = [f"{review['product_name']} {review['original_content']}" for review in summary if review["document_sentiment"] == "positive"]
    return positive_reviews

# 부정적인 리뷰만 필터링 (상품명을 포함)
def filter_negative_reviews(summary):
    negative_reviews = [f"{review['product_name']} {review['original_content']}" for review in summary if review["document_sentiment"] == "negative"]
    return negative_reviews

# 중립적인 리뷰만 필터링 (상품명을 포함)
def filter_neutral_reviews(summary):
    negative_reviews = [f"{review['product_name']} {review['original_content']}" for review in summary if review["document_sentiment"] == "neutral"]
    return negative_reviews

# 워드 클라우드 생성 함수
def generate_wordcloud(text, title=''):
    wordcloud = WordCloud(font_path='ReviewLens-data/viz/NanumGothic.TTF', 
                          width=800, height=400, background_color='white').generate(text)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(title, fontsize=16)
    plt.axis('off')
    plt.show()

# 긍정적/부정적 워드클라우드 생성 함수
def generate_sentiment_wordclouds(summary):
    # 긍정적인 리뷰 필터링
    positive_reviews = filter_positive_reviews(summary)
    positive_text = " ".join(positive_reviews)
    
    # 부정적인 리뷰 필터링
    negative_reviews = filter_negative_reviews(summary)
    negative_text = " ".join(negative_reviews)
    
    # 중립적인 리뷰 필터링
    neutral_reviews = filter_neutral_reviews(summary)
    neutral_text = " ".join(neutral_reviews)
    
    # 불용어 제거
    wordcloud_stopword = ['아', '구매했네요', '제가', '좋구', '써보니', '쓰던', '없어서', '없네요', '넘', '앞으로', '다른', 'OOO', '많이', '않아', '같이', '같아요', '전', '것', '않고', '진짜', '좀', '정말', '더', '않아요', '있어', '있습니다', '좋아요', '좋고', '잘', '많이', '너무너무', '원래', '샀는데', '같습니다', '좋다길래', '괜찮아요', '있어요', '사봤어요', '보다', '요건', '그래서', '별로', '따지면', '같구요', '선택했는데적당한것', '하고', '말이죠', '구매', '너무많아서', '바르면', '입니다', '바르고', '광고', '첨에', '엄청', '열심히', '바르다', '생각보단', '요거', '제형' '00', '얼굴에', '너무', '같아요', '없고', '없어요', '좋은거', '해서', '안', '아주', '그냥', '많아', '처음', '들어있는지', '쓰고', '않을거라고', '있음', '들어요', '있고', '수', '제형의', '좋은', '근데', '않을거라고']

    # 긍정적인 리뷰에서 불용어 제거 
    positive_filtered_words = [word for word in positive_text.split() if word not in wordcloud_stopword]
    positive_filtered_text = " ".join(positive_filtered_words)

    # 부정적인 리뷰에서 불용어 제거 
    negative_filtered_words = [word for word in negative_text.split() if word not in wordcloud_stopword]
    negative_filtered_text = " ".join(negative_filtered_words)
    
    # 중립적인 리뷰에서 불용어 제거
    neutral_filtered_words = [word for word in neutral_text.split() if word not in wordcloud_stopword]
    neutral_filtered_text = " ".join(neutral_filtered_words)
    
    # 긍정적인 리뷰 워드클라우드 생성
    print("긍정적인 리뷰 워드클라우드:")
    generate_wordcloud(positive_filtered_text, title='Positive Reviews Word Cloud')
    
    # 부정적인 리뷰 워드클라우드 생성
    print("부정적인 리뷰 워드클라우드:")
    generate_wordcloud(negative_filtered_text, title='Negative Reviews Word Cloud')

    # 중립적인 리뷰 워드클라우드 생성
    print("중립적인 리뷰 워드클라우드:")
    generate_wordcloud(neutral_filtered_text, title='Neutral Review Word Cloud')

# 워드 클라우드 생성 예시
generate_sentiment_wordclouds(summary)

#근데 상품명만 따서 워클하는거랑 상품 정보만 따서 워클하는거 필요할듯