from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd

def Load_Data(file_name):
    data = pd.read_csv(file_name, delimiter=',')

    return data.values.tolist()

Base = declarative_base()

class Cell(Base):
    #Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
    __tablename__ = 'cell_data'
    __table_args__ = {'sqlite_autoincrement': True}
    cell_id = Column(Integer, primary_key=True)
    sample_id = Column(String)
    tcga = Column(String)
    tissue = Column(String)
    tissue_subtype = Column(String)
    ic50 = Column(Float)
    auc = Column(Float)

if __name__ == "__main__":

    #Create the database
    engine = create_engine('sqlite:///cancer_cells.db')
    Base.metadata.create_all(engine)

    #Create the session
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    try:
        file_name = "dacinostat.csv"
        data = Load_Data(file_name)
        idx = 0
        for i in data:
            record = Cell(**{
                'cell_id': idx,
                'sample_id' : i[0],
                'tcga' : i[1],
                'tissue' : i[2],
                'tissue_subtype' : i[3],
                'ic50' : i[4],
                'auc' : i[5]
            })
            print(type(record))
            s.add(record) #Add all the records
            idx += 1
        file_name = "belinostat.csv"  # sample CSV file used:  http://www.google.com/finance/historical?q=NYSE%3AT&ei=W4ikVam8LYWjmAGjhoHACw&output=csv
        data = Load_Data(file_name)

        for i in data:
            record = Cell(**{
                'cell_id' : idx,
                'sample_id': i[0],
                'tcga': i[1],
                'tissue': i[2],
                'tissue_subtype': i[3],
                'ic50': i[4],
                'auc': i[5]
            })
            print(record)
            s.add(record)  # Add all the records
            idx += 1
        s.commit() #Attempt to commit all the records
        print("successfully committed")
    except:
        print("Exception occurred")
        s.rollback() #Rollback the changes on error
    finally:
        s.close() #Close the connection

