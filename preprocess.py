import pandas as pd
import numpy as np
import pyproj as proj
import os
from sqlalchemy import create_engine
from geoalchemy2 import Geometry, WKTElement


def preprocess(filename: str) -> pd.DataFrame :
    csv_file = pd.read_csv(filename, header=0, index_col=False, encoding='UTF8')
    print(csv_file)
    csv_file = csv_file.loc[csv_file['영업상태구분코드'] == 1]
    # 소재지전체주소가 없는 경우도 있음 없으면 False(na =False)
    # csv_file = csv_file.loc[csv_file['소재지전체주소'].str.contains('서울', na=False) | csv_file['도로명전체주소'].str.contains('서울', na=False)]
    

    df = pd.DataFrame()
    df[['id']] = csv_file[['번호']]
    df[['category']] = csv_file[['업태구분명']]

    df[['province', 'city', 'lot_number']] = csv_file['소재지전체주소'].str.extract('(\w+)\s(\w+)\s(.+)', expand=True)
    df[['road_name']] = csv_file['도로명전체주소'].str.extract('(\w+)\s(\w+)\s([^()]+\s(\w+))', expand=True)[[2]]

    df[['manage_number']] = csv_file[['관리번호']]

    df[['name']] = csv_file[['사업장명']]
    df['name_for_query'] = df['name'].str.replace('\s', '', regex=True)

    
    coord = np.array(csv_file[['좌표정보(X)','좌표정보(Y)']])
    result = project_array(coord, 'EPSG:5174', 'EPSG:4326')

    # 5174 -> 3857 -> 4326 매핑 (결과에 큰 차이는 없음)
    # result = project_array(coord, 'EPSG:5174', 'EPSG:3857')
    # result = project_array(result, 'EPSG:3857', 'EPSG:4326')

    df['y'] = result[:, 1]
    df['x'] = result[:, 0]

    df['coordinates'] = df[['x','y']].apply(create_wkt_element, axis=1)
    

    # 앞,뒤 공백 제거
    df['road_name'].str.strip()
    df['lot_number'].str.strip()
    df['name'].str.strip()
    df['category'].str.strip()
    df['manage_number'].str.strip()

    # 고정값 채워넣기
    df = df.assign(registered=False)
    df = df.assign(status='OPENED')
    df = df.assign(restaurant_id=None)
    print(df)
    return df

def project_array(coord, p1_type, p2_type):
    p1 = proj.Proj(init=p1_type)
    p2 = proj.Proj(init=p2_type)
    fx, fy = proj.transform(p1, p2, coord[:, 0], coord[:, 1])
    return np.dstack([fx, fy])[0]

def create_wkt_element(coord):
    return WKTElement(to_wkt(coord), srid = 4326)

def to_wkt(coord) :
    return "POINT(" + str(coord[1]) + " " + str(coord[0]) + ")"

def save(df: pd.DataFrame, filepath: str) :
    createFolder(filepath)
    df.to_csv(f"{filepath}/result.csv", index= False)


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

def insert_to_db(df: pd.DataFrame) :
    user = 'root'
    password = 'password'
    host = 'localhost'
    port = '3306'
    scheme = 'local_db'
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{scheme}?charset=utf8")
    engine.connect()
    df.to_sql(name='restaurant_data', con=engine, if_exists='append', index=False, dtype={'coordinates': Geometry('POINT', srid=4326)})