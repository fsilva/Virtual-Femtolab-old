import pylab
from numpy import *
from numpy.fft import *

max_t = 128e-15  #s 
num_p = 128
t_fwhm = 10e-15 #s
GVD = 362e-30    #s

t = arange(-max_t,max_t,2*max_t/num_p)
#freqs = 2*pi*arange(-1/max_t/2.,1/max_t/2.,1/max_t/num_p)
#freqs = roll(freqs,num_p/2)
freqs = 2*pi*fftfreq(num_p,2*max_t/num_p)

t_sigma = t_fwhm/2.3548
t_sigma *= sqrt(2) #t_fwhm is for the intensity envelope
E = exp(-t**2/(2*t_sigma**2))
fft_E = fft(E)

fft_E *= exp(1j*freqs**2*GVD/2.)
E2 = ifft(fft_E)

pylab.plot(t,abs(E)**2)
pylab.plot(t,abs(E2)**2)
pylab.show()

#calculate intensity envelope
env1 = abs(E)**2
env2 = abs(E2)**2
        
# calculate FWHM by gaussian fit
X = arange(len(env1))
x = sum(X*env1)/sum(env1)
width = sqrt(abs(sum((X-x)**2*env1)/sum(env1)))
fwhm1 = 2.3548*width*2*max_t/num_p

# calculate FWHM by gaussian fit
X = arange(len(env2))
x = sum(X*env2)/sum(env2)
width = sqrt(abs(sum((X-x)**2*env2)/sum(env2)))
fwhm2 = 2.3548*width*2*max_t/num_p

print 'initial = ',fwhm1*1e15,' fs\n final = ',fwhm2*1e15,' fs' 


