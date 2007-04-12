%define	name	marlin
%define version 0.9
%define	major	0
%define	libname	%mklibname marlin %major

%define	Summary	A GNOME sample editor
%define	title	Marlin
%define	section	Multimedia/Sound 

Summary: 	%Summary
Name: 		%name
Version: 	%version
Release: 	%mkrel 3
License: 	GPL
Group: 		Graphical desktop/GNOME
URL: 		http://marlin.sourceforge.net/

Source: 	http://prdownloads.sourceforge.net/marlin/marlin-%{version}.tar.bz2
Source1:	%name-16.png
Source2:	%name-32.png
Source3:	%name.png

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot


BuildRequires:	gettext
BuildRequires:	scrollkeeper
BuildRequires:	libgnomeui2-devel
BuildRequires:	libgstreamer-plugins-devel
BuildRequires:	libnautilus-burn-devel >= 2.11.5
BuildRequires:	e2fsprogs-devel
BuildRequires:	libmusicbrainz-devel >= 2.1.1
BuildRequires:	perl-XML-Parser

%description 
Marlin is a sample editor for Gnome 2. It uses GStreamer for 
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

%description
Marlin library file.

%package -n	%libname
Summary: 	Marlin library file
Group: 		Sound
Provides:	libmarlin = %version-%release

%description -n	%libname
Marlin devel file.
    
%description
Marlin devel file.

%package -n	%libname-devel
Summary: 	Marlin devel file
Requires:	%libname = %version
Group: 		Sound
Provides: 	libmarlin-devel = %version-%release

%description -n	%libname-devel
Marlin devel file.

%prep
%setup -q

%build
%configure2_5x

%make WARN_CFLAGS=""

%install
rm -rf %buildroot
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 
%{makeinstall_std}

%find_lang %name --with-gnome

# menu
mkdir -p %buildroot%{_menudir}
cat > %buildroot%{_menudir}/%{name} << EOF
?package(%name): \
command="%{_bindir}/%{name}" \
needs="x11" \
icon="%{name}.png" \
section="%{section}" \
title="%{title}" \
startup_notify="true" \
longtitle="%{Summary}"
EOF

# icon
mkdir -p %buildroot/{%_liconsdir,%_iconsdir,%_miconsdir}
#install -m 644 src/pixmaps/%name.png %buildroot/%_datadir/pixmaps/%name.png
install -m644 %SOURCE1 -D %buildroot%{_miconsdir}/%{name}.png
install -m644 %SOURCE2 -D %buildroot%{_liconsdir}/%{name}.png
install -m644 %SOURCE3 -D %buildroot%{_iconsdir}/%{name}.png

%post
%update_menus
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/%{name}.schemas > /dev/null
if [ -x %{_bindir}/scrollkeeper-update ]; then %{_bindir}/scrollkeeper-update -q; fi


%preun
if [ $1 -eq 0 ]; then
  GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/%{name}.schemas > /dev/null
fi


%post -n %{libname} -p /sbin/ldconfig

%postun
%clean_menus
if [ -x %{_bindir}/scrollkeeper-update ]; then %{_bindir}/scrollkeeper-update -q; fi

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %buildroot

%files -n %name -f %name.lang
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog README TODO
%{_sysconfdir}/gconf/schemas/%{name}.schemas
%{_bindir}/*
%dir %{_datadir}/marlin/
%dir %{_datadir}/marlin/ui/
%{_datadir}/marlin/ui/*.xml
%dir %{_datadir}/omf/marlin/
%{_datadir}/omf/marlin/marlin-C.omf
%{_datadir}/pixmaps/*
%{_datadir}/applications/%{name}.desktop
%_menudir/%name
%_liconsdir/%name.png
%_miconsdir/%name.png
%_iconsdir/%name.png

%files -n %libname
%defattr(-,root,root,-)
%{_libdir}/lib*.so.*

%files -n %libname-devel
%defattr(-,root,root,-)
%dir %{_includedir}/libmarlin
%{_includedir}/libmarlin/*
%{_libdir}/*a
%{_libdir}/*.so

