%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/rolling/.*$
%global __requires_exclude_from ^/opt/ros/rolling/.*$

Name:           ros-rolling-spdlog-vendor
Version:        1.4.4
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS spdlog_vendor package

License:        Apache License 2.0 and MIT
URL:            https://github.com/gabime/spdlog
Source0:        %{name}-%{version}.tar.gz

Requires:       %{name}-runtime%{?_isa?} = %{version}-%{release}
Requires:       spdlog-devel
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}

%description
Wrapper around spdlog, providing nothing but a dependency on spdlog, on some
systems. On others, it provides an ExternalProject build of spdlog.

%package runtime
Summary:        Runtime-only files for spdlog_vendor package
Requires:       spdlog-devel
Requires:       ros-rolling-ros-workspace-runtime
BuildRequires:  ros-rolling-ament-cmake-devel
BuildRequires:  spdlog-devel
BuildRequires:  ros-rolling-ros-workspace-devel

%if 0%{?with_tests}
BuildRequires:  ros-rolling-ament-lint-auto-devel
BuildRequires:  ros-rolling-ament-lint-common-devel
%endif

%description runtime
Runtime-only files for spdlog_vendor package

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/rolling" \
    -DAMENT_PREFIX_PATH="/opt/ros/rolling" \
    -DCMAKE_PREFIX_PATH="/opt/ros/rolling" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

for f in \
    /opt/ros/rolling/include/ \
    /opt/ros/rolling/share/ament_index/resource_index/packages/ \
    /opt/ros/rolling/share/spdlog_vendor/cmake/ \
    /opt/ros/rolling/share/spdlog_vendor/package.dsv \
    /opt/ros/rolling/share/spdlog_vendor/package.xml \
; do
    if [ -e %{buildroot}$f ]; then echo $f; fi
done > devel_files

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files -f devel_files

%files runtime
/opt/ros/rolling
%exclude /opt/ros/rolling/include/
%exclude /opt/ros/rolling/share/ament_index/resource_index/packages/
%exclude /opt/ros/rolling/share/spdlog_vendor/cmake
%exclude /opt/ros/rolling/share/spdlog_vendor/package.dsv
%exclude /opt/ros/rolling/share/spdlog_vendor/package.xml

%changelog
* Tue Apr 11 2023 Dharini Dutia <dharini@openrobotics.org> - 1.4.4-1
- Autogenerated by Bloom

* Wed Mar 22 2023 Dharini Dutia <dharini@openrobotics.org> - 1.4.3-2
- Autogenerated by Bloom

