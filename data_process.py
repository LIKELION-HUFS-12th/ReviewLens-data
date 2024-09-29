### 전처리 전, 엑셀 파일의 리뷰 데이터들을 불러와서 리스트 속 문자열로 각각 저장 - json 파일로 변환 위해서 (클로바 api 사용 위함).

#출력 한글 인코딩 문제 발생 방지 - 기본적으로 파이썬이 출력할 때 사용하는 인코딩을 'utf-8'로 강제 지정하여 한글이 깨지는 문제를 해결.
import sys  #시스템 관련 모듈 불러옴.
import io   #입출력 관련 모듈 불러옴.
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')  #파이썬의 기본 출력 스트림(sys.stdout)을 새롭게 설정하여 인코딩을 UTF-8로 변경.

import pandas as pd

file_path = 'makeup_review.xlsx'  #엑셀 파일 경로를 변수에 저장.

text_data = pd.read_excel(file_path)  #변수에 pd.read_excel("엑셀 경로") 으로 엑셀 파일을 데이터프레임(DataFrame) 타입으로 할당.

review = text_data['상품평']  #'상품평'이라는 열(Column)을 선택하여 해당 데이터를 'review' 변수에 할당.

review_list = review.astype(str).tolist() # '상품평' 데이터를 문자열로 변환한 뒤 리스트로 변환하여 'review_list'에 저장.


### 결과 테스트 
# 리스트의 첫 5개의 리뷰를 출력하여 결과를 확인.
# enumerate를 사용하여 인덱스와 값을 동시에 받아옴.
for i, review in enumerate(review_list[:5]):
  print(f"리뷰 {i+1} : {review}")




