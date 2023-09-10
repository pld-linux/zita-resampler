#
# Conditional build:
%bcond_with	sse2	# SSE2 support

%ifarch %{x8664} x32
%define	with_sse2	1
%endif
Summary:	C++ library for sample rate conversion of audio signals
Summary(pl.UTF-8):	Biblioteka C++ do konwersji szybkości próbkowania sygnałów dźwiękowych
Name:		zita-resampler
Version:	1.11.2
Release:	1
License:	GPL v3+
Group:		Libraries
Source0:	http://kokkinizita.linuxaudio.org/linuxaudio/downloads/%{name}-%{version}.tar.xz
# Source0-md5:	da0373a02f0d1ba0a15a1fd270a177cd
URL:		http://kokkinizita.linuxaudio.org/linuxaudio/
BuildRequires:	libsndfile-devel
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Zita-resampler is a C++ library for sample rate conversion of audio
signals.

%description -l pl.UTF-8
Zita-resampler to biblioteka C++ do konwersji szybkości próbkowania
sygnałów dźwiękowych.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package apps
Summary:	Example applications using the %{name} library
Summary(pl.UTF-8):	Przykładowe aplikacje wykorzystujące bibliotekę %{name}
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description apps
Example applications using the %{name} library.

%description apps -l pl.UTF-8
Przykładowe aplikacje wykorzystujące bibliotekę %{name}.

%prep
%setup -q

%if %{without sse2}
%{__sed} -i -e '/-DENABLE_SSE2/d' source/Makefile
%endif

%build
CPPFLAGS="%{rpmcppflags}" \
LDFLAGS="%{rpmldflags}" \
%{__make} -C source \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags} -fPIC -Wall -ffast-math%{?with_sse2: -msse2}"

ln -s "$(basename source/libzita-resampler.so.*.*.*)" source/libzita-resampler.so

CPPFLAGS="-I../source %{rpmcppflags}" \
LDFLAGS="-L../source %{rpmldflags}" \
%{__make} -C apps \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags} -Wall -ffast-math"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir},%{_mandir}/man1}

cp -p source/lib%{name}.so.1.* $RPM_BUILD_ROOT%{_libdir}
/sbin/ldconfig -nN $RPM_BUILD_ROOT%{_libdir}
ln -s "$(basename $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so.1.*)" $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so
cp -pr source/%{name} $RPM_BUILD_ROOT%{_includedir}

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
%attr(755,root,root) %{_libdir}/libzita-resampler.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzita-resampler.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzita-resampler.so
%{_includedir}/zita-resampler

%files apps
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/zresample
%attr(755,root,root) %{_bindir}/zretune
%{_mandir}/man1/zresample.1*
%{_mandir}/man1/zretune.1*
