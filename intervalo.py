# Usamos mpmath para las funciones elementales (exp, log, sin, cos, tan, etc)
# para adem\'as poder usar precisi\'on extendida
# NOTA

from sympy.mpmath import mp, mpf

class Intervalo(object):

    """
    Se define la clase 'Intervalo', y la aritm\'etica b\'asica de intervalos, 
    es decir, suma, resta, multiplicaci\'on y divisi\'on. 

    Se carga antes (internamente) mp y mpf de mpmath para usar las funciones 
    elementales y poder usar precisi\'on extendida de manera sencilla.
    """

    def __init__(self, a, b=None):
        """ 
        Se define la clase 'Intervalo', y los m\'etodos para la aritm\'etica 
        b\'asica de intervalos, es decir, suma, resta, multiplicaci\'on y 
        divisi\'on. 
        Se incluyen otras funciones (sin, cos, exp, log) que ser\'an \'utiles.
        """

        
        if isinstance(a, Intervalo):  # "copy constructor"
        	self.lo, self.hi = a.lo, a.hi
        	return

        if b is None:  # single argument, so make thin interval
            b = a

        elif (b < a):  # limits wrong way round; not right approach for extended IA
            a, b = b, a

        # print(a, type(a), b, type(b))

        a = make_mpf(a)
        b = make_mpf(b)

        self.lo, self.hi = a, b
        
        # self.lo, self.hi = lo, hi
            

    # Lo siguiente sirve para dar informaci\'on bonita del objeto `Intervalo`
    #
    def __repr__(self):
        return "Intervalo [{},{}]".format(repr(self.lo),repr(self.hi))
    
    def __str__(self):
        return "[{},{}]".format(self.lo,self.hi)


    # Aqu\'i vienen las operaciones aritm\'eticas y varias funciones
    #
    def __add__(self, otro):
        """
        Suma de intervalos
        """

        otro = Intervalo(otro)
        return Intervalo(self.lo + otro.lo, self.hi + otro.hi)
        
    def __radd__(self, otro):
        return self + otro


    def __sub__(self, otro):
        """
        Resta de intervalos
        """

        otro = Intervalo(otro)
        return Intervalo( self.lo - otro.hi, self.hi - otro.lo )
        
    def __rsub__(self, otro):
        return -(self - otro)


    def __pos__(self):
        return self

    def __neg__(self):
        """
        El negativo de un intervalo
        """
        return Intervalo(-self.hi,-self.lo)
    
    def __mul__(self, otro):
        """
        Se implementa la multiplicaci\'on usando `multFast`
        """

        otro = Intervalo(otro)
        return self.mult2(otro)
        
    def __rmul__(self, otro):
        return self * otro


    def mult1(self,otro):
        """ Algor\'itmo de la multiplicaci\'on ingenuo """
        S = [ self.lo*otro.lo, self.lo*otro.hi, 
              self.hi*otro.lo, self.hi*otro.hi ]
        return Intervalo( min(S), max(S) )

    def mult2(self,otro):
        """
        Algor\'itmo de la multiplicaci\'on que distingue los nueve casos posibles
        """
        if (self.lo >= 0.0 and otro.lo >= 0.0):
            return Intervalo( self.lo*otro.lo, self.hi*otro.hi )
        elif (self.hi < 0.0 and otro.hi < 0.0):
            return Intervalo( self.hi*otro.hi, self.lo*otro.lo )
        elif (self.lo >= 0.0 and otro.hi < 0.0):
            return Intervalo( self.lo*otro.hi, self.hi*otro.lo )
        elif (self.hi < 0.0 and otro.lo >= 0.0):
            return Intervalo( self.hi*otro.lo, self.lo*otro.hi )
        elif (self.lo >= 0.0 and otro.lo*otro.hi < 0.0):
            return Intervalo( self.hi*otro.lo, self.hi*otro.hi )
        elif (self.hi < 0.0 and otro.lo*otro.hi < 0.0):
            return Intervalo( self.lo*otro.hi, self.lo*otro.lo )
        elif (otro.lo >= 0.0 and self.lo*self.hi < 0.0):
            return Intervalo( self.lo*otro.hi, self.hi*otro.hi )
        elif (otro.hi < 0.0 and self.lo*self.hi < 0.0):
            return Intervalo( self.hi*otro.lo, self.lo*otro.lo )

        else: #(self.lo*self.hi < 0.0 and otro.lo*otro.hi < 0.0):

            S1 = [ self.lo*otro.lo, self.hi*otro.hi ]
            S2 = [ self.hi*otro.lo, self.lo*otro.hi ]
            return Intervalo( min(S2), max(S1) )

    def __div__(self, otro):
        """
        Divisi\'on de intervalos: producto del primero por el rec\'iproco del segundo
        """
        otro = Intervalo(otro)
        try:
            return self * otro.reciprocal()
        except ZeroDivisionError:
            print "To divide by an interval containining 0, we need to implement extended intervals!"
            # put extended interval code here

    def __rdiv__(self, otro):
        # Esto se encarga de cosas tipo numero/intervalo; self es el intervalo
        return (self / otro).reciprocal()


    def __contains__(self, x):
        """
        Esto verifica si el intervalo contiene (o no) un n\'umero real
        """
        return self.lo <= x <= self.hi

    def __abs__(self):  # use as abs(i)
        return max( abs(self.lo), abs(self.hi) )


    def abs(self):     # use as i.abs()
        return abs(self)


    def reciprocal(self):
        """
        Esto define el rec\'iproco de un intervalo
        """
        if 0 in self:
            raise ZeroDivisionError("Interval {} in denominator contains 0.".format(self))

        return Intervalo( 1.0/self.hi, 1.0/self.lo )

    
        # pow, rpow, abs, sin, cos, ...


    def exp(self):
        """Exponencial de un intervalo: 'self.exp()'"""
        return Intervalo( mp.exp(self.lo), mp.exp(self.hi))

    def log(self):
        """Logaritmo de un intervalo: 'self.log()'"""
        return Intervalo( mp.log(self.lo), mp.log(self.hi))

    def __pow__(self, exponent):
        """
        Se calcula la potencia de un intervalo; operador '**'
        NOT YET IMPLEMENTED
        """
        raise NotImplementedError('self**exponent is not yet implemented for Intervalo')

    def sin(self):
        """
        Se calcula el seno de un intervalo
        NOT YET IMPLEMENTED
        """
        raise NotImplementedError('self.sin() is not yet implemented for Intervalo')

    def cos(self):
        """
        Se calcula el seno de un intervalo
        NOT YET IMPLEMENTED
        """
        raise NotImplementedError('self.cos() is not yet implemented for Intervalo')


    #    # TESTING
    #    #if 0 in self and exponent < 0:
    #    #    raise ZeroDivisionError("Interval {} in denominator contains 0.".format(self))
    #    #
    #    #if exponent > 0:
    #    #
    #    #    if self.lo<0:
    #    #        raise ValueError("Negative number cannot be raised to a fractional power")
    #    #    else:
    #    #        return Intervalo(self.lo**exponent, self.hi**exponent)
    #    #else:
    #    #    try:
    #    #        return (self.reciprocal())**(-exponent)
    #    #    except:
    #    #        raise ZeroDivisionError(0.0 cannot be raised to a negative power)
    #    return Intervalo( self.lo**exponent, self.hi**exponent )

    # Las relaciones que sirven para checar el orden parcial
    def __eq__(self, otro):
        """
        Aqu\'i se checa la igualdad de dos intervalos; operador '=='
        """
        try:
            return self.lo == otro.lo and self.hi == otro.hi
        except:
            return self == Intervalo(otro)

    def __ne__(self, otro):
        """
        Aqu\'i se checa la NO igualdad de dos intervalos; operador '!='
        """
        return not self == otro

    def __le__(self, otro):
        """
        Se checa el ordenamiento de los intervalos (ver Tucker); 
        operador '<='
        """
        try:
            return self.lo <= otro.lo and self.hi <= otro.hi
        except:
            return self <= Intervalo(otro)

    def __rle__(self, otro):
        return self >= otro

    def __ge__(self, otro):
        """ 
        Se checa el ordenamiento de los intervalos (ver Tucker); 
        operador '>='
        """
        try:
            return self.lo >= otro.lo and self.hi >= otro.hi
        except:
            return self >= Intervalo(otro)

    def __rge__(self, otro):
        return self <= otro

    def __lt__(self, otro):
        """
        Se checa el ordenamiento de los intervalos (ver Tucker); 
        operador '<'
        """
        try:
            return self.lo < otro.lo and self.hi < otro.hi
        except:
            return self < Intervalo(otro)

    def __rlt__(self, otro):
        return self > otro

    def __gt__(self, otro):
        """
        Se checa el ordenamiento de los intervalos (ver Tucker); 
        operador '>'
        """
        try:
            return self.lo > otro.lo and self.hi > otro.hi
        except:
            return self > Intervalo(otro)

    def __rgt__(self, otro):
        return self < otro

    # Las operaciones entre intervalos vistas como conjuntos 
    def _is_empty_intersection(self, otro):
        """Verifica si la intersecci\'on de los intervalos es vac\'ia"""
        return self.hi < otro.lo or otro.hi < self.lo

    def intersection(self, otro):
        """
        Intersecci\'on de intervalos
        """
        if not isinstance(otro, Intervalo):
            otro = Intervalo(otro)
        if self._is_empty_intersection(otro):
            print "Intersection is empty: " \
                  "Intervals {} and {} are disjoint".format(self,otro)
        else:
            return Intervalo( max(self.lo,otro.lo), min(self.hi,otro.hi) )

    def hull(self, otro):
        """Envoltura/caso de dos intervalos"""
        return Intervalo( min(self.lo,otro.lo), max(self.hi,otro.hi) )

    def union(self, otro):
        """Uni\'on de intervalos"""
        if not isinstance(otro, Intervalo):
            otro = Intervalo(otro)
        if self._is_empty_intersection(otro):
            print "Union yields no connected interval: " \
                  "Intervals {} and {} are disjoint".format(self,otro)
        else:
            return self.hull(otro)

    # Algunas funciones escalares de intervalos
    def diam(self):
        return self.hi-self.lo

    def centre(self):
        return 0.5*(self.lo+self.hi)

    def mag(self):
        """Distancia m\'axima (magnitude) al origen"""
        return max( abs(self.lo), abs(self.hi) )

    def mig(self):
        """Distancia m\'inima (mignitude) al origen"""
        if 0 in self:
            return 0
        else:
            return min( abs(self.lo), abs(self.hi) )

    # Representaciones especiales para el IPython Notebook:
    def _repr_html_(self):
        #return "[{}, {}]".format(self.lo, self.hi)
        representation = "[{}, {}]".format(self.lo, self.hi)
        representation = representation.replace("inf", r"&infin;")
        return representation

    def _repr_latex_(self):
        return "$[{}, {}]$".format(self.lo, self.hi)


def make_mpf(a):

	if isinstance(a, mpf):
		return a

	return mpf(str(a))

def exp(a):
    return a.exp()



# Correct (directed) rounding:
# in each calculation of the lower bound, "floor" rounding must be used;
# for the upper bound, "ceiling" rounding

# In mpmath, use keyword arguments  rounding="f"  or  rounding="c", respectively

# E.g. to construct the thin interval 0.1, we use:
# mp.pretty = False
# a = mpf("0.1", rounding="f")
# b = mpf("0.1", rounding="c")
# i = Intervalo(a, b)
# i.lo, i.hi
