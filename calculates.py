import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.linear_model import LinearRegression
from DBimports import getGoals
from DBconnect import cur

goals = list(getGoals())
df = pd.DataFrame(goals, columns=['home_score', 'away_score'])

print("Sum:", np.sum(goals))
print("Mean:", np.mean(goals))
print("Std", np.std(goals))

# #Test normalności
stat, p = stats.normaltest(df['home_score'])
print('p= %.3f' % p)

# #analiza wariancji
k = df['home_score'].var(ddof=0)
print('k=%.1f' % k)

# #niezależne
test_2 = stats.ttest_ind(df['home_score'], df['away_score'])
print("Test: ", test_2[1])

# #zależne
test_4 = stats.ttest_rel(df['home_score'], df['away_score'])
print("Test: ", test_4[1])

# #regresja liniowa
x = np.array(df['home_score']).reshape((-1, 1))
y = np.array(df['away_score'])

model = LinearRegression()
model.fit(x, y)
model = LinearRegression().fit(x, y)

r_sq = model.score(x, y)
print('coefficient of determination:', r_sq)

# # ZADANIE 7
cur.callproc('byYears')
result_data = list(cur.fetchall())
df = pd.DataFrame(result_data, columns=['year', 'home_score', 'away_score'])

plt.bar(df['year'], df['home_score'])
plt.show()
plt.bar(df['year'], df['away_score'], color='orange')
plt.show()
