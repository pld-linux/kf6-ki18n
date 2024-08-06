#
# Conditional build:
%bcond_with	tests		# build with tests
# TODO:
# find_lang needs to be updated (to handle pmap, pmapc, js files)
%define		kdeframever	6.4
%define		qtver		5.15.2
%define		kfname		ki18n

Summary:	KDE Gettext-based UI text internationalization
Name:		kf6-%{kfname}
Version:	6.4.0
Release:	2
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	8a5c6454de0eec7f7acfd8c150fb04d0
URL:		http://www.kde.org/
BuildRequires:	Qt6Concurrent-devel >= %{qtver}
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Qml-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	ninja
BuildRequires:	python3
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt6Core >= %{qtver}
Requires:	Qt6Qml >= %{qtver}
Requires:	kf6-dirs
#Obsoletes:	kf5-%{kfname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KI18n provides functionality for internationalizing user interface
text in applications, based on the GNU Gettext translation system. It
wraps the standard Gettext functionality, so that the programmers and
translators can use the familiar Gettext tools and workflows.

KI18n provides additional functionality as well, for both programmers
and translators, which can help to achieve a higher overall quality of
source and translated text. This includes argument capturing,
customizable markup, and translation scripting.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cmake >= 3.16
Requires:	gettext-tools
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

# not supported by glibc yet
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{kfname}6 --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}6.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF6I18n.so.6
%attr(755,root,root) %{_libdir}/libKF6I18n.so.*.*
%ghost %{_libdir}/libKF6I18nLocaleData.so.6
%attr(755,root,root) %{_libdir}/libKF6I18nLocaleData.so.*.*
%attr(755,root,root) %{qt6dir}/plugins/kf6/ktranscript.so
%{_datadir}/qlogging-categories6/ki18n.categories
%{_datadir}/qlogging-categories6/ki18n.renamecategories
%dir %{_libdir}/qt6/qml/org/kde/i18n
%dir %{_libdir}/qt6/qml/org/kde/i18n/localeData
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/i18n/localeData/libki18nlocaledataqmlplugin.so
%{_libdir}/qt6/qml/org/kde/i18n/localeData/qmldir
%{_libdir}/qt6/qml/org/kde/i18n/localeData/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/i18n/localeData/ki18nlocaledataqmlplugin.qmltypes

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KI18n
%{_includedir}/KF6/KI18nLocaleData
%{_libdir}/cmake/KF6I18n
%{_libdir}/libKF6I18n.so
%{_libdir}/libKF6I18nLocaleData.so
