import csv
from datetime import datetime
from matplotlib import pyplot as plt

# 从文件中获取日期、最高气温和最低气温
filename1 = 'sitka_weather_2014.csv'
with open(filename1) as f1:
    reader1 = csv.reader(f1)
    header_row1 = next(reader1)

    dates1, highs1 ,lows1 = [], [], []
    for row1 in reader1:
        current_date1 = datetime.strptime(row1[0], "%Y-%m-%d")
        dates1.append(current_date1)

        high1 = int(row1[1])
        highs1.append(high1)

        low1 = int(row1[3])
        lows1.append(low1)

filename2 = 'death_valley_2014.csv'
with open(filename2) as f2:
    reader2 = csv.reader(f2)
    header_row2 = next(reader2)

    dates2, highs2, lows2 = [], [], []
    for row2 in reader2:
        try:
            current_date2 = datetime.strptime(row2[0], "%Y-%m-%d")
            high2 = int(row2[1])
            low2 = int(row2[3])
        except ValueError:
            print(current_date2, 'missing date')
        else:
            dates2.append(current_date2)
            highs2.append(high2)
            lows2.append(low2)

# 根据数据绘制图形
fig1 = plt.figure(dpi=128, figsize=(10, 5))
plt.plot(dates1, highs1, c='red',alpha=0.5)
plt.plot(dates1, lows1, c='green',alpha=0.5)
plt.fill_between(dates1,highs1,lows1,facecolor='green',alpha=0.1)

fig2 = plt.figure(dpi=128, figsize=(10, 5))
plt.plot(dates2, highs2, c='red',alpha=0.5)
plt.plot(dates2, lows2, c='green',alpha=0.5)
plt.fill_between(dates2,highs2,lows2,facecolor='green',alpha=0.1)

# 设置图形的格式
plt.title('Compare',fontsize=23)
plt.xlabel('',fontsize=16)
fig1.autofmt_xdate()
fig2.autofmt_xdate()
plt.ylabel("Temperature(F)",fontsize=16)
plt.tick_params(axis='both',which='major',labelsize=16)

plt.show()

