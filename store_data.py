from sqlalchemy import create_engine


class Store():
    def store_to_csv(self, loc, df):
        df.to_csv(loc, mode='a', encoding='utf-8')

    def store_to_sql(self, df, name="india"):
        engine = create_engine(f"mysql://abhay:1234@localhost/covid_db")
        con = engine.connect()
        df.to_sql(con=con, name=name,
                  if_exists='replace')
