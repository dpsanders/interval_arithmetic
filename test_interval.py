# run using the command "nosetests" in the current directory
# nosetests finds tests with name "test_..."
# (nose must be installed, of course)

from intervalo import *

# Lo siguiente se necesita para verificar 'errores' que usan 'raise'
from nose.tools import *

def test_adicion():
	a = Intervalo(1, 2)
	b = Intervalo(3, 4)
	c1 = a + b
	c2 = a + 4.3
	c3 = 4.3 + a
	assert c1.lo == 4 and c1.hi == 6
	assert c2.lo == 5.3 and c2.hi == 6.3
	assert c3.lo == 5.3 and c3.hi == 6.3
	
#@raises(ValueError)
def test_pow():
	a = Intervalo(-1,1)
	b = a**2
	c = a**Intervalo(2)
	assert b.lo == 0 and b.hi == 1 and c.lo == 0 and c.hi == 1
	b = a**3
	c = a**Intervalo(3)
	assert b.lo == -1 and b.hi == 1 and c.lo == -1 and c.hi == 1
	b = a**2.5
	assert b.lo == 0 and b.hi == 1
	#
	b = Intervalo(-2,-1)
	c = b**2
	assert c.lo == 1 and c.hi == 4
	c = b**3
	assert c.lo == -8 and c.hi == -1
	#c = b**2.5
	#raise ValueError("Lanzar este error es ok")
	#
	c = a**b
	assert c.lo == 1 and c.hi == c.hi == mpf('inf')

@raises(ValueError)
def test_log():
	a = Intervalo(3.2,5)
	b = a.log()
	assert b.lo == mp.log(a.lo) and b.hi == mp.log(a.hi)
	a = Intervalo(-2,5)
	b = a.log()
	assert b.lo == mpf('-inf') and b.hi == mp.log(a.hi)
	b = Intervalo(0).log()
	assert b.lo == mpf('-inf') == b.hi
	b = Intervalo(-5,-2).log()
	raise ValueError("Lanzar este error es ok")

