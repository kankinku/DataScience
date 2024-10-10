import requests
import json
import pandas as pd
from datetime import datetime, timedelta

# API key와 기본 URL
api_key = '6e927f984e0745787469e2452351991a'
base_url = 'http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'

# 박스오피스 데이터 가져오기
def get_box_office_data(date):
    url = f'{base_url}?key={api_key}&targetDt={date}'
    res = requests.get(url)
    
    if res.status_code == 200:
        try:
            return json.loads(res.text)['boxOfficeResult']['dailyBoxOfficeList']
        except KeyError:
            print(f"'{date}' 날짜의 박스오피스 데이터가 없습니다.")
            return []
    else:
        print(f"API 요청 실패: {res.status_code} 상태 코드")
        return []

# 시작 날짜 입력 및 끝 날짜 자동 설정
start_date = input("시작일을 입력하세요 (예: 20210501): ")
end_date = datetime.now().strftime("%Y%m%d")

# 영화 데이터를 저장할 리스트
movie_list = []
for day in pd.date_range(start=start_date, end=end_date).strftime("%Y%m%d"):
    movie_list.extend([[b['movieNm'], b['movieCd'], b['audiCnt'], day] for b in get_box_office_data(day)])

# 데이터프레임으로 변환
if movie_list:
    df = pd.DataFrame(movie_list, columns=['영화명', '영화 코드','관객수', '날짜'])
    
    # 중복 제거 (영화명이 같으면 이후에 들어온 데이터만 유지)
    df.drop_duplicates(subset=['영화명'], keep='last', inplace=True)
    
    # 전체 데이터 저장 (영화명, 관객수, 날짜)
    df.to_csv("movie_list.csv", mode='w', encoding='utf-8', header=True, index=False)
    
    # 영화명만 따로 저장
    df[['영화 코드']].to_csv("movie_names.csv", mode='w', encoding='utf-8', header=True, index=False)
    
    print(f"{start_date}부터 {end_date}까지의 영화 데이터가 movie_list.csv에 저장되었습니다.")
    print("중복 제거된 영화명만 movie_names.csv에 저장되었습니다.")
else:
    print("새로 수집된 데이터가 없습니다.")
