import numpy as np
from matplotlib import pyplot as pl
from astropy.io import fits

# function to read fits files
def read(band):
    hdulist = fits.open('W3+3-2.'+band+'.12901_13028_7448_7575.fits')
    x = hdulist[0].data
    h = hdulist[0].header
    h = str(h)
    h = h.partition('EXPTIME =')[2]
    h = h.partition('/')[0]
    x /= int(h)
#    lo,hi = np.percentile(x,2),np.percentile(x,99) #non-linear
#    print(band,lo,hi)
    lo,hi = 0,0.01    #linear stretch so UV is faint
    x = np.clip(x,lo,hi) #for each pix, clip betw. hi & lo
    
#  normalize to 1.0 
    x = 0.01 + 0.99*(x-lo)/(hi-lo)
     #    x = (x-lo)/(hi-lo)
    
    #grab size of image W; w == white == grey
    W = len(x)
    w = np.zeros(shape=(W,W,3), dtype=float)
    # make a greyscale image; [xpix,ypix,primaryColourIndex]
    for c in range(3):
        w[:,:,c] = 1*x
    return w
# end of function to read fits files
    
# defining the blending mode algorithms
# screen blending    
def screen(b,f):
    return 1 - (1-b)*(1-f)

# Call function to read fits files
u = read('U')
g = read('G')
r = read('R')
i = read('I2')
z = read('Z')
W = len(u)

# Defining primary hues
black = np.zeros(shape=(W,W,3), dtype=float)
red = 1*black
red[:,:,0] = 1 # set the 0th element (R of RGB) of all pixels equal to 1.
green = 1*black
green[:,:,1] = 1
blue = 1*black
blue[:,:,2] = 1


# colour definitions for filters
ucol = (181*red + 1*green + 254*blue)/255
gcol = (254*red + 1*green + 245*blue)/255
rcol = (254*red + 63*green + 0*blue)/255
icol = 1 - gcol  # across the colour wheel
zcol = 1 - ucol

# using screen blending mode
img = z*zcol
img = screen(img,i*icol)
img = screen(img,r*rcol)
img = screen(img,g*gcol)
img = screen(img,u*ucol)

# Deal with zeros by taking max value of R,G or B and store value/pix.
gr = np.amax(img,axis=2)
lo,hi = np.amin(gr),np.amax(gr)
print('img range',lo,hi)

# Stretches
#img /= hi #if overshooting - deprecated by screen algorithm
#img = img**.5  #square root
img = np.log(1e-6+img/lo) #log
lo,hi = np.amin(img),np.amax(img) #log rescale to max = 1.0
print('img range',lo,hi)
img /= hi  #if overshooting - deprecated by screen algorithm

# Display image
pl.imshow(img, origin='lower', interpolation='nearest')
#pl.xlim((0,127))
#pl.ylim((127,0))
pl.show()





