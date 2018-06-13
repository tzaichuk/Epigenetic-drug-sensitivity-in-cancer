from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine, desc, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, Text, Float, ForeignKey

import pandas as pd


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

engine = create_engine("sqlite:///cancer_cells.db")

Base = automap_base()

class Cell(Base):
    #Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
    __tablename__ = 'cell_data'
    __table_args__ = {'sqlite_autoincrement': True}
    cell_id = Column(Integer, primary_key=True)
    sample_id = Column(Text)
    tcga = Column(Text)
    tissue = Column(Text)
    tissue_subtype = Column(Text)
    ic50 = Column(Float)
    auc = Column(Float)

Base.prepare(engine, reflect=True)
session = Session(engine)

dacinostat_data = pd.read_csv("dacinostat.csv")
belinostat_data = pd.read_csv("belinostat.csv")
all_data = dacinostat_data.append(belinostat_data)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tissue', methods=['GET', 'POST'])
def names():
    result = engine.execute('SELECT "tissue" FROM '
                            '"cell_data"')
    resultset = [row['tissue'] for row in result]

    print(jsonify(list(set(resultset))))
    return jsonify(list(set(resultset)))

@app.route('/tissue/<sample>')
def metadata(sample):
    result = engine.execute('SELECT * FROM '
                            '"cell_data" where "sample_id" == "' + sample + '"')
    resultset = [dict(row) for row in result][0]

    print("results", resultset)
    metadict = {
        "ID": resultset['sample_id'],
        "TCGA": resultset['tcga'],
        "TISSUE": resultset['tissue'],
        "TISSUE_SUBTYPE": resultset['tissue_subtype'],
        "ic50": resultset['ic50'],
    }
    print("metadict", metadict)
    return jsonify(metadict)

@app.route('/samples/<sample>')
def samples(sample):
    filtered_data = all_data[all_data.tissue == sample]
    data = filtered_data[['tissue_subtype', 'ic50']]
    s = data.groupby('tissue_subtype').sum().reset_index()

    tissue_subtype = s['tissue_subtype'].values.tolist()
    tissue_ic50 = list()
    for x in tissue_subtype:
        y = s[s.tissue_subtype == x]['ic50'].values[0]
        tissue_ic50.append(y)
    sampdict = {"tissue_subtype": tissue_subtype,
                "tissue_values": tissue_ic50}
    print(sampdict)
    return jsonify(sampdict)

@app.route('/cell')
def cell():
    result = engine.execute('SELECT "sample_id" FROM '
                            '"cell_data"')
    resultset = [row['sample_id'] for row in result]

    print("/cell results", resultset)
    return jsonify(resultset)

if __name__ == '__main__':
    app.run(debug=True)
