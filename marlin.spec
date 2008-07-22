%define	name	marlin
%define version 0.12
%define schemas	%{name}

%define	major		0
%define	libname		%mklibname %name %major
%define develname	%mklibname %name -d

Summary: 	A GNOME sample editor
Name: 		%name
Version: 	%version
Release: 	%mkrel 4
License: 	GPLv2
Group: 		Graphical desktop/GNOME
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL: 		http://marlin.sourceforge.net/

Source0: 	http://folks.o-hand.com/iain/marlin-releases/%{name}-%{version}.tar.bz2
Source1:	%name-16.png
Source2:	%name-32.png
Source3:	%name.png
# From GNOME bug #475905: updates marlin to newer libunique API.
# tested for libunique 0.9.3, may need updating for future versions.
# by Emmanuele Bassi. - AdamW 2007/09
Patch0:		marlin-0.12-unique.patch
# Fixes some errors in the .schemas file - AdamW 2007/09
Patch1:		marlin-0.12-schemas.patch


BuildRequires:	gettext
BuildRequires:	scrollkeeper
BuildRequires:	intltool
BuildRequires:	libgnomeui2-devel
BuildRequires:	libgstreamer0.10-plugins-base-devel
BuildRequires:	libnautilus-burn-devel >= 2.11.5
BuildRequires:	e2fsprogs-devel
BuildRequires:	libmusicbrainz-devel >= 2.1.1
BuildRequires:	perl-XML-Parser
BuildRequires:	gnome-common
BuildRequires:	unique-devel
BuildRequires:	soundtouch-devel
BuildRequires:	libjack-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	desktop-file-utils

%description 
Marlin is a sample editor for GNOME. It uses GStreamer for 
file operations and for recording and playback, meaning it 
can handle a great number of formats and work with most sound 
systems.

    * Can load from a large number of media formats (mp3, ogg, mpg, avi...)
    * Can save to many formats (mp3, wav, ogg...)
    * Can handle large files with no problems
    * Handles cut, copy, paste, and mix operations
    * Fully Gnome 2 HIG compliant
    * Can record from a variety of sources (ALSA, OSS, esd, MAS, arts)
    * Playback
    * Can extract audio from CDs

%package -n	%libname
Summary: 	Shared libraries for Marlin
Group: 		Sound
Provides:	libmarlin = %version-%release

%description -n	%libname
Marlin is a sample editor for GNOME. It uses GStreamer for 
file operations and for recording and playback, meaning it 
can handle a great number of formats and work with most sound 
systems.

%package -n	%develname
Summary: 	Development libraries and headers for Marlin
Requires:	%libname = %version
Group: 		Sound
Provides: 	%name-devel = %version-%release
Obsoletes:	%mklibname %name 0 -d

%description -n	%develname
Marlin is a sample editor for GNOME. It uses GStreamer for 
file operations and for recording and playback, meaning it 
can handle a great number of formats and work with most sound 
systems.

%prep
%setup -q
%patch0 -p0 -b .unique
%patch1 -p1 -b .schemas
perl -pi -e 's,marlin/marlin-icon.png,%{name},g' marlin.desktop.in

%build
autoreconf
# the tarball has old versions of the intltool scripts, which don't
# work any more. this is a somewhat hacky way to make it use packaged
# ones instead. there must be a cleaner way to do it, but I can't
# figure it out: the lines are in aclocal.m4, and if you generate
# aclocal.m4 with 'aclocal' they're in the generated copy, but I can't
# figure out where the hell they come *from*. the lines don't appear
# in any other file in the tarball. autoreconf runs aclocal, so we
# have to do this substitution *after* autoreconf, and then do
# autoconf again to get the changes into the 'configure' script.
# - AdamW 2007/09
perl -pi -e 's,\$\(top_builddir\)/intltool,%{_bindir}/intltool,g' aclocal.m4
autoconf

%configure2_5x --disable-schemas-install
%make WARN_CFLAGS=""

%install
rm -rf %buildroot
%{makeinstall_std}

# menu entry
desktop-file-install --vendor="" \
  --add-category="GTK" \
  --add-category="GNOME" \
  --add-category="Audio" \
  --add-category="AudioVideoEditing" \
  --remove-category="Application" \
  --remove-category="Multimedia" \
  --remove-key="Encoding" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

%find_lang %name --with-gnome

# icon
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
#install -m 644 src/pixmaps/%name.png %buildroot/%_datadir/pixmaps/%name.png
install -m644 %SOURCE1 -D %buildroot%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m644 %SOURCE2 -D %buildroot%{_iconsdir}/hicolor/48x48/apps/%{name}.png
install -m644 %SOURCE3 -D %buildroot%{_iconsdir}/hicolor/32x32/apps/%{name}.png

%if %mdkversion < 200900
%post
%update_menus
%post_install_gconf_schemas %{schemas}
%update_scrollkeeper
%update_icon_cache hicolor
%endif

%preun
%preun_uninstall_gconf_schemas %{schemas}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_scrollkeeper
%clean_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %buildroot

%files -n %name -f %name.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog README TODO
%{_sysconfdir}/gconf/schemas/%{name}.schemas
%{_bindir}/*
%{_libdir}/%{name}-%{version}
%{_datadir}/%{name}
%{_datadir}/omf/%{name}
%{_datadir}/pixmaps/*
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

%files -n %libname
%defattr(-,root,root,-)
%{_libdir}/lib*.so.%{major}*

%files -n %develname
%defattr(-,root,root,-)
%dir %{_includedir}/libmarlin
%{_includedir}/libmarlin/*
%{_libdir}/*a
%{_libdir}/*.so

