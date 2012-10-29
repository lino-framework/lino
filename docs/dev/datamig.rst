Designing data migrations for your application
----------------------------------------------

The principle is easy but not yet well documented: 
since Python dumps are Python scripts, we can do everything with them.


A magical `before_dumpy_save` attribute may contain custom 
code to apply inside the try...except block. 
If that code fails, the deserializer will simply 
defer the save operation and try it again.
    
