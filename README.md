gedit XML encode plugin
=======================



**gedit XML encode plugin** is a plugin for
[gedit](http://projects.gnome.org/gedit/) that adds new menu commands to convert
XML special characters (“&”, “<”, “>”, “'” and “"”) in a section, or the whole
document, into XML character entities.



Latest version
--------------

The latest release can be downloaded from the
[github project downloads page](https://github.com/DarkerStar/gedit-xml-encode/downloads).



Documentation
-------------

Once the plugin is installed, it may be activated. Select Edit->Preferences from
the main menu to open the preferences dialog. In the Plugins tab of the
preferences dialog, look for the “XML Encode” plugin. Select it to activate it,
and it should start working right away.

Once the plugin is active, there will be a new item in the gedit Edit menu,
called “XML Encode” whenever there is a document open in gedit. This item wil
lead to a submenu with two options: “Document” and “Selection”.

Both options do the same thing, but the first works on the whole document, while
the second only applies to the current selection (if there is no selection,
nothing is done). Depending on the option, all of the special XML characters in
the document or selection will be converted to XML entity references.

The special XML characters are “&”, “<”, “>”, “'” and “"”. These characters have
special meaning in XML syntax, and there are several places they cannot be used
in text data without causing problems. By converting them to entity references -
“&amp;”, “&lt;”, “&gt;”, “&apos;” and “&quot;” respectively - these problems can
be avoided.

This plugin does that conversion automatically, so that the selection or
document converted can be embedded as text data in an XML file without problems.
This is especially useful for embedding source code in (X)HTML files.



Installation
------------

Normally, the package may be built and installed with the following sequence of
commands:

*   `./configure`
    
*   `make`
    
*   `make install`

If installation requires root privileges, then it may necessary to change the
last command to “`sudo make install`”, or to first request root privileges with
“`su`”, then run “`make install`”.

This sequence of commands will normally build the plugin and install it in the
default location for global gedit plugins. All that should be necessary then is
to restart gedit, and the plugin should be available in the plugin manager.

An alternative to installing the plugin globally is to install it locally for
use by only a single user. This installs the plugin and all of its data files
into a hidden directory in the user's home. Installing this way means there is
no need for root privileges, but it also means that the plugin is only available
to the user it was installed for. To install the plugin locally, use the
configure script with the “`--enable-local-install`” option. For example:

*   `./configure --enable-local-install`

After that, the regular “`make`” and “`make install`” commands should build the
plugin and install it in the desired location, whether that means locally in
the user's home, or globally.

In some cases, it may be required to run the “bootstrap” script first. This
should normally only be run by developers to prepare the project for the end
user.

For more details, please see the file called “INSTALL”.



Development information
-----------------------

__Why isn't this part of the gedit-plugins project?__

I doubt they would be interested in such a trivial plugin. More likely than not,
there's already something in the standard gedit UI, or the default plugins, or
in the gedit-plugins, that does this. I just haven't been able to find it, and
this took all of two afternoons to put together, so... yeah.

But if there is nothing like it in the existing plugins or the standard gedit
functions, and if enough people think this is worth including, then I'd be happy
to port it over.

__Why Autotools?__

gedit itself uses Autotools, as does the gedit-plugins project.

__Why Python?__

The plugin's functions are so simple, there was simply no need for the
power of C++, or the headache of C.

__Known issues and potential improvements__
    
*   A message should be displayed in the statusbar giving the number of entities
    converted, similar to how the normal Replace function works. The reason this
    isn't working yet is because of a missing API function.
    
*   XML _de_code?
    
*   Currently the characters and entities are hardcoded in the source. Instead
    of that, they could be stored in the gedit configuration file, so that users
    have the option of changing the conversion behaviour. (For example, if they
    don't want “'” converted to “&apos;”.)
    
*   Especially if the above is implemented, perhaps the conversion options could
    be set in a configure dialog.
    
*   A help dialog could be implemented, even if all it does is give more info
    about the plugin.
    
*   Rather than _just_ an XML entity encoder, perhaps a more generalized
    transformation plugin might be handy, with XML encoding being just one of a
    number of specialized transformations. But what other transformations might
    there be?



Licensing
---------

Please see the file called “COPYING”.



Contacts
--------

For contact information, check out the
[github project page](https://github.com/DarkerStar/gedit-xml-encode).
