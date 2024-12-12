from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
import pandas as pd
import re
import json
import time

# Hugging Face 모델 로드
model_name = "rlawltjd/kobert-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
label_map = {0: "negative", 1: "neutral", 2: "positive"}

def load_file(file_path):
    print("파일 로딩 중...")
    text_data = pd.read_excel(file_path)
    product_names = text_data['상품명'].astype(str).tolist() 
    reviews = text_data['상품평']
    review_list = reviews.astype(str).tolist()
    return review_list, product_names

def preprocess(review_list):
    print("파일 로딩 완료. 데이터 전처리 중...")
    processed_reviews = []
    original_reviews = []
    
    for review in review_list:
        cleaned_original_review = re.sub(r'\s+', ' ', review).strip() 
        original_reviews.append(cleaned_original_review)
        
        review_cleaned = re.sub(r'[^가-힣a-zA-Z0-9\s]', '', cleaned_original_review)
        processed_reviews.append(review_cleaned)

    return original_reviews, processed_reviews


def create_test_data(preprocessed_reviews, original_reviews, product_names, sample_size):
    if sample_size == 'max':
        max_size = len(preprocessed_reviews)
    else:
        max_size = min(sample_size, len(preprocessed_reviews), len(original_reviews), len(product_names))
    
    preprocessed_reviews_sliced = preprocessed_reviews[:max_size]
    original_review_list_sliced = original_reviews[:max_size]
    product_list_sliced = product_names[:max_size]
    
    return preprocessed_reviews_sliced, original_review_list_sliced, product_list_sliced

def analyze_reviews_with_model(preprocessed_reviews_sliced):
    print("데이터 전처리 완료. 감정 분석 시작...")
    start_time = time.time()

    result_list = []
    for i, review in enumerate(preprocessed_reviews_sliced):
        progress = (i + 1) / len(preprocessed_reviews_sliced) * 100
        print(f'전체 {len(preprocessed_reviews_sliced)}개 데이터 중 {i+1}번 째 데이터 {progress:.2f}% 완료')

        inputs = tokenizer(review, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            probs = F.softmax(logits, dim=-1).squeeze()
            predicted_class = logits.argmax(dim=-1).item()

        sentiment = label_map[predicted_class]
        result_list.append({"review": review, "sentiment": sentiment})

    end_time = time.time()
    total_time = end_time - start_time
    print(f"감정 분석 완료. 총 소요 시간: {total_time:.2f}초")
    return result_list

def process_sentiment_analysis(sentiment_data_list, original_reviews, product_list_test):
    summary = []
    
    for i, sentiment_data in enumerate(sentiment_data_list):
        document_sentiment = sentiment_data.get('sentiment', 'neutral')
        product_name_cleaned = product_list_test[i].replace(" ", "")

        document_summary = {
            "product_name": product_name_cleaned,
            "original_content": original_reviews[i],
            "document_sentiment": document_sentiment
        }
        summary.append(document_summary)
        
    result = json.dumps(summary, ensure_ascii=False, indent=4)

    output_file_path = 'result/sentiment_analysis_result_kobert.json'
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(result)

    print(f"결과가 {output_file_path}에 저장되었습니다.")

def main_process(file_path):
    review_list, product_names = load_file(file_path)  
    original_reviews, preprocessed_reviews = preprocess(review_list)  
    review_list_test, original_review_list_test, product_list_test = create_test_data(
        preprocessed_reviews, original_reviews, product_names, sample_size='max'
    )
    result_list = analyze_reviews_with_model(review_list_test)  
    process_sentiment_analysis(result_list, original_review_list_test, product_list_test)

file_path = 'reviews/메이크업뷰티케어_reviews.xlsx'
main_process(file_path)
