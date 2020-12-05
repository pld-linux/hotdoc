#
# Condional build:
%bcond_without	tests	# unit tests

Summary:	A documentation tool micro-framework
Summary(pl.UTF-8):	Mikroszkielet narzędzia do tworzenia dokumentacji
Name:		hotdoc
Version:	0.10.0
Release:	0.1
License:	LGPL v2.1+
Group:		Development/Tools
#Source0Download: https://github.com/hotdoc/hotdoc/releases
Source0:	https://github.com/hotdoc/hotdoc/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	7ece3cc130cf220a057669753ea822d4
Source1:	https://github.com/MathieuDuponchelle/cmark/archive/7e5438a/cmark-7e5438a.tar.gz
# Source1-md5:	6d90c8153c0c16f467e46b4e0cbfca59
Source2:	https://github.com/PrismJS/prism/archive/eccf09f/prism-eccf09f.tar.gz
# Source2-md5:	bf45a06cebc01ef5f36b4521bf97b410
Source3:	https://github.com/hotdoc/hotdoc_bootstrap_theme/archive/da9b877/hotdoc_bootstrap_theme-da9b877.tar.gz
# Source3-md5:	e932cf06b825291f679af22235480987
Patch0:		%{name}-setup.patch
URL:		https://hotdoc.github.io/
BuildRequires:	cmake >= 2.8.9
BuildRequires:	flex
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	json-glib-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	npm
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3.4
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
#Requires:	python3-PyYAML >= 5.1, python3-lxml, python3-schema, python3-appdirs, python3-wheezy.template = 0.1.167, python3-toposort >= 1.4, python3-xdg >= 4.0.0, python3-dbus-deviation >= 0.4.0
#Requires:	python3-pkgconfig = 1.1.0, python3-cchardet, python3-networkx = 1.11
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

%{__mv} cmark-*/* cmark
%{__mv} prism-*/* hotdoc/extensions/syntax_highlighting/prism
%{__mv} hotdoc_bootstrap_theme-*/* hotdoc/hotdoc_bootstrap_theme

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
