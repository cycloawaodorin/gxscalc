import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['axes.axisbelow'] = True
cmap = plt.get_cmap('tab10')

def _mmean(df, s, r):
	return df.rolling(s*r+1, center=True, win_type='gaussian', min_periods=1).mean(std=s)

def _intersection(x00, y00, x01, y01, x10, y10, x11, y11):
	n0, n1 = (x10*y11-x11*y10), (x00*y01-x01*y00)
	x0, x1 = x00-x01, x10-x11
	y0, y1 = y00-y01, y10-y11
	den = x1*y0-x0*y1
	x, y = (x0*n0-x1*n1)/den, (y0*n0-y1*n1)/den
	return (x, y)

def _cross(on, off, *, std=5, rng=10, rf=False):
	x = on[:-1].reset_index()['speed']
	y = _mmean(on[1:].reset_index()['speed']-x, std, rng)
	df1 = pd.DataFrame({'speed': x, 'accel': y})
	x = off[:-1].reset_index()['speed']
	y = _mmean(off[1:].reset_index()['speed']-x, std, rng)
	df0 = pd.DataFrame({'speed': x, 'accel': y})
	for i in range(len(df0)-1):
		s0b, s0a = df0.loc[:, 'speed'].iloc[i], df0.loc[:, 'speed'].iloc[i+1]
		a0b, a0a = df0.loc[:, 'accel'].iloc[i], df0.loc[:, 'accel'].iloc[i+1]
		bef = df1.query(f'{s0b}<=speed')
		if len(bef)==0:
			continue
		aft = df1.query(f'speed<={s0a}')
		if len(aft)==0:
			continue
		df1_in = df1.loc[bef.index[-1]:aft.index[0], :]
		for j in range(len(df1_in)-1):
			s1b, s1a = df1_in.loc[:, 'speed'].iloc[j], df1_in.loc[:, 'speed'].iloc[j+1]
			a1b, a1a = df1_in.loc[:, 'accel'].iloc[j], df1_in.loc[:, 'accel'].iloc[j+1]
			s, a = _intersection(s0a, a0a, s0b, a0b, s1a, a1a, s1b, a1b)
			if s0a<=s<=s0b and s1a<=s<=s1b:
				if rf:
					fig = plt.figure()
					ax = fig.add_subplot(xlabel='Speed [km/h]', ylabel='Acceleration [km/h/f]')
					ax.plot(df1.loc[:, 'speed'], df1.loc[:, 'accel'], label='on', color=cmap(0))
					ax.plot(df0.loc[:, 'speed'], df0.loc[:, 'accel'], label='off', color=cmap(1))
					ax.scatter([s], [a], marker='x', label='MT point', color=cmap(2), zorder=2)
					ax.grid()
					ax.legend()
					return (s, a, fig, ax)
				else:
					return (s, a)
	if rf:
		fig = plt.figure()
		ax = fig.add_subplot(xlabel='Speed [km/h]', ylabel='Acceleration [km/h/f]')
		ax.plot(df1.loc[:, 'speed'], df1.loc[:, 'accel'], label='on')
		ax.plot(df0.loc[:, 'speed'], df0.loc[:, 'accel'], label='off')
		ax.grid()
		ax.legend()
		return (None, None, fig, ax)
	else:
		return (None, None)

def _b1bd(b, th):
	for i in range(len(b)-1):
		if (b.loc[:, 'speed'].iat[i] - b.loc[:, 'speed'].iat[i+1]) > th:
			return (b.loc[:, 'speed'].iat[i], i)

def mtp(on, off, *, std=5, rng=10, return_figure=False, with_frames=True):
	if not isinstance(on, pd.DataFrame):
		if with_frames:
			on = pd.read_csv(on, sep='\s+', names=['frame', 'speed'])
		else:
			on = pd.read_csv(on, sep='\s+', names=['speed'])
	if not isinstance(off, pd.DataFrame):
		if with_frames:
			off = pd.read_csv(off, sep='\s+', names=['frame', 'speed'])
		else:
			off = pd.read_csv(off, sep='\s+', names=['speed'])
	return _cross(on, off, std=std, rng=rng, rf=return_figure)

def calc(accel, boost, on, off, *, duration_threshold=4):
	a = pd.read_csv(accel, sep='\s+', names=['frame', 'speed'])
	b = pd.read_csv(boost, sep='\s+', names=['frame', 'speed'])
	on = pd.read_csv(on, sep='\s+', names=['frame', 'speed'])
	off = pd.read_csv(off, sep='\s+', names=['frame', 'speed'])
	top = a.loc[:, 'speed'].max()
	a800 = a.query('speed>=800').loc[:, 'frame'].iat[0]
	mtp, decel = _cross(on, off)
	b1, bd = _b1bd(b, duration_threshold)
	b1300 = b.query('speed>=1300').loc[:, 'frame'].iat[0]
	b4 = b[:241].loc[:, 'speed'].max()
	b10 = b.loc[:, 'speed'].max()
	return (top, a800, mtp, decel, b1, bd, b1300, b4, b10)

def _distance(df, fps):
	ret = 0
	sp = df.loc[:, 'speed'].iat[0]/3.6
	for i in range(len(df)-1):
		sp2 = df.loc[:, 'speed'].iat[i+1]/3.6
		ret += (sp+sp2)/(fps*2)
		sp = sp2
	return ret

def distance(file, fps=60, *, with_frames=True):
	if not isinstance(file, pd.DataFrame):
		if with_frames:
			df = pd.read_csv(file, sep='\s+', names=['frame', 'speed'])
		else:
			df = pd.read_csv(file, sep='\s+', names=['speed'])
	return _distance(df, fps)
