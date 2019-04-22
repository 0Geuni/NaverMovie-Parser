# 사이트 접속 모듈
import urllib.request
# 문자열 처리 모듈
import re
# 파싱 / 데이터 처리 모듈
from bs4 import BeautifulSoup
# print 보다 깨끗하게 정리해서 출력해주는 모듈
from pprint import pprint
# SQlite3 DB
import sqlite3

# 네이버 영화 객체
class NaverMovie_Core:
     # 영화 순위 가져오기
    def NaverMovie(self):
        # 네이버 영화 랭킹 URL
        NaverMovieURL = "https://movie.naver.com/movie/sdb/rank/rmovie.nhn"
        # 네이버 영화 기본 페이지 URL
        NaverBaseURL = "https://movie.naver.com"

        # 네이버 영화 열기 | timeout 은 10초 동안 접속이 안 될 경우 끊기
        OpenNaverMovie = urllib.request.urlopen(NaverMovieURL, timeout=10)
        # 네이버 영화 페이지 읽기
        ReadNaverMovie = OpenNaverMovie.read()

        # BeautifulSoup 에서 HTML 형식으로 파싱
        SoupNaverMovie = BeautifulSoup(ReadNaverMovie, "html.parser")

        # 네이버 영화 | 영화 랭킹 검색
        # id 값이 container 인 태그를 찾는다
        Find_NaverMovie_container = SoupNaverMovie.find(id="container")
        # class 값이 old_layout old_super_db 인 태그를 찾는다
        Find_NaverMovie_class_db = Find_NaverMovie_container.find(class_="old_layout old_super_db")
        # id 값이 cbody | class 값이 type_1 인 태그를 찾는다
        Find_NaverMovie_cbody = Find_NaverMovie_class_db.find(id="cbody", class_="type_1")
        # id 값이 old_content 인 태그를 찾는다
        Find_NaverMovie_old_content = Find_NaverMovie_cbody.find(id="old_content")
        # Table 태그를 검색
        Find_NaverMovie_Table = Find_NaverMovie_old_content.find("table", class_="list_ranking")
        # tbody 태그를 검색
        Find_NaverMovie_tbody = Find_NaverMovie_Table.find("tbody")
        # tr 태그들을 검색 해서 Tuple 형태로 저장
        Find_NaverMovie_tr = Find_NaverMovie_tbody.find_all("tr")

        # 1 ~ 50 까지 영화 순위가 담기는 Tuple 형태의 리스트
        MovieRank = []
        # 1 ~ 50 까지 영화 정보 링크가 담기는 Tuple 형태의 리스트
        MovieInfo_Link = []
        # 1 ~ 50 까지 영화 고유 코드가 담기는 Tuple 형태의 리스트
        MovieCode = []

        # for(반복문)을 돌려 Find_NaverMovie_tr 에 있는 영화 데이터를 index에 담아준다
        for index in Find_NaverMovie_tr:
            # 만약에 index 안에 class 명이 title 인 태그가 있다면 찾는다
            if index.find(class_="title"):
                # movie_index 변수에 tit3 를 가진 태그 안에 a 태그 데이터를 찾아 담는다
                movie_index = index.find(class_="tit3").find("a")
                # 링크와 코드 처리를 위한 변수 생성
                href_index = movie_index["href"]
                # MovieRank(list) 에 정제 된 영화 제목 데이터를 추가한다
                MovieRank.append(movie_index["title"])
                # MovieInfo_Link(list) 에 정제 된 영화 정보 링크를 추가한다
                MovieInfo_Link.append(NaverBaseURL + href_index)
                # MovieCode(list) 에 정제 된 영화 코드를 추가한다 | 뒤에서 여섯 개의 문자 추출
                MovieCode.append("".join(list(filter(str.isdigit, href_index[-6:]))))

            else:
                # pass | else 문을 들어 올 경우 그냥 넘겨서 다음 for 문이 실행 될 수 있도록 한다
                pass

        # 영화 포스터 이미지 URL
        MovieIMG_URL = "https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode="
        # 네이버 영화 출연자 URL
        MoviePerfomer_URL = "https://movie.naver.com/movie/bi/mi"
        # 영화 개별 데이터가 담기는 리스트
        # 이미지
        MovieIMG = []
        # 영어 제목
        MovieTitle_en = []
        # 관람객 평점
        MovieAudience_Score = []
        # 기자 · 평론가 평점
        MovieReporter_Critic_Score = []
        # 네티즌 평점
        MovieNetizen_Score = []
        # 장르
        MovieGenre = []
        # 국가
        MovieCountry = []
        # 상영시간
        MovieTime = []
        # 개봉일
        MovieRelease_Date = []
        # 감독
        MovieDirector = []
        # 출연자 링크
        MoviePerformer_Link = []
        # 등급
        MovieRating = []
        # 예매율
        MovieTicketRate = []
        # 누적관객
        MovieCumulaAudience = []

        # self 인자를 통해서 영화 상세 정보 페이지 URL을 가져온다 | MovieInfo_Link
        # 1 ~ 50까지 데이터가 담겨 있음
        # 영화 데이터 하나씩 정리 | index 에 0 부터 MovieInfo_Link 리스트 안에 있는 갯수 만큼 대입
        for index in range(0, len(MovieInfo_Link)):
            # 네이버 영화 정보 열기 | timeout 은 10초 동안 접속이 안 될 경우 끊기
            MovieMore_urlopen = urllib.request.urlopen(MovieInfo_Link[index], timeout=10)
            # 네이버 영화 정보 페이지 읽기
            Read_MovieMore_url = MovieMore_urlopen.read()
            # BeautifulSoup 에서 HTML 형식으로 파싱
            SoupMovieMore = BeautifulSoup(Read_MovieMore_url, "html.parser")

            # html -> body 태그 이동
            Find_MovieMoreTag = SoupMovieMore.find(id="container")
            # div class="article" 검색
            Find_MovieMore_article = Find_MovieMoreTag.find(class_="article")
            # div class="mv_info_area" 검색
            Find_MovieMore_mvinfoarea = Find_MovieMore_article.find(class_="mv_info_area")
            # div class="mv_info" 검색
            Find_MovieMore_mvinfo = Find_MovieMore_mvinfoarea.find(class_="mv_info")
            # 평점 | div class="main_score" 검색
            Find_MovieMore_Score = Find_MovieMore_mvinfo.find(class_="main_score")

            # **이미지**
            MovieIMG_Link = MovieIMG_URL + MovieCode[index]
            MovieIMG.append(MovieIMG_Link)

            # **영어 제목**
            Title_lang_en = Find_MovieMore_mvinfo.strong.get_text()
            MovieTitle_en.append(Title_lang_en)

            # **관람객 평점**
            try:
                Audience_Score = Find_MovieMore_Score.find(class_="ntz_score")
                Audience_Score = Audience_Score.find(class_="star_score")
                Audience_Score = Audience_Score.find_all("em")

                for i in range(0, len(Audience_Score)):
                    Audience_Score[i] = Audience_Score[i].get_text()

                Audience_Score = "".join(Audience_Score)
                if Audience_Score == "":
                    Audience_Score = "0.00"

                MovieAudience_Score.append(Audience_Score)
            except:
                MovieAudience_Score.append("0.00")

            # **기자 · 평론가 평점**
            try:
                Reporter_Critic_Score = Find_MovieMore_Score.find(class_="spc_score_area")
                Reporter_Critic_Score = Reporter_Critic_Score.find(class_="star_score")
                Reporter_Critic_Score = Reporter_Critic_Score.find_all("em")

                for i in range(0, len(Reporter_Critic_Score)):
                    Reporter_Critic_Score[i] = Reporter_Critic_Score[i].get_text()

                Reporter_Critic_Score = "".join(Reporter_Critic_Score)

                if Reporter_Critic_Score == "":
                    Reporter_Critic_Score = "0.00"

                MovieReporter_Critic_Score.append(Reporter_Critic_Score)
            except:
                MovieReporter_Critic_Score.append("0.00")

            # **네티즌 평점**
            try:
                Netizen_Score = Find_MovieMore_Score
                Netizen_Score = Netizen_Score.find(class_="star_score")
                Netizen_Score = Netizen_Score.find_all("em")

                for i in range(0, len(Netizen_Score)):
                    Netizen_Score[i] = Netizen_Score[i].get_text()

                Netizen_Score = "".join(Netizen_Score)

                if Netizen_Score == "":
                    Netizen_Score = "0.00"

                MovieNetizen_Score.append(Netizen_Score)
            except:
                MovieNetizen_Score.append("0.00")

            # 영화 정보 | 개요, 감독, 출연, 등급, 흥행
            MovieInfo = Find_MovieMore_mvinfo.find(class_="info_spec")
            MovieInfo = MovieInfo.find_all("dd")

            # *개요* [0]
            Summary_info = MovieInfo[0].p.find_all("span")

            # **장르** -[0]
            try:
                Genre = Summary_info[0].find_all("a")

                for i in range(0, len(Genre)):
                    Genre[i] = Genre[i].get_text()

                MovieGenre.append(Genre)
            except:
                MovieGenre.append(["-"])

            # **국가** -[1]
            try:
                Country = Summary_info[1].find_all("a")

                for i in range(0, len(Country)):
                    Country[i] = Country[i].get_text()

                MovieCountry.append(Country)
            except:
                MovieCountry.append(["-"])

            # **상영시간** -[2] | 분
            try:
                Time = Summary_info[2].get_text()
                MovieTime.append(str(Time))
            except:
                MovieTime.append("0")

            # **개봉일** -[3]
            try:
                Release_Date = Summary_info[3].find_all("a")

                for i in range(0, len(Release_Date)):
                    Release_Date[i] = Release_Date[i].get_text()

                Release_Date = "".join(Release_Date).strip()
                MovieRelease_Date.append(Release_Date)
            except:
                MovieRelease_Date.append("0000.00.00")

            # **감독** [1]
            try:
                Director = MovieInfo[1].p.find("a").get_text()
                MovieDirector.append(Director)
            except:
                MovieDirector.append("-")

            # **출연 링크** [2]
            Performer_Link = MoviePerfomer_URL + "/detail.nhn?code=" + MovieCode[index]
            MoviePerformer_Link.append(Performer_Link)

            # **등급** [3]
            try:
                Rating = MovieInfo[3].p.find("a").get_text()
                MovieRating.append(Rating)
            except:
                MovieRating.append("-")

            # *흥행* [4]
            try:
                MovieBO = MovieInfo[4].div
            except:
                MovieBO = "None"

            # **예매율** | 명
            try:
                TicketRate = MovieBO.find(class_="rate")
                TicketRate = TicketRate.find("a").get_text()
                MovieTicketRate.append(str(TicketRate))
            except:
                MovieTicketRate.append("0")

            # **누적관객**
            try:
                Cumulative_Audience = MovieBO.find(class_="count").get_text()
                MovieCumulaAudience.append(Cumulative_Audience)
            except:
                MovieCumulaAudience.append("0")

        MovieCharacters = []
        
        # MoviePerformer_Link | 출연자 목록 [이름, 연기, 역할, 프로필링크]
        for index in range(0, len(MoviePerformer_Link)):
            MoviePerLink = urllib.request.urlopen(MoviePerformer_Link[index], timeout=10)
            ReadMoviePerLink = MoviePerLink.read()
            SoupMoviePerLink = BeautifulSoup(ReadMoviePerLink, "html.parser")

            Act_Lv1 = SoupMoviePerLink.find(class_="lst_people_area height100")
            try:
                Act_Lv2 = Act_Lv1.find("ul")

                Act_Thumb = Act_Lv2.find_all(class_="p_thumb")
                Act_Info = Act_Lv2.find_all(class_="p_info")

                Thumb_list = []
            except:
                pass
            
            try:
                for x in range(0, len(Act_Thumb)):
                    try:
                        th = Act_Thumb[x].find("a").find("img")["src"]
                    except:
                        th = "프로필 없음"
                    try:
                        name = Act_Info[x].find("a")["title"]
                    except:
                        name = "이름 없음"

                    try:
                        act = Act_Info[x].find(class_="part").find(class_="in_prt").find("em").get_text()
                    except:
                        act = "단역 없음"

                    try:
                        role = Act_Info[x].find(class_="part").find(class_="pe_cmt").find("span").get_text()
                    except:
                        role = "역할 없음"

                    Thumb_list.append([
                        name,
                        act,
                        role,
                        th
                    ])
            except:
                Thumb_list.append([
                        "이름 없음",
                        "단역 없음",
                        "역할 없음",
                        "프로필 없음"
                    ])

            MovieCharacters.append(Thumb_list)

        # 이후 여기서 데이터 리턴
        returnDataList = []

        for index in range(0, 50):
            NumData = str(index + 1)
            returnDataList.append([
                # 순번
                NumData,
                # 영화 제목 한국어
                MovieRank[index],
                # 영화 제목 영어
                MovieTitle_en[index],
                # 고유 코드
                MovieCode[index],
                # 영화 포스터(고화질)
                MovieIMG[index],
                # 관람객 평점
                MovieAudience_Score[index],
                # 기자 · 평론가 평점
                MovieReporter_Critic_Score[index],
                # 네티즌 평점
                MovieNetizen_Score[index],
                # 장르
                MovieGenre[index],
                # 국가
                MovieCountry[index],
                # 상영 시간
                MovieTime[index],
                # 개봉일
                MovieRelease_Date[index],
                # 감독
                MovieDirector[index],
                # 영화 등급(국내)
                MovieRating[index],
                # 예매율
                MovieTicketRate[index],
                # 누적 관객
                MovieCumulaAudience[index],
                # 배우 목록
                MovieCharacters[index]
            ])

        return returnDataList

'''
def DB_con():
    Naver = NaverMovie_Core().NaverMovie()
    data_col = "Rank, Name_ko, Name_en, inher_Code, Post_Link, AudienceScore, ReporterCriticScore, NetizenScore, Genre, Country, Time, ReleaseDate, Director, Rating, TicketRate, CumulaAudience"
    data_num = "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"

    with sqlite3.connect(r"/Naver_MovieDB.sqlite") as conn:
        cursor = conn.cursor()
        
        sql = "insert into naver_movie ({0}) values ({1})".format(data_col, data_num)

        cursor.executemany(sql, Naver)

        conn.commit()
        cursor.close()
'''

Naver = NaverMovie_Core()
pprint(Naver.NaverMovie()[0])

# DB_con()