# run using the command "nosetests" in the current directory
# nosetests finds tests with name "test_..."
# (nose must be installed, of course)

from intervalo import *

def test_adicion():
	a = Intervalo(1, 2)
	b = Intervalo(3, 4)

	c = a + b

	assert c.lo == 4 and c.hi == 6
	