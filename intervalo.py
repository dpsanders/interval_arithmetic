# -*- coding: utf-8 -*-

# Usamos mpmath para las funciones elementales (exp, log, sin, cos, tan, etc)
# para adem\'as poder usar precisi\'on extendida

from sympy.mpmath import mp, mpf
import numpy as np

class Intervalo(object):
    """
    Se define la clase 'Intervalo', y la aritm\'etica b\'asica de intervalos, 
    es decir, suma, resta, multiplicaci\'on y divisi\'on, y las funciones básicas.

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

        if b is None:  # single argument, so make thin interval
            b = a

        elif (b < a):  # limits wrong way round; not right approach for extended IA
            a, b = b, a

        # print(a, type(a), b, type(b))

        a = make_mpf(a)
        b = make_mpf(b)

        self.lo, self.hi = a, b
            

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

        otro = self.make_interval(otro)
        return Intervalo(self.lo + otro.lo, self.hi + otro.hi)
        
    def __radd__(self, otro):
        return self + otro


    def __sub__(self, otro):
        """
        Resta de intervalos
        """

        otro = self.make_interval(otro)
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

        otro = self.make_interval(otro)
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
        otro = self.make_interval(otro)

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

    def strictly_contains(self, x):
        return self.lo < x < self.hi


    def __abs__(self):  # use as abs(i)
        """La máxima distancia de los bordes al cero"""
        return max( abs(self.lo), abs(self.hi) )


    def abs(self):     # use as i.abs()
        return abs(self)


    def reciprocal(self):
        """
        Esto define el rec\'iproco de un intervalo
        """
        if self.strictly_contains(0):
            txt_error = "Interval {} in denominator contains 0.".format(self)
            raise ZeroDivisionError( txt_error )

        try:
            lower = 1. / self.hi
        except:
            lower = - mpf("inf")

        try:
            upper = 1. / self.lo
        except:
            upper = mpf("inf")

        #return Intervalo( 1.0/self.hi, 1.0/self.lo )
        return Intervalo(lower, upper)

    
    # pow, rpow, abs, sin, cos, ...

    def exp(self):
        """
        Exponencial de un intervalo: 'self.exp()'
        """
        return Intervalo( mp.exp(self.lo), mp.exp(self.hi) )

    def log(self):
        """
        Logaritmo de un intervalo: 'self.log()'

        NOTA: Si el intervalo contiene al 0, pero no es estrictamente negativo,
        se calcula el logaritmo de la intersecci\'on  del intervalo con el dominio
        natural del logaritmo, i.e., [0,+inf].
        """
        
        if 0 in self:

            domainNatural = Intervalo( 0, mpf('inf') )
            intervalRestricted = self.intersection( domainNatural )

            txt_warning = "\nWARNING: Interval {} contains 0.\n".format(self)
            print txt_warning
            
            txt_warning = "Restricting to the intersection "\
                  "with the natural domain of log, i.e. {}\n".format(intervalRestricted)
            print txt_warning
            
            return Intervalo( mp.log(intervalRestricted.lo), mp.log(intervalRestricted.hi) )

        elif 0 > self.hi:
            txt_error = 'Interval {} < 0\nlog cannot be computed '\
                'for negative numbers.'.format(self)
            raise ValueError( txt_error )

        else:
            return Intervalo( mp.log(self.lo), mp.log(self.hi) )


    def __pow__(self, exponent):
        """
        Se calcula la potencia de un intervalo; operador '**'
        UNDER TESTING
        """
        if isinstance( exponent, Intervalo ): # exponent is an interval

            if exponent.lo == exponent.hi: # exponent is a thin interval
                return self**exponent.lo

            else: # exponent is a generic interval
                return ( exponent*self.log() ).exp()

        else: # exponent is a number (int, float, mpf, ...)
            
            if exponent == int(exponent):  # exponent is an integer

                if exponent >= 0:
                    if exponent%2 == 0:  # even exponent
                        return Intervalo( self.mig()**exponent, self.mag()**exponent )

                    else:  # odd exponent
                        return Intervalo( self.lo**exponent, self.hi**exponent )

                else:   # exponent < 0
                    return (self**(-exponent)).reciprocal()

            else:
                # exponent is a generic float
                if exponent >= 0:
                    if 0 in self:
                        domainNatural = Intervalo( 0, mpf('inf') )
                        intervalRestricted = self.intersection( domainNatural )

                        txt_warning = "\nWARNING: Interval {} contains 0.\n".format(self)
                        print txt_warning

                        txt_warning = "Restricting to the intersection "\
                              "with the natural domain of **, i.e. {}\n".format(intervalRestricted)
                        print txt_warning

                        return Intervalo( 0, self.hi**exponent )

                    else:
                        return Intervalo( self.lo**exponent, self.hi**exponent )

                else:
                    return (self**(-exponent)).reciprocal()

    def __rpow__(self,exponent):
        return Intervalo(exponent)**self


    def sin(self):
        """
        Se calcula el seno de un intervalo
        TEST CAREFULLY
        """
        pi = mp.pi
        pi_half = 0.5 * pi
        dospi = 2.0 * pi
        xlow, xhig = self.lo, self.hi
        whole_range = Intervalo(-1,1)

        # Check the specific case:
        if xhig > xlow + dospi: # more than 1 full period away
            return whole_range
        
        else: # within 1 full period of sin(x); 20 cases
            # some abreviations
            lo_mod2pi = xlow % dospi
            hi_mod2pi = xhig % dospi
            lo_quarter = mp.floor( lo_mod2pi / pi_half )
            hi_quarter = mp.floor( hi_mod2pi / pi_half )
            sin_xlo = mp.sin( xlow )
            sin_xhi = mp.sin( xhig )
            min_sin, max_sin = sin_xlo, sin_xhi
            if sin_xhi < sin_xlo:
                min_sin, max_sin = sin_xhi, sin_xlo
                
            if lo_quarter == hi_quarter: # mismo cuadrante --> 8 casos

                if lo_mod2pi <= hi_mod2pi:
                    return Intervalo( sin_xlo, sin_xhi )
                else:
                    return whole_range

            else:
                
                if ( lo_quarter == 3 and hi_quarter==0 ) or \
                ( lo_quarter == 1 and hi_quarter==2 ) : # 2 cases
                    return Intervalo( sin_xlo, sin_xhi )
                
                elif ( lo_quarter == 0 or lo_quarter==3 ) and \
                ( hi_quarter==1 or hi_quarter==2 ) : # 4 cases
                    return Intervalo( min_sin, 1 )
                
                elif ( lo_quarter == 1 or lo_quarter==2 ) and \
                ( hi_quarter==3 or hi_quarter==0 ) : # 4 cases
                    return Intervalo( -1, max_sin )
                
                elif ( lo_quarter == 0 and hi_quarter==3 ) or \
                ( lo_quarter == 2 and hi_quarter==1 ) : # 2 cases
                    return whole_range
                
                else: # This should be never reached!
                    raise NotImplementedError( 'SOMETHING WENT WRONG. This should have never\
                        been reached' )


    def cos(self):
        """
        Se calcula el coseno de un intervalo
        TEST CAREFULLY
        """
        pi = mp.pi
        pi_half = 0.5 * pi
        dospi = 2.0 * pi
        xlow, xhig = self.lo, self.hi
        whole_range = Intervalo(-1,1)

        # Check the specific case:
        if xhig > xlow + dospi: # more than 1 full period away
            return whole_range
        
        else: # within 1 full period of sin(x); 20 cases
            # some abreviations
            lo_mod2pi = xlow % dospi
            hi_mod2pi = xhig % dospi
            lo_quarter = mp.floor( lo_mod2pi / pi_half )
            hi_quarter = mp.floor( hi_mod2pi / pi_half )
            cos_xlo = mp.cos( xlow )
            cos_xhi = mp.cos( xhig )
            min_cos, max_cos = cos_xlo, cos_xhi
            if cos_xhi < cos_xlo:
                min_cos, max_cos = cos_xhi, cos_xlo
                
            if lo_quarter == hi_quarter: # mismo cuadrante --> 8 casos

                if lo_mod2pi <= hi_mod2pi:
                    return Intervalo( cos_xlo, cos_xhi )
                else:
                    return whole_range

            else:
                
                if ( lo_quarter == 2 and hi_quarter==3 ) or \
                ( lo_quarter == 0 and hi_quarter==1 ) : # 2 cases
                    return Intervalo( cos_xlo, cos_xhi )
                
                elif ( lo_quarter == 2 or lo_quarter==3 ) and \
                ( hi_quarter==0 or hi_quarter==1 ) : # 4 cases
                    return Intervalo( min_cos, 1 )
                
                elif ( lo_quarter == 0 or lo_quarter==1 ) and \
                ( hi_quarter==2 or hi_quarter==3 ) : # 4 cases
                    return Intervalo( -1, max_cos )
                
                elif ( lo_quarter == 3 and hi_quarter==2 ) or \
                ( lo_quarter == 1 and hi_quarter==0 ) : # 2 cases
                    return whole_range
                
                else: # This should be never reached!
                    raise NotImplementedError( 'SOMETHING WENT WRONG. This should have never\
                        been reached' )



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
        """Distancia máxima (magnitude) al origen"""
        return max( abs(self.lo), abs(self.hi) )

    def mig(self):
        """Distancia mínima (mignitude) al origen"""
        if 0 in self:
            return 0
        else:
            return min( abs(self.lo), abs(self.hi) )


    # Representaciones especiales para el IPython Notebook:
    def _repr_html_(self):
        reprn = "[{}, {}]".format(self.lo, self.hi)
        reprn = reprn.replace("inf", r"&infin;")
        return reprn

    def _repr_latex_(self):
        return "$[{}, {}]$".format(self.lo, self.hi)

    def make_interval(self, a):
        if isinstance(a, Intervalo):
            return a

        return Intervalo(a)


# Funciones extras
def make_mpf(a):

	if isinstance(a, mpf):
		return a

	return mpf(str(a))


def exp(a):
    return a.exp()


def log(a):
    return a.log()


def sin(a):
    return a.sin()


def cos(a):
    return a.cos()


def split_interval( x, num_divisions=1 ):
    """
    Divide un intervalo en n=num_divisions intervalos iguales
    """
    num_divisions = int(num_divisions)
    if num_divisions < 1:
        num_divisions = 1

    edge_points = np.linspace(x.lo, x.hi, num_divisions+1)
    splited_intervals = [Intervalo(a, b) for (a,b) in zip(edge_points[:-1], edge_points[1:])]

    return splited_intervals


def range_interval_f( fun, subdivided_interval ):
    """
    Evalua la función f(x) extendida sobre intervalos, en una lista de subintervalos
    y regresa el hull de todos ellos, es decir, una cota del rango de la función
    """
    if not isinstance( subdivided_interval, list ):
        subdivided_interval = [ subdivided_interval ]

    range_fun = [ fun(i) for i in subdivided_interval ]
    range_tot = range_fun[0]

    for i in range_fun[1:]:
        range_tot = range_tot.hull(i)

    return range_tot


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
