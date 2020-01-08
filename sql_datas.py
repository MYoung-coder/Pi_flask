import psycopg2

def latest_row():
    conn = psycopg2.connect(dbname="AgroIot", user="postgres",password="950315", host="39.97.186.109", port="5432")
    cur = conn.cursor()
    str_sql = "select * from dbo.klha_data"
    cur.execute(str_sql)
    rows = cur.fetchall()
    # print(len(rows))
    # print(rows[-1])
    data_time=rows[-1][5].strftime(('%H:%M %d/%m') )
    # print(data_time)
    soil_humidity=rows[-1][4]
    soil_temp=rows[-2][4]
    light=rows[-3][4]
    air_humidity=rows[-4][4]
    air_temp=rows[-5][4]
    latest_row_data=[air_temp,air_humidity,light,soil_temp,soil_humidity,data_time]
    conn.commit()
    conn.close()
    # print(latest_row_data)
    return latest_row_data

# latest_row()