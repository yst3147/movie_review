import requests
from bs4 import BeautifulSoup

response = requests.get('https://movie.naver.com/movie/running/current.nhn')
soup = BeautifulSoup(response.text, 'html.parser')

movies_list = soup.select(
    '#content > .article > .obj_section > .lst_wrap > ul > li')

final_movie_data = []

for movie in movies_list:
    a_tag = movie.select_one('dl > dt > a')

    movie_title = a_tag.contents[0]
    movie_code = a_tag['href'].split('code=')[1]
    # split 사용하지 않고 가져오기
    # movie_code = a['href']
    # movie_code = movie_code[movie_code.find('code=') + len('code='):]

    movie_data = {
        'title': movie_title,
        'code': movie_code
    }

    final_movie_data.append(movie_data)


# select 간결하게 가져오기
# 처음 하실 때는 귀찮더라도, 일일히 접근하시면서 구조를 눈에 익히는게 좋습니다..!

# a_list = soup.select(
#     'dl[class=lst_dsc] > dt > a')

# for a in a_list:
#     movie_title = a.text
#     movie_code = a['href'].split('code=')[1]
#     # split 사용하지 않고 가져오기
#     # movie_code = a['href']
#     # movie_code = movie_code[movie_code.find('code=') + len('code='):]
#     print(movie_code, ' ', movie_title)


for movie in final_movie_data:
    #review_url = "https://movie.naver.com/movie/bi/mi/basic.nhn?code=" + movie['code'] + "#tab"
    
    #response = requests.get(review_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    params = (
    ('code', movie['code']),
    ('type', 'after'),
    ('isActualPointWriteExecute', 'false'),
    ('isMileageSubscriptionAlready', 'false'),
    ('isMileageSubscriptionReject', 'false'),
    )

    response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    review = soup.select('div.ifr_area.basic_ifr > .input_netizen > .score_result > ul > li')
    
    i = 0
    for r in review:
        i = str(i)
        score = r.select_one('.star_score > em').text
        reple = r.select_one(f'.score_reple > p > span[id=_filtered_ment_{i}]')
        if reple != None:
            reple = reple.text.replace("\n","").replace("\t", "")
        else:
            reple = reple.select_one('._unfold_ment > a')['data-src']
        print(score)
        print(reple)
        i = int(i) + 1

    break