REQUIREMENTS: 
-------------------------------------------------------------------------------
Before running make sure you have PyGame installed first:

  pip3 install pygame

You need to be on Python 3.7 or higher as I am using time.time_ns() which was introduced in Python version 3.7. PyGame's clock.tick() causes frame rate jerkyness, which is why I'm not using it.


ABOUT: 
-------------------------------------------------------------------------------
Bouncy Balloon is a small game I made with my youngest daughter that has no external dependencies outside of needing PyGame.

The entire program is less than 140 lines. It is not the smallest game ever in terms of code size, but it is pretty small (by design).

Besides being a fun little game, the point is to help young programers understand some of the basic components of game design in a readable form.

Now go learn C you script kiddies!

INSTRUCTIONS: 
-------------------------------------------------------------------------------
  > Hit Space Bar to bounce up.
  > Avoid enemy baloons.
  > Fly Bouncy Balloon through the gaps to score points. 
  > Press escape to end the game or simply close the window.
