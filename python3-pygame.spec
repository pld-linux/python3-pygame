#
# Conditional build:
%bcond_without	apidocs	# Sphinx documentation

%define		module	pygame

Summary:	Python modules designed for writing games
Summary(pl.UTF-8):	Moduły Pythona dla piszących gry
Name:		python3-%{module}
Version:	2.6.1
Release:	1
License:	LGPL v2.1+
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/p/pygame/pygame-%{version}.tar.gz
# Source0-md5:	cb6bf42a449b0bb1f53c534bcbcc220c
Patch2:		x32.patch
URL:		https://www.pygame.org/
BuildRequires:	SDL2-devel >= 2.0
BuildRequires:	SDL2_image-devel >= 2.0
BuildRequires:	SDL2_mixer-devel >= 2.0
BuildRequires:	SDL_ttf-devel >= 2.0
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	portmidi-devel >= 217
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-numpy-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with apidocs}
BuildRequires:	sphinx-pdg-3
%endif
BuildRequires:	xorg-lib-libX11-devel
Requires:	python3-modules >= 1:3.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pygame is a set of Python modules designed for writing games. It is
written on top of the excellent SDL library. This allows you to create
fully featured games and multimedia programs in the python language.
The package is highly portable, with games running on Windows, NT4,
MacOS, OSX, BeOS, FreeBSD, IRIX, and Linux.

%description -l pl.UTF-8
Pygame jest zbiorem modułów Pythona zaprojektowanych do pisania gier.
Moduły te zostały napisane na bazie wspaniałej biblioteki SDL. Dzięki
temu możliwe jest tworzenie bogatych w multimedia gier w języku
Python.

%package devel
Summary:	C header files for pygame modules
Summary(pl.UTF-8):	Pliki nagłówkowe języka C modułów pygame
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-devel >= 1:2.7
BuildArch:	noarch

%description devel
C header files for pygame modules.

%description devel -l pl.UTF-8
Pliki nagłówkowe języka C modułów pygame.

%package apidocs
Summary:	API documentation for Python pygame modules
Summary(pl.UTF-8):	Dokumentacja API modułów Pythona pygame
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python pygame modules.

%description apidocs -l pl.UTF-8
Dokumentacja API modułów Pythona pygame.

%package examples
Summary:	Examples for Python pygame modules
Summary(pl.UTF-8):	Przykłady do modułów Pythona pygame
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description examples
Examples for Python pygame modules.

%description examples -l pl.UTF-8
Przykłady do modułów Pythona pygame.

%prep
%setup -q -n %{module}-%{version}
%patch2 -p1

%build
export PORTMIDI_INC_PORTTIME=1
CFLAGS="%{rpmcflags} -DPG_COMPILE_SSE4_2=0"
%py3_build

%if %{with apidocs}
sphinx-build-3 -b html docs/reST docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%py3_install

cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/{docs,examples,tests}
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/pygame.ico
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/pygame_icon.*
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/pygame_icon_mac.*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.ttf
%attr(755,root,root) %{py3_sitedir}/%{module}/*.so
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/*.pyi
%{py3_sitedir}/%{module}/py.typed
%{py3_sitedir}/%{module}/__pycache__
%dir %{py3_sitedir}/%{module}/__pyinstaller
%{py3_sitedir}/%{module}/__pyinstaller/*.py
%{py3_sitedir}/%{module}/__pyinstaller/__pycache__
%dir %{py3_sitedir}/%{module}/_sdl2
%attr(755,root,root) %{py3_sitedir}/%{module}/_sdl2/*.so
%{py3_sitedir}/%{module}/_sdl2/*.py
%{py3_sitedir}/%{module}/_sdl2/*.pyi
%{py3_sitedir}/%{module}/_sdl2/__pycache__
%dir %{py3_sitedir}/%{module}/threads
%{py3_sitedir}/%{module}/threads/*.py
%{py3_sitedir}/%{module}/threads/__pycache__
%{py3_sitedir}/pygame-%{version}-py*.egg-info

%files devel
%defattr(644,root,root,755)
%{py3_incdir}/%{module}

%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_static,c_api,ref,tut,*.html,*.js}

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
