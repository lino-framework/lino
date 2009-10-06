import sys

EMULATE=0
 
def aplayer( name, card, rate, tt ):
  import pymedia.muxer as muxer
  import pymedia.audio.acodec as acodec
  #import pymedia.audio.sound as sound
  import time
  dm= muxer.Demuxer( str.split( name, '.' )[ -1 ].lower() )
  
  f= open( name, 'rb' )
  #snd= resampler= dec= None
  dec=None
  s= f.read( 32000 )
  t= 0
  while len( s ):
    frames= dm.parse( s )
    if frames:
      for fr in frames:
        # Assume for now only audio streams
        if dec== None:
          print dm.getInfo(), dm.streams
          dec= acodec.Decoder( dm.streams[ fr[ 0 ] ] )
        
        r= dec.decode( fr[ 1 ] )
        if r:
            pass
            #print repr(r)
    
    s= f.read( 512 )

##   while snd.isPlaying():
##     time.sleep( .05 )

# ----------------------------------------------------------------------------------
# Play any compressed audio file with adjustable pitch
# http://pymedia.org/
if len( sys.argv )< 2 or len( sys.argv )> 5:
  print "Usage: aplayer <filename> [ sound_card_index, rate( 0..1- slower, 1..4 faster ) ]"
else:
  i= 0
  r= 1
  t= -1
  if len( sys.argv )> 2 :
    i= int( sys.argv[ 2 ] )
  if len( sys.argv )> 3 :
    r= float( sys.argv[ 3 ] )
  if len( sys.argv )> 4 :
    t= int( sys.argv[ 4 ] )
  aplayer( sys.argv[ 1 ], i, r, t ) 
