

df = pd.read_csv(Location,delimiter=',', encoding = "ISO-8859-1",header=None)
df.sort_values(['Like Count'], ascending=False).plot(x='Like Count',y='Star Count')
     ...: df.sort_values(['Like Count'], ascending=False).plot(x='Like Count',y='Subject WC')
     ...: df.sort_values(['Like Count'], ascending=False).plot(x='Like Count',y='Content WC')
     ...: df.sort_values(['Like Count'], ascending=False).plot(x='Like Count',y='Days')
     ...: df.sort_values(['Like Count'], ascending=False).plot(x='Like Count',y='Attacheds')