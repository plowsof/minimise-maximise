# minimise-maximise
When playing SoF in fullscreen at lower resolutions e.g. 640x480 - you must now navigate around your desktop at this resolution unless you quit SoF.exe. 

With this script running in the background, any time you leave SoF by alt+tab or pressing the windows key it will minimise and resize your desktop to its default value.

Advantage of using an SoFplus script are that you can change gl_mode on the fly with this and it will adjust the desktop correctly

**Install**
- extract the git .zip to your SoF's user folder 
- Requires an SoFplus client from sof1.megalag.org/sofplus

**Usage**
- sof-mini-maxi.exe must be in your user/ folder
- when you start the exe, just make sure the desktop resolution is correct
- to be safe, start sof-mini-maxi.exe first, then SoF

**Changes**
- Uing the python injector, sound is disabled when SoF is minimised and enabled on maximise to prevent the sound glitch

**Known bugs/issues**
- for now the exe starts with a terminal box spamming debug strings (normal)
- Weird window behaviour on rare occasions


