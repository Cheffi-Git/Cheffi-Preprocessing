import pandas as pd

if __name__ == '__main__':
    csv_file = pd.read_csv('/source.csv',header=0, encoding='cp949')
    csv_file = csv_file.loc[csv_file['영업상태구분코드'] == 1]
    # 소재지전체주소가 없는 경우도 있음 없으면 False(na =False)
    csv_file = csv_file.loc[csv_file['소재지전체주소'].str.contains('서울', na=False) | csv_file['도로명전체주소'].str.contains('서울', na=False)]
    

    df = pd.DataFrame()
    df[['id']] = csv_file[['번호']]
    df[['category']] = csv_file[['업태구분명']]

    df[['province', 'city', 'lot_number']] = csv_file['소재지전체주소'].str.extract('(\w+)\s(\w+)\s(.+)', expand=True)
    df[['road_name']] = csv_file['도로명전체주소'].str.extract('(\w+)\s(\w+)\s([^()]+)', expand=True)[[2]]

    df[['manage_number']] = csv_file[['관리번호']]

    df[['name']] = csv_file[['사업장명']]
    df['name_for_query'] = df['name'].str.replace('\s', '', regex=True)

    
    df[['x','y']] = csv_file[['좌표정보(x)','좌표정보(y)']]

    # 앞,뒤 공백 제거
    df['road_name'].str.strip()
    df['lot_number'].str.strip()
    df['name'].str.strip()
    df['category'].str.strip()
    df['manage_number'].str.strip()

    # 고정값 채워넣기
    df = df.assign(registered=False)
    df = df.assign(status='OPENED')
    df = df.assign(restaurant_id='NaN')

    df.to_csv('./result/restaurant_data.csv',index=False)


