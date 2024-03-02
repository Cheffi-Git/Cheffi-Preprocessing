import  preprocess as pp
from datetime import datetime

if __name__ == '__main__':
    df = pp.preprocess('source.csv')
    pp.save(df, f'./result/{datetime.today().strftime("%Y%m%d%H%M%S")}')
    pp.insert_to_db(df) 

