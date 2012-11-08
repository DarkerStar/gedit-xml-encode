dnl This file is free software: you can redistribute it and/or modify
dnl it under the terms of the GNU General Public License as published by
dnl the Free Software Foundation, either version 3 of the License, or
dnl (at your option) any later version.
dnl 
dnl This file is distributed in the hope that it will be useful,
dnl but WITHOUT ANY WARRANTY; without even the implied warranty of
dnl MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
dnl GNU General Public License for more details.
dnl 
dnl You should have received a copy of the GNU General Public License
dnl along with this file.  If not, see <http://www.gnu.org/licenses/>.

dnl GEDIT_PROG
dnl 
dnl Macro to setup variables related to gedit and gedit plugins.
dnl 
dnl Configure arguments:
dnl   
dnl   --enable-local-install[=x]   If <x> is "yes", sets up $geditplugindir and
dnl                                $localedir for plugins installed in the user
dnl                                home directory.
dnl   
dnl   --disable-local-install      Equivalent to "--enable-local-install=no"
dnl 
dnl Variables:
dnl   
dnl   geditplugindir     Directory to install gedit plugins into. For regular
dnl                      installs, this defaults to:
dnl                        ${libdir}/gedit/plugins
dnl                      For local installs, this defaults to:
dnl                        ${HOME}/.local/share/gedit/plugins
dnl 
dnl WARNING:
dnl   
dnl   Because intltool does not honour $localedir, (see intltool bug #1030541
dnl   <https://bugs.launchpad.net/intltool/+bug/1030541>) some trickery is
dnl   necessary to get translations to install in the user home directory during
dnl   local installs.
dnl   
dnl   That trickery involves setting the $prefix to "$HOME/.local". So you
dnl   cannot override the prefix while doing a local install.

AC_DEFUN([GEDIT_PROG],
[
# Add new configure arguments to allow the user to select a local install
AC_ARG_ENABLE([local-install],
  [AS_HELP_STRING([--enable-local-install],
    [install plugin in user home directory for private use @<:@default=no@:>@])],
  [enable_local_install="${enableval}"],
  [enable_local_install="no"])
    
# Set directory variables depending on whether the user has selected a local
# install or not.
# 
# Affected variables are $geditplugindir and possibly $prefix.
# 
# If the plugin is being installed normally (globally), only $geditplugindir
# is set. It defaults to:
#   ${libdir}/gedit/plugins
# 
# If the plugin is being installed locally, $geditplugindir gets set to:
#   ${HOME}/.local/share/gedit/plugins
# However, $prefix also gets set. This is necessary to work around a bug in
# intltool, where intltool does not honour $localedir (bug #1030541
# <https://bugs.launchpad.net/intltool/+bug/1030541>). $prefix gets set to:
#   ${HOME}/.local
AC_MSG_CHECKING([install plugin in user home directory for private use])
AS_IF([test "x${enable_local_install}" = "xyes"],
  [AC_MSG_RESULT([yes])
   geditpluginexecdir=${HOME}/.local/share/gedit/plugins
   geditplugindatadir=${HOME}/.local/share/gedit/plugins
   prefix=${HOME}/.local
  ],
  [AC_MSG_RESULT([no])
   geditpluginexecdir=${libdir}/gedit/plugins
   geditplugindatadir=${datadir}/gedit/plugins
  ])
    
# Set up gedit directory variables
AC_SUBST(geditpluginexecdir)
AC_SUBST(geditplugindatadir)
    
# Notify the user during configure what the variables are
AC_MSG_CHECKING([gedit plugin directory])
AC_MSG_RESULT([${geditpluginexecdir}])
AC_MSG_CHECKING([gedit plugin data directory])
AC_MSG_RESULT([${geditplugindatadir}])
])
