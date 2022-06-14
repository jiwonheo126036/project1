import pandas as pd
from scipy.spatial import distance
from datetime import datetime
import requests
import random


# In[2]:


# 이용자가 있을 때 - 주 소비 업종
def find_priority_category(user, today):

    priority_df=pd.read_csv('/code/app/csv_file/priority_df.csv', encoding='cp949')

    target=pd.concat([user, today], axis=1)
    sim=list(priority_df[['age', 'gender', 'season', 'wcondition', 'date']].apply(lambda x: distance.euclidean(x, target), axis=1))
    idx=sim.index(min(sim))
    upjong=priority_df[['first1', 'second', 'third', 'fourth', 'fifth', 'sixth']].iloc[idx]
    if user.sex[0]==0:
        top6_upjong=upjong.replace('u5', 'u5_1')
    elif user.sex[0]==1:
        top6_upjong=upjong.replace('u5', 'u5_2')
    return top6_upjong  


# # 은수님 코드에서 출력물을 rs로 받아옴
# ai_js = json.loads(rs)
# ai_result = pd.DataFrame(ai_js, index=[0])
# ai_result.rename(columns={'gender':'sex'}, inplace=True)




# ai_result={'gender': 1, 'age': 1}
# ai_result = pd.DataFrame(ai_result, index=[0])
# ai_result.rename(columns={'gender':'sex'}, inplace=True)
# 코드 돌려보려고 ai_result 임의로 넣음.



def get_base_time():
    if datetime.now().hour <11 :
        base_time = '0800'
    elif datetime.now().hour < 14 :
        base_time = '1100'
    elif datetime.now().hour < 17 :
        base_time = '1400'
    elif datetime.now().hour < 20:
        base_time = '1700'
    return base_time



def get_items(time):
        
        
    vilage_weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?"

    service_key = "zdllRmKK82EGkx6HI0QiOGIjN6xR5K8Hq4axIQMvzkOzsVMFD4vXR2pRnSL3FffZqt8tEud2Sk/HsIZh8aTJ6Q=="

    today = datetime.today()
    base_date = today.strftime("%Y%m%d") 
    base_time = time
    

    nx = "59"
    ny = "126"

    payload = "serviceKey=" + service_key + "&" +        "dataType=json" + "&" +        "base_date=" + base_date + "&" +        "base_time=" + base_time + "&" +        "nx=" + nx + "&" +        "ny=" + ny

    res = requests.get(vilage_weather_url + payload)

    items = res.json().get('response').get('body').get('items')
    return items



def get_today_info(items):
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
    today = datetime.today()

    data['wcondition'] = weather_state
    data['season'] = season
    data['date'] = today.weekday()

    today_info=pd.DataFrame(data, columns = ['season','wcondition', 'date'], index=[0], dtype=int)
    return today_info



today_info = get_today_info(get_items(get_base_time()))



# 이용객 있는 경우
def show_ad_with_user(f):
    
    ads = pd.read_csv('/code/app/csv_file/ads.csv')
    
    first1, second, third, fourth, fifth, sixth = f[0],f[1],f[2],f[3],f[4],f[5]
    
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

    # random.choice(f_l), random.choice(s_l), random.choice(t_l), random.choice(fo_l), random.choice(fi_l), random.choice(si_l)
    # url_list = {"url_list": [random.choice(f_l), random.choice(s_l), random.choice(t_l), random.choice(fo_l), random.choice(fi_l), random.choice(si_l)]}
    
    return [random.choice(f_l), random.choice(s_l), random.choice(t_l), random.choice(fo_l), random.choice(fi_l), random.choice(si_l)]
    



def result_population(age, gender):
    ai_result ={'age': age, 'sex': gender}
    ai_result_frame = pd.DataFrame(ai_result, index=[0])
    category = find_priority_category(ai_result_frame, today_info)
    res = show_ad_with_user(category)
    
    return res











