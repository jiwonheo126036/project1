import pandas as pd
from scipy.spatial import distance
from datetime import datetime
from pytz import timezone
import requests
import random 

priority_df=pd.read_csv('/code/app/csv_file/priority_df.csv', encoding='cp949')
time_major_local_people=pd.read_csv('/code/app/csv_file/time_major_local_people.csv')
ads = pd.read_csv('/code/app/csv_file/ads.csv')


# 해당 시간대 주요그룹의 - 주 소비 업종 (이용자의 주 소비 업종 찾는 것과 동일)
def find_priority_category(user, today):
    target=pd.concat([user, today], axis=1)
    sim=list(priority_df[['age', 'gender', 'season', 'wcondition', 'date']].apply(lambda x: distance.euclidean(x, target), axis=1))
    idx=sim.index(min(sim))
    upjong=priority_df[['first1', 'second', 'third', 'fourth', 'fifth', 'sixth']].iloc[idx]
    if user.sex[0]==0:
        top6_upjong=upjong.replace('u5', 'u5_1')
    elif user.sex[0]==1:
        top6_upjong=upjong.replace('u5', 'u5_2')
    return top6_upjong      


###### 승진님 코드 : 계절, 날씨, 요일 정보 ~ 
vilage_weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?"

service_key = "zdllRmKK82EGkx6HI0QiOGIjN6xR5K8Hq4axIQMvzkOzsVMFD4vXR2pRnSL3FffZqt8tEud2Sk/HsIZh8aTJ6Q=="

today = datetime.today()
base_date = today.strftime("%Y%m%d") 
base_time = "0800" 

nx = "59"
ny = "126"

payload = "serviceKey=" + service_key + "&" +    "dataType=json" + "&" +    "base_date=" + base_date + "&" +    "base_time=" + base_time + "&" +    "nx=" + nx + "&" +    "ny=" + ny

res = requests.get(vilage_weather_url + payload)

items = res.json().get('response').get('body').get('items')



data = dict()

for item in items['item']:

    # 하늘상태
    if item['category'] == 'SKY':
        
        sky_code = item['fcstValue']
        
        if sky_code =='1':
            sky_state = '0'
        elif sky_code == '3':
            sky_state = '1'
        elif sky_code =='4':
            sky_state = '2'
    
    # 기상상태
    if item['category'] == 'PTY':
        
        weather_code = item['fcstValue']
        
        if weather_code == '1':
            weather_state = '3'
        elif weather_code == '2':
            weather_state = '3'
        elif weather_code == '3':
            weather_state = '3'
        elif weather_code == '4':
            weather_state = '3'
        else:
            weather_state = sky_state
    # 계절
    if (int(item['baseDate'][4:6]) >=3) & (int(item['baseDate'][4:6]) <=5):
        season = '1'
    elif (int(item['baseDate'][4:6]) >=6) & (int(item['baseDate'][4:6]) <=8):
        season = '2'
    elif (int(item['baseDate'][4:6]) >=9) & (int(item['baseDate'][4:6]) <=11):
        season = '3'
    elif int(item['baseDate'][4:6]) in (12, 1, 2):
        season = '4'

data['wcondition'] = weather_state
data['season'] = season
data['date'] = today.weekday()


today_info=pd.DataFrame(data, columns = ['season','wcondition', 'date'], index=[0], dtype=int)

###### ~ 승진님 코드 : 계절, 날씨, 요일 정보


# 이용자가 없을 때 우선순위 그룹 - 주 소비 업종
def when_no_user():
    now_hour = datetime.now(timezone('Asia/Seoul')).hour
    # now_hour=int(datetime.now().hour)
    
    if datetime.now().weekday() < 5:
        now_weekday=1 # 평일 1, 주말 0
    else:
        now_weekday=0

    con=(time_major_local_people.hour==now_hour) & (time_major_local_people.weekday==now_weekday)
    df=time_major_local_people[con][['age', 'sex']].reset_index(drop=True)
    
    priority_category=[]

    for i, j in df.iterrows():
        major_grp=pd.DataFrame(j).T.reset_index(drop=True)
        priority_category.append(find_priority_category(major_grp, today_info))

    return priority_category


# 이용객 있는 경우, 없는 경우 모두 6순위까지
# 이용객 없는 경우는 total_grp 이용해서 실행
def show_ad_with_user(gr):
    
    first1, second, third, fourth, fifth, sixth = gr[0],gr[1],gr[2],gr[3],gr[4],gr[5]
    
    first1_list = ads[ads['라벨링1'] == first1]['파일 경로 (미정)']
    second_list = ads[ads['라벨링1'] == second]['파일 경로 (미정)']
    third_list = ads[ads['라벨링1'] == third]['파일 경로 (미정)']
    fourth_list = ads[ads['라벨링1'] == fourth]['파일 경로 (미정)']
    fifth_list = ads[ads['라벨링1'] == fifth]['파일 경로 (미정)']
    sixth_list = ads[ads['라벨링1'] == sixth]['파일 경로 (미정)']
    
    res = [first1_list, second_list, third_list, fourth_list, fifth_list, sixth_list]
    
    f_l = list(res[0])
    s_l = list(res[1])
    t_l = list(res[2])
    fo_l = list(res[3])
    fi_l = list(res[4])
    si_l = list(res[5])
    # {"url_list": f"{random.choice(f_l)}, {random.choice(s_l)}, {random.choice(t_l)}, {random.choice(fo_l)}, {random.choice(fi_l), random.choice(si_l)}"}
    url_list = {"url_list": [random.choice(f_l), random.choice(s_l), random.choice(t_l), random.choice(fo_l), random.choice(fi_l), random.choice(si_l)]}
    
    return url_list
    
def result_no_population():
    f = when_no_user()[0][:3]
    m = when_no_user()[1][:3]
    total_grp = pd.concat([f,m], axis=0)
    url_list = show_ad_with_user(total_grp)
    return url_list


