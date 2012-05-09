The `using` directory
=====================

If you run several Lino sites on a single server and want 
to be able to easily switch Lino versions individually per site, 
then you need to insert `lino` to the Python path in the
:xfile:`settings.py` of each Lino instance.

But we recommend to not simply add the hard-coded path because your 
decision (which Lino version that site should use) is needed 
at another place: the `/media/lino/` must link to the 
`/lino/media/` directory of the correct Lino version.

That's why we recommend to use a `using` directory.
The `using` directory is a subdirectory of your project 
directory that contains a symbolic link to the root of 
Lino's source tree.
There are two places who need this information:

- `media/lino` links to `using/lino/media`
- `settings.py` adds `using/lino` (and not some hard-coded directory) 
  to the system path

