import json
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import io
from matplotlib import font_manager, rc
import math

# 파이썬 stdout 인코딩 설정 (출력 한글 깨짐 방지)
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

# 한글 폰트 설정
font_path = 'ReviewLens-data/viz/NanumGothic.TTF'
#font = font_manager.FontProperties(fname=font_path).get_name()
#rc('font', family=font)
font_manager.fontManager.addfont(font_path)
rc('font', family='NanumGothic')

results_path = 'ReviewLens-data/data/results_3.json'  # JSON 파일 경로

# JSON 파일 가져오기
with open(results_path, 'r', encoding='utf-8') as f:
    results = json.load(f)




### 상품별로 리뷰 나누기
ps_counts = {}

for review_id, data in results.items():
    product = data['상품명']  # 상품명
    sentiment = data['감정분석결과']['document']['sentiment']

    # 상품별로 감정 카운트가 없으면 초기화
    if product not in ps_counts:
        ps_counts[product] = {'Positive': 0, 'Neutral': 0, 'Negative': 0}

    # 감정별 카운트 증가
    if sentiment == 'positive':
        ps_counts[product]['Positive'] += 1
    elif sentiment == 'neutral':
        ps_counts[product]['Neutral'] += 1
    elif sentiment == 'negative':
        ps_counts[product]['Negative'] += 1

output_dir = 'ReviewLens-data/viz/'  # 저장할 디렉토리 경로
max_products_per_page = 20  # 한 페이지(이미지)에 포함할 최대 상품 수

### 시각화 및 저장 (여러 페이지로 분할 10000개 리뷰 이미지 9장으로 출력)
def charts(ps_counts, output_dir, max_products_per_page):
    products = list(ps_counts.items())
    num_pages = math.ceil(len(products) / max_products_per_page)

    for page in range(num_pages):
        start = page * max_products_per_page
        end = start + max_products_per_page
        subset = products[start:end]
        
        num_products = len(subset)
        fig, axes = plt.subplots(num_products, 2, figsize=(10, 5 * num_products))  # 상품별로 2개 차트
        fig.tight_layout(pad=5.0)  # 차트 사이의 간격

        for i, (product, counts) in enumerate(subset):
            sentiments = list(counts.keys())  # 감정 (Positive, Neutral, Negative)
            values = list(counts.values())  # 각 감정에 대한 카운트
            colors = ['#ff9999', '#66b3ff', '#99ff99']  # 파이 차트 색상

            # Bar chart (왼쪽)
            sns.barplot(x=sentiments, y=values, palette='Set2', ax=axes[i, 0])
            axes[i, 0].set_title(f"ReviewLens for {product}", loc='left')
            axes[i, 0].set_xlabel("Sentiment")
            axes[i, 0].set_ylabel("Count")

            # Pie chart (오른쪽)
            if sum(values) > 0 and values.count(0) == len(values) - 1:  # 100%와 0%만 있는 경우
                non_zero_index = values.index(max(values))  # 100%에 해당하는 인덱스 찾기
                filtered_labels = [sentiments[non_zero_index]]  # 100% 레이블만 사용
                filtered_values = [values[non_zero_index]]  # 100% 값만 사용
                axes[i, 1].pie(
                    filtered_values,
                    labels=filtered_labels,
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=[colors[non_zero_index]]
                )
            else:
                axes[i, 1].pie(values, labels=sentiments, autopct='%1.1f%%', startangle=90, colors=colors)
            axes[i, 1].axis('equal') 

        # 페이지별로 차트를 저장
        output_file = f"{output_dir}individual_viz_charts_3_page_{page + 1}.png"
        plt.savefig(output_file, bbox_inches='tight')
        #plt.show()
        plt.close()


# 차트 생성 및 저장
charts(ps_counts, output_dir, max_products_per_page)

"""
# 기존
### 시각화 및 저장
def charts(ps_counts, output_file):
    num_products = len(ps_counts)
    fig, axes = plt.subplots(num_products, 2, figsize=(8, 5 * num_products))  # 상품별로 2개 차트
    fig.tight_layout(pad=5.0)  # 차트 사이의 간격

    for i, (product, counts) in enumerate(ps_counts.items()):
        sentiments = list(counts.keys())  # 감정 (Positive, Neutral, Negative)
        values = list(counts.values())  # 각 감정에 대한 카운트
        colors = ['#ff9999', '#66b3ff', '#99ff99']  # 파이 차트 색상

        # Bar chart (왼쪽)
        sns.barplot(x=sentiments, y=values, palette='Set2', ax=axes[i, 0])
        axes[i, 0].set_title(f"Sentiment Analysis (Bar Chart) for {product}", loc='left')
        axes[i, 0].set_xlabel("Sentiment")
        axes[i, 0].set_ylabel("Count")

        # Pie chart (오른쪽)
        if values[0] == 100:  # Positive가 100%인 경우
            # 레이블을 표시하지 않거나 다른 방식으로 처리
            axes[1].pie(values, labels=[sentiments[0], ''], autopct='%1.1f%%', startangle=90, colors=colors)
        else:
            axes[1].pie(values, labels=sentiments, autopct='%1.1f%%', startangle=90, colors=colors)

        axes[1].axis('equal') 


    # 전체 차트를 하나의 이미지로 저장
    plt.savefig(output_file, bbox_inches='tight')
    plt.show()


# 차트를 저장할 파일 경로
output_file = 'ReviewLens-data/viz/individual_viz_charts.png'

# 차트 생성 및 저장
charts(ps_counts, output_file)
"""




