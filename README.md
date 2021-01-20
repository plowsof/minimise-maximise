# minimise-maximise
When playing SoF in fullscreen at lower resolutions e.g. 640x480 - you must now navigate around your desktop at this resolution unless you quit SoF.exe. 

With this script running in the background, any time you leave SoF by alt+tab or pressing the windows key it will minimise and resize your desktop to its default value.

**Install**
- extract the git .zip to your SoF's user folder 
- Requires an SoFplus client from sof1.megalag.org/sofplus

**Usage**
- sof-mini-maxi.exe must be in your user/ folder
- when you start the exe, just make sure the desktop resolution is correct
- to be safe, start sof-mini-maxi.exe first, then SoF

**Known bugs/issues**
- for now the exe starts with a terminal box spamming debug strings (normal)
- when you return to SoF you'll hear bugged sound e.g. an infinite loop playing. Type 'snd_restart' in console to fix this
