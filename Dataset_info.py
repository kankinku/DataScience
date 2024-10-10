import requests
import pandas as pd

# API 설정
api_key = '9f5af280224642b8c4ee5606010b8c34'  # 실제 API 키 입력
base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'

# 파일 경로 설정
input_csv_file = 'movie_names.csv' 
output_csv_file = 'movie_info.csv'  

# 입력 CSV 파일 읽기
movie_codes_df = pd.read_csv(input_csv_file)

# 결과를 저장할 리스트
results = []

# 각 영화 코드에 대해 API 요청
for index in range(len(movie_codes_df)):
    movie_cd = movie_codes_df.iloc[index, 0]  # 두 번째 열에서 영화 코드 가져오기

    # API 요청
    response = requests.get(f"{base_url}?key={api_key}&movieCd={movie_cd}")
    
    if response.status_code == 200:
        data = response.json()  # JSON으로 변환
        movie_info = data.get('movieInfoResult', {}).get('movieInfo', {})
        
        # 영화 정보 추출
        if movie_info:
            # 원하는 필드 추출 +영화 매출액, 영화 순수익액
            movie_cd = movie_info.get('movieCd', 'N/A')  # 영화 코드
            movie_nm = movie_info.get('movieNm', 'N/A')  # 영화명 (국문)
            movie_nm_en = movie_info.get('movieNmEn', 'N/A')  # 영화명 (영문)
            prdt_year = movie_info.get('prdtYear', 'N/A')  # 제작연도
            show_tm = movie_info.get('showTm', 'N/A')  # 상영시간
            open_dt = movie_info.get('openDt', 'N/A')  # 개봉일
            prdt_stat_nm = movie_info.get('prdtStatNm', 'N/A')  # 제작상태
            type_nm = movie_info.get('typeNm', 'N/A')  # 영화유형
            nations = ', '.join(nation['nationNm'] for nation in movie_info.get('nations', [])) or 'N/A'  # 제작국가
            genres = ', '.join(genre['genreNm'] for genre in movie_info.get('genres', [])) or 'N/A'  # 장르
            directors = ', '.join(director['peopleNm'] for director in movie_info.get('directors', [])) or 'N/A'  # 감독
            actors = ', '.join(actor['peopleNm'] for actor in movie_info.get('actors', [])) or 'N/A'  # 배우
            watch_grade_nm = ', '.join(aud['watchGradeNm'] for aud in movie_info.get('audits', [])) or 'N/A'  # 관람등급
            # CSV에 저장할 정보
            movie_info_row = [
                movie_cd, movie_nm, movie_nm_en, prdt_year, show_tm, open_dt,
                prdt_stat_nm, type_nm, nations, genres, directors, actors, watch_grade_nm
            ]
            results.append(movie_info_row)
        else:
            print(f"No movie info found for movie code {movie_cd}")
    else:
        print(f"Error: {response.status_code} for movie code {movie_cd}")

# 결과를 DataFrame으로 변환 및 저장
if results:
    columns = [
        'Movie Code', 'Movie Name (Korean)', 'Movie Name (English)', 'Production Year',
        'Running Time', 'Open Date', 'Production Status', 'Movie Type',
        'Nations', 'Genres', 'Directors', 'Actors', 'Watch Grade'
    ]
    results_df = pd.DataFrame(results, columns=columns)
    results_df.to_csv(output_csv_file, index=False)
    print(f"데이터가 {output_csv_file}로 저장되었습니다.")
else:
    print("저장할 데이터가 없습니다.")
