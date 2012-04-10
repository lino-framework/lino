The `using` directory
=====================

If you run several Lino sites on a single server and want 
to be able to easily switch Lino versions individually per site, 
then you need a `using` directory

The `using` directory is a subdirectory of your project 
directory, containing a symbolic link to the root of 
Lino's source. 
There are two places who need this information:

- `media/lino` links to `using/lino/media`
- `settings.py` adds `using/lino` (and not some hard-coded directory) 
  to the system path

