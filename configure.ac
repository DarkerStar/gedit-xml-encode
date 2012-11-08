################################################################################
#                                                                              #
# This file is part of the gedit XML encode plugin.                            #
#                                                                              #
# The gedit XML encode plugin is free software: you can redistribute it and/or #
# modify it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or (at your   #
# option) any later version.                                                   #
#                                                                              #
# The gedit XML encode plugin is distributed in the hope that it will be       #
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General    #
# Public License for more details.                                             #
#                                                                              #
# You should have received a copy of the GNU General Public License along with #
# the gedit XML encode plugin.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                              #
################################################################################

# Initialize autoconf ##########################################################
AC_PREREQ([2.69])

AC_INIT([gedit XML encode plugin], [0.1], [indi.in.the.wired@gmail.com], ,
        [https://github.com/DarkerStar/gedit-xml-encode])

AC_CONFIG_AUX_DIR([build-aux])
AC_CONFIG_MACRO_DIR([m4])

AC_CONFIG_SRCDIR([src/xml-encode.py])

AC_PREFIX_PROGRAM([gedit])

# Initialize automake and libtool ##############################################
AM_INIT_AUTOMAKE([-Wall -Werror])

# Set up program checks ########################################################
AM_PATH_PYTHON

GEDIT_PROG

# Set up gettext and translation stuff #########################################
IT_PROG_INTLTOOL([0.50.0])

GETTEXT_PACKAGE=$PACKAGE_TARNAME
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE, ["$GETTEXT_PACKAGE"], [Gettext domain])

# Output #######################################################################
AC_CONFIG_FILES([Makefile src/Makefile po/Makefile.in])
AC_OUTPUT
