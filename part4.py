# Name: Linya Li
# Uniq Id:linyal

import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as offline
import csv


f = open('noun_data.csv')
csv_data = csv.reader(f)

word = []
freq = []
for row in csv_data:
    word.append(row[0])
    freq.append(int(row[1]))

data = [go.Bar(
            x = word,
            y = freq
    )]

layout = go.Layout(
    title='Most Frequent Nouns',
)

fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='part4_viz_image')
