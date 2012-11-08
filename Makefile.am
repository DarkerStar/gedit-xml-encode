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

## Tell automake where to find extra m4 macros
ACLOCAL_AMFLAGS = -I m4 --install

## Tell automake about the subdirectories to look into
SUBDIRS = src po

## Take care of the markdown version of README (which is just README with a
## .md extension)
README.md: README
	@cp $< $@

EXTRA_DIST = README.md
