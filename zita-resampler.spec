Summary:	C++ library for sample rate conversion of audio signals
Name:		zita-resampler
Version:	1.3.0
Release:	1
License:	GPL v3+
Group:		Libraries
Source0:	http://kokkinizita.linuxaudio.org/linuxaudio/downloads/%{name}-%{version}.tar.bz2
# Source0-md5:	74c12e2280008f63ac9f2670fe4cf79b
URL:		http://kokkinizita.linuxaudio.org/linuxaudio/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Zita-resampler is a C++ library for sample rate conversion of audio
signals.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package apps
Summary:	Example applications using the %{name} library
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description apps
Example applications using the %{name} library.

%prep
%setup -q

%build
CXXFLAGS="%{rpmcxxflags}" \
CPPFLAGS="%{rpmcppflags}" \
LDFLAGS="%{rpmldflags}" \
%{__make} -C libs

ln -s "$(basename libs/libzita-resampler.so.*.*.*)" libs/libzita-resampler.so

CXXFLAGS="%{rpmcxxflags}" \
CPPFLAGS="-I../libs %{rpmcppflags}" \
LDFLAGS="-L../libs %{rpmldflags}" \
%{__make} -C apps

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}}

cp -p libs/lib%{name}.so.1.* $RPM_BUILD_ROOT%{_libdir}
/sbin/ldconfig -nN $RPM_BUILD_ROOT%{_libdir}
ln -s "$(basename libs/lib%{name}.so.1.*)" $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so
cp -R libs/%{name} $RPM_BUILD_ROOT%{_includedir}

%{__make} -C apps install \
	PREFIX="%{_prefix}" \
	DESTDIR="$RPM_BUILD_ROOT"

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/lib%{name}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/lib%{name}.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib%{name}.so
%{_includedir}/%{name}

%files apps
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*.1*
