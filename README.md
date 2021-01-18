# minimise-maximise
When playing SoF in fullscreen at lower resolutions e.g. 640x480 - you must now navigate around your desktop at this resolution unless you quit SoF.exe. 

With this script running in the background, any time you leave SoF by alt+tab or pressing the windows key it will minimise and resize your desktop to its default value.

Major bug where pressing LALT key will lag the game (i the desktop is registering the LALT button press) as if SoF isnt really fullscreen. ~seems to be fixed by messing around with minimizing / maximizing SoF. This 'fix' somehow needs a 'snd_restart' to sounds looping after entering SoF(??)

An 'snd_restart' on maximise would fix an existing bug anyway where sounds while minimised all play at once (also some effects)
