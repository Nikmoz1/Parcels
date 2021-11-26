import pandas as pd
from dto import SizeEntity


class TableProcessing:
    @staticmethod
    def getting_table():
        list_size_object = []
        parcels = pd.read_excel('test_table.xlsx', sheet_name='Sheet1')
        df = pd.DataFrame(parcels)
        sizes_of_parcels = df.filter(items=['BOX 1 LENGTH', 'BOX 1 DEPTH/WIDTH', 'BOX 1 HEIGHT', 'BOX 1 LBS'])
        for row in sizes_of_parcels.itertuples(index=True):
            size_object = SizeEntity(id=row[0], length=row[1], width=row[2], height=row[3], lbs=row[4])
            list_size_object.append(size_object)
        return list_size_object
