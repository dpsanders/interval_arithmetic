import Base.show

type Interval
    lo
    hi
    
    function Interval(a, b)
    	if a > b
    		a, b = b, a
    	end

    	lo, hi = a, b
    	new(lo, hi)

    end
end

I = Interval  # convenience!

Interval(a) = Interval(a, a)  # constructor

+(a::Interval, b::Interval) = Interval(a.lo+b.lo, a.hi+b.hi)
+(a, b::Interval) = Interval(a) + b
+(a::Interval, b) = a + Interval(b)

-(a::Interval) = Interval(-a.hi, -a.lo)  # unary minus
-(a::Interval, b::Interval) = a + (-b)
-(a, b::Interval) = Interval(a) - b
-(a::Interval, b) = a - Interval(b)

function *(a::Interval, b::Interval)
	S = (a.lo*b.lo, a.lo*b.hi, a.hi*b.lo, a.hi*b.hi)
	return Interval(min(S), max(S))
end

*(a::Interval, b) = a * Interval(b)
*(a, b::Interval) = Interval(a) * b

in(x, a::Interval) = a.lo <= x <= a.hi

function reciprocal(a::Interval)
	if zero(a.lo) in a  
		error("Dividing by interval containing 0")
	else
		return Interval(one(a.hi)/a.hi, one(a.lo)/a.lo)
	end
end

/(a::Interval, b::Interval) = a * reciprocal(b)
/(a::Interval, b) = a / Interval(b)
/(a, b::Interval) = Interval(a) / b

intersection(a::Interval, b::Interval) = a.hi < b.lo ? None : Interval(b.lo, a.hi)

show(io::IO, x::Interval) = print("[$(x.lo), $(x.hi)]")




