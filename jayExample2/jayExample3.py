# JE - testing colour tables using square root after colour applied. 

import numpy as np
from matplotlib import pyplot as pl
from astropy.io import fits

def logstretch(x): # doesn't work yet
    x = x + 1e-9
    x = np.log(x)
    x = x/np.amax(x)
    return x

# function to read fits files
def read(band):
    hdulist = fits.open('cps'+band+'J14.fits')
    # working on data that are already in counts per second
    x = hdulist[0].data
    # h = hdulist[0].header
    # h = str(h)
    # h = h.partition('EXPTIME =')[2]
    # h = h.partition('/')[0]
    # x /= int(h)
#    lo,hi = np.percentile(x,2),np.percentile(x,99) #non-linear
#    print(band,lo,hi)
    lo,hi = 0,0.1    #linear stretch so UV is faint
                     # for J14 field the 99.9% level =0.11 for i & z
                     # if stretch u to this then it is fainter than at its 99.9% value of 0.01
    x = np.clip(x,lo,hi) #for each pix, clip betw. hi & lo
    
#  normalize to 1.0 
    x = 0.01 + 0.99*(x-lo)/(hi-lo)
     #    x = (x-lo)/(hi-lo)
    
# stretch
    x = x**.5
#    x = logstretch(x)
    
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
u = read('u')
g = read('g')
r = read('r')
i = read('i') #I2
z = read('z')
W = len(u)

#Apply log before colour assigned
# weird random greytable with and without lomin (wrapping?)
#lomin=0.1
#ulog = np.log(1e-6+u/lomin) 
# ulog = np.log(u)

# Defining primary hues
black = np.zeros(shape=(W,W,3), dtype=float)
red = 1*black
red[:,:,0] = 1 # set the 0th element (R of RGB) of all pixels equal to 1.
green = 1*black
green[:,:,1] = 1
blue = 1*black
blue[:,:,2] = 1


# colour definitions for filters
# Prasenjit's colours
# ucol = (181*red + 1*green + 254*blue)/255
# gcol = (254*red + 1*green + 245*blue)/255
# rcol = (254*red + 63*green + 0*blue)/255
# icol = 1 - gcol  # across the colour wheel
# zcol = 1 - ucol

#chromatic colours
ucol = (180*red + 1*green + 254*blue)/255 #violet
#ucol = np.log(ucol)
#ucol = ucol*5
gcol = (1*red + 1*green + 254*blue)/255   #blue
#gcol = np.log(gcol)
#gcol = gcol*4
rcol = (1*red + 254*green + 1*blue)/255   #green
#rcol = rcol*3
#rcol = np.log(rcol)
icol = (254*red + 128*green + 1*blue)/255 #orange
#icol = icol*2
#icol = np.log(icol)
zcol = (254*red + 1*green + 1*blue)/255 
#zcol = np.log(zcol)

#bwcol = (254*red + 254*green + 254*blue)/255

# using screen blending mode
img = z*zcol
img = screen(img,i*icol)
img = screen(img,r*rcol)
img = screen(img,g*gcol)
img = screen(img,u*ucol)

#Apply log before assign colours.
#img = u*ucol #test one colour:
#img = ulog*bwcol #testing --> weird log -- actually random assigned b&w values

# Deal with zeros by taking max value of R,G or B and store value/pix.
# Note: operating on RGB colour rather than intensity
gr = np.amax(img,axis=2)  #np refers to numpy functions; 2 is colour; (0,1) are position.
lo,hi = np.amin(gr),np.amax(gr)
print('img range',lo,hi)

# Stretches on whole image -- operates on RGB values, rather than intensity
# Applied to the linear stretch, linear occurred per filter on reading in

# square root start
#img /= hi #if overshooting - deprecated by screen algorithm
#img = img**.5  #square root


#log start
# img = np.log(1e-6+img/lo) #log
#lo,hi = np.amin(img),np.amax(img) #log rescale to max = 1.0
#print('img range',lo,hi)
#img /= hi  #if overshooting - deprecated by screen algorithm 
            # however changes colour if not used.
#log end

#img = np.log(1e-6+img) #run without "gr" gives different colours

# Display image
pl.imshow(img, origin='lower', interpolation='nearest')
#pl.xlim((0,127))
#pl.ylim((127,0))
pl.show()





