# TODO: allow build without network (npm install)
#
# Condional build:
%bcond_without	tests	# unit tests
%bcond_with	npm	# bootstrap with npm

Summary:	A documentation tool micro-framework
Summary(pl.UTF-8):	Mikroszkielet narzędzia do tworzenia dokumentacji
Name:		hotdoc
Version:	0.13.3
Release:	5
License:	LGPL v2.1+
Group:		Development/Tools
#Source0Download: https://github.com/hotdoc/hotdoc/releases
Source0:	https://github.com/hotdoc/hotdoc/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	9ddff982abb44a31c9c03b7ea00fdaad
Source1:	https://github.com/MathieuDuponchelle/cmark/archive/db73e39/cmark-db73e39.tar.gz
# Source1-md5:	8b7647adcf770ae012e8594fba2a7916
Source2:	https://github.com/PrismJS/prism/archive/eccf09f/prism-eccf09f.tar.gz
# Source2-md5:	bf45a06cebc01ef5f36b4521bf97b410
Source3:	https://github.com/hotdoc/hotdoc_bootstrap_theme/archive/89e04ee/hotdoc_bootstrap_theme-89e04ee.tar.gz
# Source3-md5:	504d2876b68042dbbbb45bcd99dc2079
# compressed hotdoc/hotdoc_bootstrap_theme/dist after bootstrapping npm with network (node_modules not needed?)
Source4:	hotdoc-%{version}-hotdoc_bootstrap_theme-dist.tar.xz
# Source4-md5:	d7907f232dbdc910457a20d445609165
Patch0:		%{name}-setup.patch
Patch1:		clang_libdir.patch
URL:		https://hotdoc.github.io/
BuildRequires:	cmake >= 2.8.9
BuildRequires:	flex
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	json-glib-devel
BuildRequires:	libxml2-devel >= 2.0
%{?with_npm:BuildRequires:	npm}
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3.5
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
BuildRequires:	python3-wheel
# runtime dependencies, but required at build time to avoid fetching wheels from network
BuildRequires:	python3-PyYAML >= 5.1
BuildRequires:	python3-appdirs
BuildRequires:	python3-cchardet
BuildRequires:	python3-dbus-deviation >= 0.4.0
BuildRequires:	python3-lxml
BuildRequires:	python3-networkx >= 2.5
BuildRequires:	python3-pkgconfig
BuildRequires:	python3-schema
BuildRequires:	python3-toposort >= 1.4
BuildRequires:	python3-wheezy.template
# libclang.so dlopen in c extension
Requires:	clang-devel
# llvm-config in c extension
Requires:	llvm-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Hotdoc is a documentation micro-framework. It provides an interface
for extensions to plug upon, along with some base objects (formatters,
...).

%description -l pl.UTF-8
Hotdoc to mikroszkielet do tworzenia dokumentacji. Udostępnia
interfejs rozszerzeń, a także trochę podstawowych obiektów (formaterów
itp.).

%prep
%setup -q -a1 -a2 -a3
%patch0 -p1
%patch1 -p1

%{__mv} cmark-*/* cmark
%{__mv} prism-*/* hotdoc/extensions/syntax_highlighting/prism
%{__mv} hotdoc_bootstrap_theme-*/* hotdoc/hotdoc_bootstrap_theme

%if %{without npm}
%{__tar} xf %{SOURCE4}
%endif

%{__sed} -i -e '1s, /usr/bin/env sh,/bin/sh,' hotdoc/extensions/gi/transition_scripts/translate_sections.sh

%build
%py3_build %{?with_tests:test}

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/hotdoc/{tests,core/tests,parsers/tests,utils/tests}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/hotdoc
%attr(755,root,root) %{_bindir}/hotdoc_dep_printer
%{py3_sitedir}/hotdoc
%{py3_sitedir}/hotdoc-%{version}-py*.egg-info
