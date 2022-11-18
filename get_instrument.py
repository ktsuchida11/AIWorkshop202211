import tpqoa
import numpy as np
import pandas as pd
import json

api = tpqoa.tpqoa('pyalgo.cfg')

summary = api.get_account_summary()

print("balance:" + json.dumps(summary['balance'], indent=2))

inst = api.get_instruments()

print(json.dumps(inst[:10], indent=2))

instrument = 'EUR_USD'
start = '2022-11-15'
end = '2022-11-17'
granularity = 'M1'
price = 'M'

data = api.get_history(instrument, start, end,
                      granularity, price)

print(data)

data['returns'] = np.log(data['c'] / data['c'].shift(1))

cols = []

for momentum in [15,30,60,120]:
    col = 'position_{}'.format(momentum)
    data[col] = np.sign(data['returns'].rolling(momentum).mean())
    cols.append(col)

from pylab import plt
plt.style.use('seaborn')
import matplotlib as mpl
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['font.family'] = 'serif'

strats = ['returns']

for col in cols:
    strat = 'strategy_{}'.format(col.split('_')[1])
    data[strat] = data[col].shift(1) * data['returns']
    strats.append(strat)

data[strats].dropna().cumsum(
    ).apply(np.exp).plot(figsize=(10, 6));

plt.show()

instrument = 'EUR_USD'

api.stream_data(instrument, stop=10)