def mround(x):
	if x < 0.01:
		return str(x)

	rounded = str(round(x, 2))

	if len(rounded.split('.')) == 1:
		rounded += ".00"
	elif len(rounded.split('.')[1]) == 1:
		rounded += "0"

	return rounded