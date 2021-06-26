import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['axes.axisbelow'] = True

def _mmean(df, s, r):
	return df.rolling(s*r+1, center=True, win_type='gaussian', min_periods=1).mean(std=s)

def _cross(on, off, *, std=5, rng=10, rf=False):
	x = on[:-1].reset_index()['speed']
	y = _mmean(on[1:].reset_index()['speed']-x, std, rng)
	df1 = pd.DataFrame({'speed': x, 'accel': y})
	x = off[:-1].reset_index()['speed']
	y = _mmean(off[1:].reset_index()['speed']-x, std, rng)
	df0 = pd.DataFrame({'speed': x, 'accel': y})
	for j in range(len(df0)-1):
		x0b, x0a = df0['speed'].iat[j], df0['speed'].iat[j+1]
		bef = df1.query(f'{x0b}<=speed')
		if len(bef)==0:
			continue
		aft = df1.query(f'speed<={x0a}')
		y0b, y0a = df0['accel'].iat[j], df0['accel'].iat[j+1]
		x1b, x1a = bef['speed'].iat[-1], aft['speed'].iat[0]
		y1b, y1a = bef['accel'].iat[-1], aft['accel'].iat[0]
		if y1b<=y0b and y0a<=y1a:
			alp0 = (y0b-y0a)/(x0b-x0a)
			bet0 = (x0b*y0a-x0a*y0b)/(x0b-x0a)
			alp1 = (y1b-y1a)/(x1b-x1a)
			bet1 = (x1b*y1a-x1a*y1b)/(x1b-x1a)
			spd = (bet1-bet0)/(alp0-alp1)
			acl = (alp0*bet1-alp1*bet0)/(alp0-alp1)
			if rf:
				fig = plt.figure()
				ax = fig.add_subplot(xlabel='Speed [km/h]', ylabel='Acceleration [km/h/f]')
				ax.plot(df1['speed'], df1['accel'], label='on')
				ax.plot(df0['speed'], df0['accel'], label='off')
				ax.grid()
				ax.legend()
				return (spd, acl, fig, ax)
			else:
				return (spd, acl)

def _b1bd(b, th):
	for i in range(len(b)-1):
		if (b['speed'].iat[i] - b['speed'].iat[i+1]) > th:
			return (b['speed'].iat[i], i)

def mtp(on, off, *, std=5, rng=10, return_figure=False):
	on = pd.read_csv(on, sep='\s+', names=['frame', 'speed'])
	off = pd.read_csv(off, sep='\s+', names=['frame', 'speed'])
	return _cross(on, off, std=std, rng=rng, rf=return_figure)

def calc(accel, boost, on, off, *, duration_threshold=4):
	a = pd.read_csv(accel, sep='\s+', names=['frame', 'speed'])
	b = pd.read_csv(boost, sep='\s+', names=['frame', 'speed'])
	on = pd.read_csv(on, sep='\s+', names=['frame', 'speed'])
	off = pd.read_csv(off, sep='\s+', names=['frame', 'speed'])
	top = a['speed'].max()
	a800 = a.query('speed>=800')['frame'].iat[0]
	mtp, decel = _cross(on, off)
	b1, bd = _b1bd(b, duration_threshold)
	b1300 = b.query('speed>=1300')['frame'].iat[0]
	b4 = b[:241]['speed'].max()
	b10 = b['speed'].max()
	return (top, a800, mtp, decel, b1, bd, b1300, b4, b10)

def _distance(df, fps):
	ret = 0
	sp = df['speed'].iat[0]/3.6
	for i in range(len(df)-1):
		sp2 = df['speed'].iat[i+1]/3.6
		ret += (sp+sp2)/(fps*2)
		sp = sp2
	return ret

def distance(file, fps=60):
	df = pd.read_csv(file, sep='\s+', names=['frame', 'speed'])
	return _distance(df, fps)
