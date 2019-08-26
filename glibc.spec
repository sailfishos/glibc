%define glibcsrcdir glibc-2.28
# Default: Always disable the benchtests.
%bcond_with benchtests

# Only some architectures have static PIE support.
%define pie_arches %{ix86} x86_64

Name: glibc

Summary: GNU C library shared libraries
Version: 2.28+git5
Release: 0
License: LGPLv2+ and LGPLv2+ with exceptions and GPLv2+
Group: System/Libraries
URL: http://www.gnu.org/software/libc/
Source0: glibc-2.28.tar.xz
Source1: build-locale-archive.c

Patch1: glibc-arm-alignment-fix.patch
Patch2: glibc-2.25-arm-runfast.patch
Patch4: glibc-2.25-elf-rtld.diff
Patch5: glibc-2.27-ldso-rpath-prefix-option.diff
Patch6: glibc-2.25-nsswitchconf-location.diff
Patch7: glibc-2.25-nscd-socket-location.diff
Patch8: glibc-2.25-ldso-nodefaultdirs-option.diff
Patch9: glibc-2.14-locarchive-fedora.patch
Patch10: eglibc-2.15-fix-neon-libdl.patch
Patch11: eglibc-2.19-shlib-make.patch
Patch12: glibc-2.27-bits.patch
Patch13: git-updates.diff

Provides: ldconfig
# The dynamic linker supports DT_GNU_HASH
Provides: rtld(GNU_HASH)
Requires: glibc-common = %{version}-%{release}

# This is a short term need until everything is rebuilt in armhf
%ifarch armv7hl armv7nhl armv7tnhl
Provides: ld-linux.so.3
Provides: ld-linux.so.3(GLIBC_2.4)
%endif

BuildRequires: xz tar
# Require libgcc in case some program calls pthread_cancel in its %%post
Requires(pre): libgcc
BuildRequires:  zlib-devel texinfo
BuildRequires: sed >= 3.95, libcap-devel, gettext
BuildRequires: gawk,  util-linux
# This gcc >= 3.2 is to ensure that __frame_state_for is exported by glibc
# will be compatible with egcs 1.x.y
BuildRequires: gcc >= 3.2
%define enablekernel 3.2
%ifarch %{ix86}
%ifarch i486
%define _target_cpu	i486
%else
%define _target_cpu	i686
%endif
%endif
%ifarch i386
%define nptl_target_cpu i486
%else
%ifarch i486
%define nptl_target_cpu i686
%else
%define nptl_target_cpu %{_target_cpu}
%endif
%endif
%define target %{nptl_target_cpu}-meego-linux-gnu

# Need AS_NEEDED directive
# Need --hash-style=* support
BuildRequires: binutils >= 2.19.51.0.10
BuildRequires: gcc >= 3.2.1-5
BuildRequires: elfutils >= 0.72
BuildRequires: rpm >= 4.2-0.56
BuildRequires: bison >= 2.7
# GNU make 4.0 introduced the -O option.
BuildRequires: make >= 4.0

%define __find_provides %{_builddir}/%{glibcsrcdir}/find_provides.sh
%define _filter_GLIBC_PRIVATE 1
%define run_glibc_tests 0

%description
The glibc package contains standard libraries which are used by
multiple programs on the system. In order to save disk space and
memory, as well as to make upgrading easier, common system code is
kept in one place and shared between programs. This particular package
contains the most important sets of shared libraries: the standard C
library and the standard math library. Without these two libraries, a
Linux system will not function.

%package devel
Summary: Object files for development using standard C libraries
Group: Development/Libraries
Requires(pre): /sbin/install-info
Requires(pre): %{name}-headers
Requires: %{name}-headers = %{version}-%{release}
Requires: %{name} = %{version}-%{release}

%description devel
The glibc-devel package contains the object files necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).  If you are developing programs which
will use the standard C libraries, your system needs to have these
standard object files available in order to create the
executables.

Install glibc-devel if you are going to develop programs which will
use the standard C libraries.

%package static
Summary: C library static libraries for -static linking
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
The glibc-static package contains the C library static libraries
for -static linking.  You don't need these, unless you link statically,
which is highly discouraged.

%package headers
Summary: Header files for development using standard C libraries
Group: Development/Libraries
Provides: %{name}-headers(%{_target_cpu})
%ifarch x86_64
# If both -m32 and -m64 is to be supported on AMD64, x86_64 glibc-headers
# have to be installed, not i586 ones.
Obsoletes: %{name}-headers(i586)
Obsoletes: %{name}-headers(i686)
%endif
Requires(pre): kernel-headers
Requires: kernel-headers >= 2.2.1, %{name} = %{version}-%{release}
BuildRequires: kernel-headers >= 2.6.22

%description headers
The glibc-headers package contains the header files necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).  If you are developing programs which
will use the standard C libraries, your system needs to have these
standard header files available in order to create the
executables.

Install glibc-headers if you are going to develop programs which will
use the standard C libraries.

%package common
Summary: Common binaries and locale data for glibc
Requires: %{name} = %{version}-%{release}
Requires: tzdata >= 2003a
Group: System/Base

%description common
The glibc-common package includes common binaries for the GNU libc
libraries, as well as national language (locale) support.

######################################################################
# File triggers to do ldconfig calls automatically (see rhbz#1380878)
######################################################################

# File triggers for when libraries are added or removed in standard
# paths.
%transfiletriggerin common -P 2000000 -- /lib /usr/lib /lib64 /usr/lib64
/sbin/ldconfig
%end

%transfiletriggerpostun common -P 2000000 -- /lib /usr/lib /lib64 /usr/lib64
/sbin/ldconfig
%end

# We need to run ldconfig manually because ldconfig cannot handle the
# relative include path in the /etc/ld.so.conf file we gneerate.
# Note: Currently an absolute path is in use
%undefine __brp_ldconfig

######################################################################

%package -n nscd
Summary: A Name Service Caching Daemon (nscd)
Group: System/Daemons
Requires(pre): /usr/sbin/useradd, /usr/sbin/userdel, sh-utils

%description -n nscd
Nscd caches name service lookups and can dramatically improve
performance with NIS+, and may help with DNS as well.

%package utils
Summary: Development utilities from GNU C library
Group: Development/Tools
Requires: %{name} = %{version}-%{release}

%description utils
The glibc-utils package contains memusage, a memory usage profiler,
mtrace, a memory leak tracer and xtrace, a function call tracer
which can be helpful during program debugging.

If unsure if you need this, don't install this package.

%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}

%description doc
%{summary}.

%prep
%setup -q -n %{glibcsrcdir}
xz -dc %SOURCE0 | tar -x

cd %{glibcsrcdir}
%patch1 -p2
%ifarch %{arm}
%patch2 -p1
%endif
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%if 0%{?qemu_user_space_build}
%patch10 -p1
%endif
%patch11 -p1
%patch12 -p1
%patch13 -p1

%build
GCC=gcc
GXX=g++
BuildFlags="-g"
%ifarch %{ix86}
%ifnarch i486
BuildFlags="$BuildFlags -march=core2 -mtune=atom"
%endif
%endif

%ifnarch %{arm}
BuildFlags="$BuildFlags -fasynchronous-unwind-tables"
%endif

%ifarch mipsel
build_CFLAGS="$BuildFlags -O1"
%else
build_CFLAGS="$BuildFlags -O3"
%endif

# Special flag to enable annobin annotations for statically linked
# assembler code.  Needs to be passed to make; not preserved by
# configure.
%define glibc_make_flags_as ASFLAGS="-g"
%define glibc_make_flags %{glibc_make_flags_as}

EnableKernel="--enable-kernel=%{enablekernel}"
# Save the used compiler and options into the file "Gcc" for use later
# by %%install.
echo "$GCC" > Gcc

##############################################################################
# build()
#	Build glibc in `build-%%{target}$1', passing the rest of the arguments
#	as CFLAGS to the build (not the same as configure CFLAGS). Several
#	global values are used to determine build flags, kernel version,
#	system tap support, etc.
##############################################################################
build()
{
	local builddir=build-%{target}${1:+-$1}
	${1+shift}
	rm -rf $builddir
	mkdir $builddir
	pushd $builddir
	../%{glibcsrcdir}/configure CC="$GCC" CXX="$GXX" CFLAGS="$build_CFLAGS" \
		--prefix=%{_prefix} \
		--with-headers=%{_prefix}/include $EnableKernel \
		--enable-bind-now \
		--build=%{target} \
		--enable-stack-protector=strong \
                --disable-profile \
                --enable-obsolete-rpc \
                --disable-profile \
                --enable-obsolete-rpc \
%ifarch %{pie_arches}
		--enable-static-pie \
%endif
		--enable-tunables \
		${core_with_options} \
%ifarch %{ix86}
		--disable-multi-arch \
%endif
%if %{without werror}
		--disable-werror \
%endif
		--disable-profile \
%if %{with bootstrap}
		--without-selinux \
%endif
                libc_cv_slibdir=/lib ||
		{ cat config.log; false; }

# Note: We need /lib instead of /lib64 for aarch64, so we force it here

	make %{?_smp_mflags} -O -r CFLAGS="$build_CFLAGS"
	popd
}

# Default set of compiler options.
build

##############################################################################
# Install glibc...
##############################################################################
%install

# The built glibc is installed into a subdirectory of $RPM_BUILD_ROOT.
# For a system glibc that subdirectory is "/" (the root of the filesystem).
# This is called a sysroot (system root) and can be changed if we have a
# distribution that supports multiple installed glibc versions.
%define glibc_sysroot $RPM_BUILD_ROOT

# Remove existing file lists.
find . -type f -name '*.filelist' -exec rm -rf {} \;

# Reload compiler and build options that were used during %%build.
GCC=`cat Gcc`

# Build and install:
make -j1 install_root=%{glibc_sysroot} install -C build-%{target}

# install_different:
#	Install all core libraries into DESTDIR/SUBDIR. Either the file is
#	installed as a copy or a symlink to the default install (if it is the
#	same). The path SUBDIR_UP is the prefix used to go from
#	DESTDIR/SUBDIR to the default installed libraries e.g.
#	ln -s SUBDIR_UP/foo.so DESTDIR/SUBDIR/foo.so.
#	When you call this function it is expected that you are in the root
#	of the build directory, and that the default build directory is:
#	"../build-%%{target}" (relatively).
#	The primary use of this function is to install alternate runtimes
#	into the build directory and avoid duplicating this code for each
#	runtime.
install_different()
{
	local lib libbase libbaseso dlib
	local destdir="$1"
	local subdir="$2"
	local subdir_up="$3"
	local libdestdir="$destdir/$subdir"
	# All three arguments must be non-zero paths.
	if ! [ "$destdir" \
	       -a "$subdir" \
	       -a "$subdir_up" ]; then
		echo "One of the arguments to install_different was emtpy."
		exit 1
	fi
	# Create the destination directory and the multilib directory.
	mkdir -p "$destdir"
	mkdir -p "$libdestdir"
	# Walk all of the libraries we installed...
	for lib in libc math/libm nptl/libpthread rt/librt nptl_db/libthread_db
	do
		libbase=${lib#*/}
		# Take care that `libbaseso' has a * that needs expanding so
		# take care with quoting.
		libbaseso=$(basename %{glibc_sysroot}/%{_lib}/${libbase}-*.so)
		# Only install if different from default build library.
		if cmp -s ${lib}.so ../build-%{target}/${lib}.so; then
			ln -sf "$subdir_up"/$libbaseso $libdestdir/$libbaseso
		else
			cp -a ${lib}.so $libdestdir/$libbaseso
		fi
		dlib=$libdestdir/$(basename %{glibc_sysroot}/%{_lib}/${libbase}.so.*)
		ln -sf $libbaseso $dlib
	done
}

##############################################################################
# Remove the files we don't want to distribute
##############################################################################

# Remove the libNoVersion files.
# XXX: This looks like a bug in glibc that accidentally installed these
#      wrong files. We probably don't need this today.
rm -f %{glibc_sysroot}/%{_libdir}/libNoVersion*
rm -f %{glibc_sysroot}/%{_lib}/libNoVersion*

# Remove the old nss modules.
rm -f %{glibc_sysroot}/%{_lib}/libnss1-*
rm -f %{glibc_sysroot}/%{_lib}/libnss-*.so.1

# This statically linked binary is no longer necessary in a world where
# the default Fedora install uses an initramfs, and further we have rpm-ostree
# which captures the whole userspace FS tree.
# Further, see https://github.com/projectatomic/rpm-ostree/pull/1173#issuecomment-355014583
rm -f %{glibc_sysroot}/{usr/,}sbin/sln

######################################################################
# Run ldconfig to create all the symbolic links we need
######################################################################

# Note: This has to happen before creating /etc/ld.so.conf.

mkdir -p %{glibc_sysroot}/var/cache/ldconfig
> %{glibc_sysroot}/var/cache/ldconfig/aux-cache

# ldconfig is statically linked, so we can use the new version.
%{glibc_sysroot}/sbin/ldconfig -N -r %{glibc_sysroot}

##############################################################################
# Install info files
##############################################################################

%if %{with docs}
# Move the info files if glibc installed them into the wrong location.
if [ -d %{glibc_sysroot}%{_prefix}/info -a "%{_infodir}" != "%{_prefix}/info" ]; then
  mkdir -p %{glibc_sysroot}%{_infodir}
  mv -f %{glibc_sysroot}%{_prefix}/info/* %{glibc_sysroot}%{_infodir}
  rm -rf %{glibc_sysroot}%{_prefix}/info
fi

# Compress all of the info files.
gzip -9nvf %{glibc_sysroot}%{_infodir}/libc*

%else
rm -f %{glibc_sysroot}%{_infodir}/dir
rm -f %{glibc_sysroot}%{_infodir}/libc.info*
%endif

##############################################################################
# Install configuration files for services
##############################################################################
install -p -m 644 %{glibcsrcdir}/nss/nsswitch.conf %{glibc_sysroot}/etc/nsswitch.conf

%ifnarch %{auxarches}
# This is for ncsd - in glibc 2.2
install -m 644 %{glibcsrcdir}/nscd/nscd.conf %{glibc_sysroot}/etc
mkdir -p %{glibc_sysroot}%{_tmpfilesdir}
install -m 644 %{glibcsrcdir}/nscd/nscd.conf %{buildroot}%{_tmpfilesdir}
mkdir -p %{glibc_sysroot}/lib/systemd/system
install -m 644 %{glibcsrcdir}/nscd/nscd.service %{glibc_sysroot}/lib/systemd/system
%endif

# Include ld.so.conf
echo 'include /etc/ld.so.conf.d/*.conf' > %{glibc_sysroot}/etc/ld.so.conf
echo -n '' > %{glibc_sysroot}/etc/ld.so.cache
chmod 644 %{glibc_sysroot}/etc/ld.so.conf
mkdir -p %{glibc_sysroot}/etc/ld.so.conf.d
%ifnarch %{auxarches}
mkdir -p %{glibc_sysroot}/etc/sysconfig
> %{glibc_sysroot}/etc/sysconfig/nscd
%endif

# Include %%{_libdir}/gconv/gconv-modules.cache
mkdir -p %{glibc_sysroot}%{_libdir}/gconv
echo -n '' > %{glibc_sysroot}%{_libdir}/gconv/gconv-modules.cache
chmod 644 %{glibc_sysroot}%{_libdir}/gconv/gconv-modules.cache


##############################################################################
# Install debug copies of unstripped static libraries
# - This step must be last in order to capture any additional static
#   archives we might have added.
##############################################################################

# If we are building a debug package then copy all of the static archives
# into the debug directory to keep them as unstripped copies.
%if 0%{?_enable_debug_packages}
mkdir -p %{glibc_sysroot}%{_prefix}/lib/debug%{_libdir}
cp -a %{glibc_sysroot}%{_libdir}/*.a \
	%{glibc_sysroot}%{_prefix}/lib/debug%{_libdir}/ || true
rm -f %{glibc_sysroot}%{_prefix}/lib/debug%{_libdir}/*_p.a || true
%endif

# Remove any zoneinfo files; they are maintained by tzdata.
rm -rf %{glibc_sysroot}%{_prefix}/share/zoneinfo

# Make sure %%config files have the same timestamp across multilib packages.
#
# XXX: Ideally ld.so.conf should have the timestamp of the spec file, but there
# doesn't seem to be any macro to give us that.  So we do the next best thing,
# which is to at least keep the timestamp consistent.  The choice of using
# glibc_post_upgrade.c is arbitrary.
touch -r %{SOURCE0} %{glibc_sysroot}/etc/ld.so.conf
touch -r %{glibcsrcdir}/sunrpc/etc.rpc %{glibc_sysroot}/etc/rpc

pushd build-%{target}
$GCC -Os -g -static -o build-locale-archive %{SOURCE1} \
	../build-%{target}/locale/locarchive.o \
	../build-%{target}/locale/md5.o \
	../build-%{target}/locale/record-status.o \
	-I../%{glibcsrcdir} -DDATADIR=\"%{_datadir}\" -DPREFIX=\"%{_prefix}\" \
	-L../build-%{target} \
	-B../build-%{target}/csu/ -lc -lc_nonshared
install -m 700 build-locale-archive %{glibc_sysroot}%{_prefix}/sbin/build-locale-archive
popd

# Lastly copy some additional documentation for the packages.
rm -rf %{glibcsrcdir}/documentation
mkdir %{glibcsrcdir}/documentation
cp %{glibcsrcdir}/timezone/README %{glibcsrcdir}/documentation/README.timezone

#%if 0%{?_enable_debug_packages}

%if %{with docs}
# Remove the `dir' info-heirarchy file which will be maintained
# by the system as it adds info files to the install.
rm -f %{glibc_sysroot}%{_infodir}/dir
%endif

%ifnarch %{auxarches}
mkdir -p %{glibc_sysroot}/var/{db,run}/nscd
touch %{glibc_sysroot}/var/{db,run}/nscd/{passwd,group,hosts,services}
touch %{glibc_sysroot}/var/run/nscd/{socket,nscd.pid}
%endif

# Move libpcprofile.so and libmemusage.so into the proper library directory.
# They can be moved without any real consequences because users would not use
# them directly.
mkdir -p %{glibc_sysroot}%{_libdir}
mv -f %{glibc_sysroot}/%{_lib}/lib{pcprofile,memusage}.so \
	%{glibc_sysroot}%{_libdir}

# Strip all of the installed object files.
strip -g %{glibc_sysroot}%{_libdir}/*.o

###############################################################################
# Rebuild libpthread.a using --whole-archive to ensure all of libpthread
# is included in a static link. This prevents any problems when linking
# statically, using parts of libpthread, and other necessary parts not
# being included. Upstream has decided that this is the wrong approach to
# this problem and that the full set of dependencies should be resolved
# such that static linking works and produces the most minimally sized
# static application possible.
###############################################################################
pushd %{glibc_sysroot}%{_prefix}/%{_lib}/
$GCC -r -nostdlib -o libpthread.o -Wl,--whole-archive ./libpthread.a
rm libpthread.a
ar rcs libpthread.a libpthread.o
rm libpthread.o
popd

##############################################################################
# Build an empty libpthread_nonshared.a for compatiliby with applications
# that have old linker scripts that reference this file. We ship this only
# in compat-libpthread-nonshared sub-package.
##############################################################################
ar cr %{glibc_sysroot}%{_prefix}/%{_lib}/libpthread_nonshared.a

##############################################################################
# Beyond this point in the install process we no longer modify the set of
# installed files, with one exception, for auxarches we cleanup the file list
# at the end and remove files which we don't intend to ship. We need the file
# list to effect a proper cleanup, and so it happens last.
##############################################################################

##############################################################################
# Build the file lists used for describing the package and subpackages.
##############################################################################
# There are several main file lists (and many more for
# the langpack sub-packages (langpack-${lang}.filelist)):
# * master.filelist
#	- Master file list from which all other lists are built.
# * glibc.filelist
#	- Files for the glibc packages.
# * common.filelist
#	- Flies for the common subpackage.
# * utils.filelist
#	- Files for the utils subpackage.
# * nscd.filelist
#	- Files for the nscd subpackage.
# * devel.filelist
#	- Files for the devel subpackage.
# * headers.filelist
#	- Files for the headers subpackage.
# * static.filelist
#	- Files for the static subpackage.
# * libnsl.filelist
#       - Files for the libnsl subpackage
# * nss_db.filelist
# * nss_hesiod.filelist
#       - File lists for nss_* NSS module subpackages.
# * nss-devel.filelist
#       - File list with the .so symbolic links for NSS packages.
# * compat-libpthread-nonshared.filelist.
#	- File list for compat-libpthread-nonshared subpackage.
# * debuginfo.filelist
#	- Files for the glibc debuginfo package.
# * debuginfocommon.filelist
#	- Files for the glibc common debuginfo package.
#

# Create the main file lists. This way we can append to any one of them later
# wihtout having to create it. Note these are removed at the start of the
# install phase.
touch master.filelist
touch glibc.filelist
touch common.filelist
touch utils.filelist
touch nscd.filelist
touch devel.filelist
touch headers.filelist
touch static.filelist
touch libnsl.filelist
touch nss_db.filelist
touch nss_hesiod.filelist
touch nss-devel.filelist
touch compat-libpthread-nonshared.filelist
touch debuginfo.filelist
touch debuginfocommon.filelist

###############################################################################
# Master file list, excluding a few things.
###############################################################################
{
  find $RPM_BUILD_ROOT \( -type f -o -type l \) '!' -path "*/lib/debug/*" \
    | sed -e "s|^${RPM_BUILD_ROOT}||" -e '\|/etc/|s|^|%%config |' \
          -e '\|/gconv-modules$|s|^|%%verify(not md5 size mtime) %%config(noreplace) |' \
          -e '\|/gconv-modules\.cache$|s|^|%%verify(not md5 size mtime) |'
  find $RPM_BUILD_ROOT -type d \
    \( -path '*%{_datadir}/locale' -prune -o \
       \( -path '*%{_datadir}/*' \
        ! -path '*%{_infodir}' -o \
          -path "*%{_includedir}/*" \) \
    \) \
    | grep -v '%{_datadir}/locale' \
    | sed "s|^$RPM_BUILD_ROOT|%%dir |"
} | {

  # primary filelist
  SHARE_LANG='s|.*/share/locale/\([^/_]\+\).*/LC_MESSAGES/.*\.mo|%lang(\1) &|'
  LIB_LANG='s|.*/lib/locale/\([^/_]\+\)|%lang(\1) &|'
  # rpm does not handle %%lang() tagged files hardlinked together accross
  # languages very well, temporarily disable
  LIB_LANG=''
  sed -e "$LIB_LANG" -e "$SHARE_LANG" \
      -e '\,/etc/\(localtime\|nsswitch.conf\|ld\.so\.conf\|ld\.so\.cache\|default\|rpc\|gai\.conf\),d' \
      -e '\,/%{_lib}/lib\(pcprofile\|memusage\)\.so,d' \
      -e '\,bin/\(memusage\|mtrace\|xtrace\|pcprofiledump\),d'
} | sort > master.filelist

# The master file list is now used by each subpackage to list their own
# files. We go through each package and subpackage now and create their lists.
# Each subpackage picks the files from the master list that they need.
# The order of the subpackage list generation does not matter.

# Make the master file list read-only after this point to avoid accidental
# modification.
chmod 0444 master.filelist

###############################################################################
# glibc
###############################################################################

# Add all files with the following exceptions:
# - The info files '%%{_infodir}/dir'
# - The partial (lib*_p.a) static libraries, include files.
# - The static files, objects, unversioned DSOs, and nscd.
# - The bin, locale, some sbin, and share.
#   - The use of [^gi] is meant to exclude all files except glibc_post_upgrade,
#     and iconvconfig, which we want in the main packages.
# - All the libnss files (we add back the ones we want later).
# - All bench test binaries.
# - The aux-cache, since it's handled specially in the files section.
# - The build-locale-archive binary since it's in the common package.
cat master.filelist \
	| grep -v \
	-e '%{_infodir}' \
	-e '%{_libdir}/lib.*_p.a' \
	-e '%{_prefix}/include' \
	-e '%{_libdir}/lib.*\.a' \
        -e '%{_libdir}/.*\.o' \
	-e '%{_libdir}/lib.*\.so' \
	-e 'nscd' \
	-e '%{_prefix}/bin' \
	-e '%{_prefix}/lib/locale' \
	-e '%{_prefix}/sbin/[^gi]' \
	-e '%{_prefix}/share' \
	-e '/var/db/Makefile' \
	-e '/libnss_.*\.so[0-9.]*$' \
	-e '/libnsl' \
	-e 'glibc-benchtests' \
	-e 'aux-cache' \
	-e 'build-locale-archive' \
	> glibc.filelist

cat master.filelist

# Add specific files:
# - The nss_files, nss_compat, and nss_db files.
# - The libmemusage.so and libpcprofile.so used by utils.
cat master.filelist | grep -e '/libnss_' |grep -E -e "(\.so\.[0-9.]+|-[0-9.]+\.so)$" \
  >> glibc.filelist

cat master.filelist | grep -e "libmemusage.so" >> glibc.filelist || true
cat master.filelist | grep -e "libpcprofile.so" >> glibc.filelist || true

cat glibc.filelist
###############################################################################
# glibc-devel
###############################################################################

%if %{with docs}
# Put the info files into the devel file list, but exclude the generated dir.
grep '%{_infodir}' master.filelist | grep -v '%{_infodir}/dir' > devel.filelist
%endif

# Put some static files into the devel package.
grep '%{_libdir}/lib.*\.a' master.filelist \
  | grep '/lib\(\(c\|pthread\|nldbl\|mvec\)_nonshared\|g\|ieee\|mcheck\)\.a$' \
  >> devel.filelist

# Put all of the object files and *.so (not the versioned ones) into the
# devel package.
grep '%{_libdir}/.*\.o' < master.filelist >> devel.filelist
grep '%{_libdir}/lib.*\.so' < master.filelist >> devel.filelist
# The exceptions are:
# - libmemusage.so and libpcprofile.so in glibc used by utils.
# - libnss_*.so which are in nss-devel.
sed -i -e '\,libmemusage.so,d' \
	-e '\,libpcprofile.so,d' \
	-e '\,/libnss_[a-z]*\.so$,d' \
	devel.filelist

###############################################################################
# glibc-headers
###############################################################################

# The glibc-headers package includes only common files which are identical
# across all multilib packages. We must keep gnu/stubs.h and gnu/lib-names.h
# in the glibc-headers package, but the -32, -64, -64-v1, and -64-v2 versions
# go into the development packages.
grep '%{_prefix}/include/gnu/stubs-.*\.h$' < master.filelist >> devel.filelist || :
grep '%{_prefix}/include/gnu/lib-names-.*\.h$' < master.filelist >> devel.filelist || :
# Put the include files into headers file list.
grep '%{_prefix}/include' < master.filelist \
  | grep -v -e '%{_prefix}/include/gnu/stubs-.*\.h$' \
  | grep -v -e '%{_prefix}/include/gnu/lib-names-.*\.h$' \
  > headers.filelist

###############################################################################
# glibc-static
###############################################################################

# Put the rest of the static files into the static package.
grep '%{_libdir}/lib.*\.a' < master.filelist \
  | grep -v '/lib\(\(c\|pthread\|nldbl\|mvec\)_nonshared\|g\|ieee\|mcheck\)\.a$' \
  > static.filelist

###############################################################################
# glibc-common
###############################################################################

# All of the bin and certain sbin files go into the common package except
# glibc_post_upgrade.* and iconvconfig which need to go in glibc. Likewise
# nscd is excluded because it goes in nscd.
grep '%{_prefix}/bin' master.filelist >> common.filelist
grep '%{_prefix}/sbin/[^gi]' master.filelist \
	| grep -v 'nscd' >> common.filelist
# All of the files under share go into the common package since they should be
# multilib-independent.
# Exceptions:
# - The actual share directory, not owned by us.
# - The info files which go in devel, and the info directory.
grep '%{_prefix}/share' master.filelist \
	| grep -v \
	-e '%{_prefix}/share/info/libc.info.*' \
	-e '%%dir %{prefix}/share/info' \
	-e '%%dir %{prefix}/share' \
	>> common.filelist

# Add the binary to build locales to the common subpackage.
echo '%{_prefix}/sbin/build-locale-archive' >> common.filelist

###############################################################################
# nscd
###############################################################################

# The nscd binary must go into the nscd subpackage.
echo '%{_prefix}/sbin/nscd' > nscd.filelist

###############################################################################
# glibc-utils
###############################################################################

# Add the utils scripts and programs to the utils subpackage.
cat > utils.filelist <<EOF
%if %{without bootstrap}
%{_prefix}/%{_lib}/libmemusage.so
%{_prefix}/%{_lib}/libpcprofile.so
#%%{_prefix}/bin/memusage
#%%{_prefix}/bin/memusagestat
%endif
%{_prefix}/bin/mtrace
%{_prefix}/bin/pcprofiledump
%{_prefix}/bin/xtrace
EOF

###############################################################################
# nss_db, nss_hesiod
###############################################################################

# Move the NSS-related files to the NSS subpackages.  Be careful not
# to pick up .debug files, and the -devel symbolic links.
for module in db hesiod; do
  grep -E "/libnss_$module(\.so\.[0-9.]+|-[0-9.]+\.so)$" \
    master.filelist > nss_$module.filelist
done

###############################################################################
# nss-devel
###############################################################################

# Symlinks go into the nss-devel package (instead of the main devel
# package).
grep '/libnss_[a-z]*\.so$' master.filelist > nss-devel.filelist

###############################################################################
# libnsl
###############################################################################

# Prepare the libnsl-related file lists.
grep '/libnsl-[0-9.]*.so$' master.filelist > libnsl.filelist
test $(wc -l < libnsl.filelist) -eq 1

###############################################################################
# compat-libpthread-nonshared
###############################################################################
echo "%{_libdir}/libpthread_nonshared.a" >> compat-libpthread-nonshared.filelist

###############################################################################
# glibc-debuginfocommon, and glibc-debuginfo
###############################################################################

find_debuginfo_args='--strict-build-id -g'
%ifarch %{debuginfocommonarches}
find_debuginfo_args="$find_debuginfo_args \
	-l common.filelist \
	-l utils.filelist \
	-l nscd.filelist \
	-p '.*/(sbin|libexec)/.*' \
	-o debuginfocommon.filelist \
	-l nss_db.filelist -l nss_hesiod.filelist \
	-l libnsl.filelist -l glibc.filelist \
%if %{with benchtests}
	-l benchtests.filelist
%endif
	"
%endif

/usr/lib/rpm/find-debuginfo.sh $find_debuginfo_args -o debuginfo.filelist

# List all of the *.a archives in the debug directory.
list_debug_archives()
{
	local dir=%{_prefix}/lib/debug%{_libdir}
	find %{glibc_sysroot}$dir -name "*.a" -printf "$dir/%%P\n"
}

%ifarch %{debuginfocommonarches}

# Remove the source files from the common package debuginfo.
sed -i '\#^%{glibc_sysroot}%{_prefix}/src/debug/#d' debuginfocommon.filelist

# Create a list of all of the source files we copied to the debug directory.
find %{glibc_sysroot}%{_prefix}/src/debug \
     \( -type d -printf '%%%%dir ' \) , \
     -printf '%{_prefix}/src/debug/%%P\n' > debuginfocommon.sources

%ifarch %{biarcharches}

# Add the source files to the core debuginfo package.
cat debuginfocommon.sources >> debuginfo.filelist

%else

%ifarch %{ix86}
%define basearch i686
%endif
%ifarch sparc sparcv9
%define basearch sparc
%endif

# The auxarches get only these few source files.
auxarches_debugsources=\
'/(generic|linux|%{basearch}|nptl(_db)?)/|/%{glibcsrcdir}/build|/dl-osinfo\.h'

# Place the source files into the core debuginfo pakcage.
grep "$auxarches_debugsources" debuginfocommon.sources >> debuginfo.filelist

# Remove the source files from the common debuginfo package.
grep -v "$auxarches_debugsources" \
  debuginfocommon.sources >> debuginfocommon.filelist

%endif # %%{biarcharches}

# Add the list of *.a archives in the debug directory to
# the common debuginfo package.
list_debug_archives >> debuginfocommon.filelist

%endif # %%{debuginfocommonarches}

# Remove some common directories from the common package debuginfo so that we
# don't end up owning them.
exclude_common_dirs()
{
	exclude_dirs="%{_prefix}/src/debug"
	exclude_dirs="$exclude_dirs $(echo %{_prefix}/lib/debug{,/%{_lib},/bin,/sbin})"
	exclude_dirs="$exclude_dirs $(echo %{_prefix}/lib/debug%{_prefix}{,/%{_lib},/libexec,/bin,/sbin})"

	for d in $(echo $exclude_dirs | sed 's/ /\n/g'); do
		sed -i "\|^%%dir $d/\?$|d" $1
	done
}

%ifarch %{debuginfocommonarches}
exclude_common_dirs debuginfocommon.filelist
%endif
exclude_common_dirs debuginfo.filelist

# %endif # 0%%{?_enable_debug_packages}


cat master.filelist | grep '/libnss_[a-z]*\.so$' master.filelist >> devel.filelist

# remove nss db Makefile
rm %{glibc_sysroot}/var/db/Makefile
# remove libnsl
rm %{glibc_sysroot}/lib/libnsl*

##############################################################################
# Delete files that we do not intended to ship with the auxarch.
# This is the only place where we touch the installed files after generating
# the file lists.
##############################################################################
%ifarch %{auxarches}
echo Cutting down the list of unpackaged files
sed -e '/%%dir/d;/%%config/d;/%%verify/d;s/%%lang([^)]*) //;s#^/*##' \
	common.filelist devel.filelist static.filelist headers.filelist \
	utils.filelist nscd.filelist \
%ifarch %{debuginfocommonarches}
	debuginfocommon.filelist \
%endif
	| (cd %{glibc_sysroot}; xargs --no-run-if-empty rm -f 2> /dev/null || :)
%endif # %%{auxarches}

##############################################################################
# Run the glibc testsuite
##############################################################################
%check
%if %{with testsuite}

# Run the glibc tests. If any tests fail to build we exit %%check with
# an error, otherwise we print the test failure list and the failed
# test output and continue.  Write to standard error to avoid
# synchronization issues with make and shell tracing output if
# standard output and standard error are different pipes.
run_tests () {
  # This hides a test suite build failure, which should be fatal.  We
  # check "Summary of test results:" below to verify that all tests
  # were built and run.
  make %{?_smp_mflags} -O check |& tee rpmbuild.check.log >&2
  test -n tests.sum
  if ! grep -q '^Summary of test results:$' rpmbuild.check.log ; then
    echo "FAIL: test suite build of target: $(basename "$(pwd)")" >& 2
    exit 1
  fi
  set +x
  grep -v ^PASS: tests.sum > rpmbuild.tests.sum.not-passing || true
  if test -n rpmbuild.tests.sum.not-passing ; then
    echo ===================FAILED TESTS===================== >&2
    echo "Target: $(basename "$(pwd)")" >& 2
    cat rpmbuild.tests.sum.not-passing >&2
    while read failed_code failed_test ; do
      for suffix in out test-result ; do
        if test -e "$failed_test.$suffix"; then
	  echo >&2
          echo "=====$failed_code $failed_test.$suffix=====" >&2
          cat -- "$failed_test.$suffix" >&2
	  echo >&2
        fi
      done
    done <rpmbuild.tests.sum.not-passing
  fi

  # Unconditonally dump differences in the system call list.
  echo "* System call consistency checks:" >&2
  cat misc/tst-syscall-list.out >&2
  set -x
}

# Increase timeouts
export TIMEOUTFACTOR=16
parent=$$
echo ====================TESTING=========================

# Default libraries.
pushd build-%{target}
run_tests
popd


echo ====================TESTING END=====================
PLTCMD='/^Relocation section .*\(\.rela\?\.plt\|\.rela\.IA_64\.pltoff\)/,/^$/p'
echo ====================PLT RELOCS LD.SO================
readelf -Wr %{glibc_sysroot}/%{_lib}/ld-*.so | sed -n -e "$PLTCMD"
echo ====================PLT RELOCS LIBC.SO==============
readelf -Wr %{glibc_sysroot}/%{_lib}/libc-*.so | sed -n -e "$PLTCMD"
echo ====================PLT RELOCS END==================

# Finally, check if valgrind runs with the new glibc.
# We want to fail building if valgrind is not able to run with this glibc so
# that we can then coordinate with valgrind to get it fixed before we update
# glibc.
pushd build-%{target}

# Show the auxiliary vector as seen by the new library
# (even if we do not perform the valgrind test).
LD_SHOW_AUXV=1 elf/ld.so --library-path .:elf:nptl:dlfcn /bin/true

%if %{with valgrind}
elf/ld.so --library-path .:elf:nptl:dlfcn \
	/usr/bin/valgrind --error-exitcode=1 \
	elf/ld.so --library-path .:elf:nptl:dlfcn /usr/bin/true
%endif
popd

%endif # %%{run_glibc_tests}


%pre -p <lua>
-- Check that the running kernel is new enough
required = '%{enablekernel}'
rel = posix.uname("%r")
if rpm.vercmp(rel, required) < 0 then
  error("FATAL: kernel too old", 0)
end

%if %{with docs}
%post devel
/sbin/install-info %{_infodir}/libc.info.gz %{_infodir}/dir > /dev/null 2>&1 || :
%endif

%pre headers
# this used to be a link and it is causing nightmares now
if [ -L %{_prefix}/include/scsi ] ; then
  rm -f %{_prefix}/include/scsi
fi

%if %{with docs}
%preun devel
if [ "$1" = 0 ]; then
  /sbin/install-info --delete %{_infodir}/libc.info.gz %{_infodir}/dir > /dev/null 2>&1 || :
fi
%endif

%pre -n nscd
getent group nscd >/dev/null || /usr/sbin/groupadd -g 28 -r nscd
getent passwd nscd >/dev/null ||
  /usr/sbin/useradd -M -o -r -d / -s /sbin/nologin \
		    -c "NSCD Daemon" -u 28 -g nscd nscd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n glibc-devel -p /sbin/ldconfig

%postun -n glibc-devel -p /sbin/ldconfig

%post -n nscd
%systemd_post nscd.service

%preun -n nscd
%systemd_preun nscd.service

%postun -n nscd
if test $1 = 0; then
  /usr/sbin/userdel nscd > /dev/null 2>&1 || :
fi
%systemd_postun_with_restart nscd.service

%files -f glibc.filelist
%dir %{_prefix}/%{_lib}/audit
%ifarch s390x
/lib/ld64.so.1
%endif
%verify(not md5 size mtime) %config(noreplace) /etc/nsswitch.conf
%verify(not md5 size mtime) %config(noreplace) /etc/ld.so.conf
%verify(not md5 size mtime) %config(noreplace) /etc/rpc
%dir /etc/ld.so.conf.d
%dir %{_prefix}/libexec/getconf
%dir %{_libdir}/gconv
%dir %attr(0700,root,root) /var/cache/ldconfig
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/cache/ldconfig/aux-cache
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /etc/ld.so.cache
%doc %{glibcsrcdir}/README %{glibcsrcdir}/NEWS %{glibcsrcdir}/INSTALL %{glibcsrcdir}/elf/rtld-debugger-interface.txt
# If rpm doesn't support %%license, then use %%doc instead.
%{!?_licensedir:%global license %%doc}
%license %{glibcsrcdir}/COPYING %{glibcsrcdir}/COPYING.LIB %{glibcsrcdir}/LICENSES

%ifnarch %{auxarches}
%files -f common.filelist common
%doc %{glibcsrcdir}/documentation/README.timezone

%files -f devel.filelist devel

%files -f static.filelist static

%files -f headers.filelist headers

%files -f utils.filelist utils

%files -f nscd.filelist -n nscd
%config(noreplace) /etc/nscd.conf
%dir %attr(0755,root,root) /var/run/nscd
%dir %attr(0755,root,root) /var/db/nscd
/lib/systemd/system/nscd.service
#/lib/systemd/system/nscd.socket
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/nscd.pid
%attr(0666,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/socket
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/passwd
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/group
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/hosts
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/services
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/passwd
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/group
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/hosts
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/services
%ghost %config(missingok,noreplace) /etc/sysconfig/nscd
%endif

%files doc
%defattr(-,root,root)
%{_docdir}/%{name}-%{version}
