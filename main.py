import  preprocess as pp
from datetime import datetime

if __name__ == '__main__':
    df = pp.preprocess('source.xlsx')
    pp.save(df, f'./result/{datetime.today().strftime("%Y%m%d%H%M%S")}')

