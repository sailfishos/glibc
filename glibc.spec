%define glibcsrcdir glibc-2.25

Name: glibc

Summary: GNU C library shared libraries
Version: 2.25+git5
Release: 0
License: LGPLv2+ and LGPLv2+ with exceptions and GPLv2+
Group: System/Libraries
URL: http://www.gnu.org/software/libc/
Source0: glibc-2.25.tar.xz
Source11: build-locale-archive.c

Patch1: glibc-arm-alignment-fix.patch
Patch2: glibc-2.25-arm-runfast.patch
Patch3: glibc-2.25-no-timestamping.patch
Patch4: glibc-2.25-elf-rtld.diff
Patch5: glibc-2.25-ldso-rpath-prefix-option.diff
Patch6: glibc-2.25-nsswitchconf-location.diff
Patch7: glibc-2.25-nscd-socket-location.diff
Patch8: glibc-2.25-ldso-nodefaultdirs-option.diff
Patch9: glibc-2.14-locarchive-fedora.patch
Patch10: eglibc-2.15-fix-neon-libdl.patch
Patch11: eglibc-2.19-shlib-make.patch
Patch12: glibc-2.25-bits.patch
Patch13: ubuntu-2.25.6-git-updates.diff

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
BuildRequires: gawk,  util-linux, quilt
# This gcc >= 3.2 is to ensure that __frame_state_for is exported by glibc
# will be compatible with egcs 1.x.y
BuildRequires: gcc >= 3.2
%define enablekernel 2.6.32
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
%patch3 -p1
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

EnableKernel="--enable-kernel=%{enablekernel}"
echo "$GCC" > Gcc

builddir=build-%{name}-%{version}
rm -rf build-%{name}-*
mkdir $builddir ; cd $builddir

echo libdir=/usr/lib > configparms
echo slibdir=/lib >> configparms
echo BUILD_CC=gcc >> configparms

%ifarch mipsel
build_CFLAGS="$BuildFlags -O1"
%else
build_CFLAGS="$BuildFlags -O3"
%endif

export MAKEINFO=:

../%{glibcsrcdir}/configure CC="$GCC" CXX="$GXX" CFLAGS="$build_CFLAGS" \
	--prefix=%{_prefix} \
	"--enable-add-ons=libidn" --without-cvs $EnableKernel \
	--enable-bind-now --with-tls \
	--with-headers=%{_prefix}/include \
%ifarch %{multiarcharches}
	--enable-multi-arch \
%endif
	--disable-profile --enable-obsolete-rpc \
    --enable-stack-protector=strong \
    --build=%{target}

make %{?_smp_mflags} -r CFLAGS="$build_CFLAGS"

cd ..

$GCC -Os -static -o build-locale-archive %SOURCE11 \
  ./build-%{name}-%{version}/locale/locarchive.o \
  ./build-%{name}-%{version}/locale/md5.o \
  -DDATADIR=\"%{_datadir}\" -DPREFIX=\"%{_prefix}\" \
  -L./build-%{name}-%{version} -I%{glibcsrcdir}

%install
rm -rf ${RPM_BUILD_ROOT}
cd build-%{name}-%{version}
make -j1 install_root=${RPM_BUILD_ROOT} install

install -p -m 644 ../%{glibcsrcdir}/nss/nsswitch.conf $RPM_BUILD_ROOT/etc/nsswitch.conf

mkdir -p $RPM_BUILD_ROOT/etc/default
install -p -m 644 ../%{glibcsrcdir}/nis/nss $RPM_BUILD_ROOT/etc/default/nss

install -m 644 ../%{glibcsrcdir}/nscd/nscd.conf $RPM_BUILD_ROOT/etc

# Include ld.so.conf
echo 'include /etc/ld.so.conf.d/*.conf' > $RPM_BUILD_ROOT/etc/ld.so.conf
> $RPM_BUILD_ROOT/etc/ld.so.cache
chmod 644 $RPM_BUILD_ROOT/etc/ld.so.conf
mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
> $RPM_BUILD_ROOT/etc/sysconfig/nscd

# Include %{_prefix}/%{_lib}/gconv/gconv-modules.cache
> $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gconv/gconv-modules.cache
chmod 644 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gconv/gconv-modules.cache

strip -g $RPM_BUILD_ROOT%{_prefix}/%{_lib}/*.o

mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_prefix}/%{_lib}
cp -a $RPM_BUILD_ROOT%{_prefix}/%{_lib}/*.a \
  $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_prefix}/%{_lib}/
rm -f $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_prefix}/%{_lib}/*_p.a
# Now strip debugging info from static libraries
pushd $RPM_BUILD_ROOT%{_prefix}/%{_lib}/
for i in *.a; do
  if [ -f $i ]; then
    case "$i" in
    *_p.a) ;;
    *) strip -g -R .comment $i ;;
    esac
  fi
done
popd

mkdir -p $RPM_BUILD_ROOT/%{_prefix}/lib/locale/

%ifarch armv7hl armv7tnhl armv7nhl
ln -s /lib/ld-linux-armhf.so.3 ${RPM_BUILD_ROOT}/lib/ld-linux.so.3
%endif

rm -f ${RPM_BUILD_ROOT}/%{_lib}/libnss1-*
rm -f ${RPM_BUILD_ROOT}/%{_lib}/libnss-*.so.1

# Ugly hack for buggy rpm
ln -f ${RPM_BUILD_ROOT}%{_sbindir}/iconvconfig{,.%{_target_cpu}}

rm -f $RPM_BUILD_ROOT/etc/gai.conf

# In F7+ this is provided by rpcbind rpm
rm -f $RPM_BUILD_ROOT%{_sbindir}/rpcinfo

# BUILD THE FILE LIST
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
  # rpm does not handle %lang() tagged files hardlinked together accross
  # languages very well, temporarily disable
  LIB_LANG=''
  sed -e "$LIB_LANG" -e "$SHARE_LANG" \
      -e '\,/etc/\(localtime\|nsswitch.conf\|ld\.so\.conf\|ld\.so\.cache\|default\),d' \
      -e '\,/%{_lib}/lib\(pcprofile\|memusage\)\.so,d' \
      -e '\,bin/\(memusage\|mtrace\|xtrace\|pcprofiledump\),d'
} | sort > rpm.filelist

mkdir -p $RPM_BUILD_ROOT%{_prefix}/%{_lib}
mv -f $RPM_BUILD_ROOT/%{_lib}/lib{pcprofile,memusage}.so $RPM_BUILD_ROOT%{_prefix}/%{_lib}

grep '%{_prefix}/include/gnu/stubs-[32164]\+\.h' < rpm.filelist >> devel.filelist || :

grep '%{_prefix}/include' < rpm.filelist |
  egrep -v '%{_prefix}/include/(linuxthreads|gnu/stubs-[32164]+\.h)' \
	> headers.filelist

sed -i -e '\|%{_prefix}/%{_lib}/lib.*_p.a|d' \
       -e '\|%{_prefix}/include|d' \
       -e '\|%{_infodir}|d' rpm.filelist

grep '%{_prefix}/%{_lib}/lib.*\.a' < rpm.filelist \
  | grep '/lib\(\(c\|pthread\|nldbl\)_nonshared\|bsd\(\|-compat\)\|g\|ieee\|mcheck\|rpcsvc\)\.a$' \
  >> devel.filelist
grep '%{_prefix}/%{_lib}/lib.*\.a' < rpm.filelist \
  | grep -v '/lib\(\(c\|pthread\|nldbl\)_nonshared\|bsd\(\|-compat\)\|g\|ieee\|mcheck\|rpcsvc\)\.a$' \
  > static.filelist
grep '%{_prefix}/%{_lib}/.*\.o' < rpm.filelist >> devel.filelist
grep '%{_prefix}/%{_lib}/lib.*\.so' < rpm.filelist >> devel.filelist

sed -i -e '\|%{_prefix}/%{_lib}/lib.*\.a|d' \
       -e '\|%{_prefix}/%{_lib}/.*\.o|d' \
       -e '\|%{_prefix}/%{_lib}/lib.*\.so|d' \
       -e '\|%{_prefix}/%{_lib}/linuxthreads|d' \
       -e '\|nscd|d' rpm.filelist

grep '%{_prefix}/bin' < rpm.filelist >> common.filelist
#grep '%{_prefix}/lib/locale' < rpm.filelist | grep -v /locale-archive.tmpl >> common.filelist
#grep '%{_prefix}/libexec/pt_chown' < rpm.filelist >> common.filelist
grep '%{_prefix}/sbin/[^gi]' < rpm.filelist >> common.filelist
grep '%{_prefix}/share' < rpm.filelist | \
  grep -v '%{_prefix}/share/zoneinfo' >> common.filelist

sed -i -e '\|%{_prefix}/bin|d' \
       -e '\|%{_prefix}/lib/locale|d' \
       -e '\|%{_prefix}/sbin/[^gi]|d' \
       -e '\|%{_prefix}/share|d' rpm.filelist

> nosegneg.filelist

echo '%{_prefix}/sbin/build-locale-archive' >> common.filelist
echo '%{_prefix}/sbin/nscd' > nscd.filelist

cat > utils.filelist <<EOF
%{_prefix}/%{_lib}/libmemusage.so
%{_prefix}/%{_lib}/libpcprofile.so
#%{_prefix}/bin/memusage
#%{_prefix}/bin/memusagestat
%{_prefix}/bin/mtrace
%{_prefix}/bin/pcprofiledump
%{_prefix}/bin/xtrace
EOF

# /etc/localtime
rm -f $RPM_BUILD_ROOT/etc/localtime
#ls -al $RPM_BUILD_ROOT%{_prefix}/share/zoneinfo/
#cp -f $RPM_BUILD_ROOT%{_prefix}/share/zoneinfo/US/Eastern $RPM_BUILD_ROOT/etc/localtime
ln -sf %{_prefix}/share/zoneinfo/US/Eastern $RPM_BUILD_ROOT/etc/localtime

rm -rf $RPM_BUILD_ROOT%{_prefix}/share/zoneinfo

# the last bit: more documentation
rm -rf ../documentation
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
bzip2 -9 ../%{glibcsrcdir}/ChangeLog*
install -m0644 -t $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} \
        ../%{glibcsrcdir}/crypt/README.ufc-crypt \
        ../%{glibcsrcdir}/ChangeLog{,.16,.17}.bz2 \
        ../%{glibcsrcdir}/posix/gai.conf \
        ../%{glibcsrcdir}/README \
        ../%{glibcsrcdir}/NEWS \
        ../%{glibcsrcdir}/INSTALL \
        ../%{glibcsrcdir}/BUGS \
        ../%{glibcsrcdir}/CONFORMANCE \
        ../%{glibcsrcdir}/hesiod/README.hesiod
install -m0644 ../%{glibcsrcdir}/timezone/README \
        $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/README.timezone

cp ../%{glibcsrcdir}/{COPYING,COPYING.LIB,LICENSES} ..

%if 0%{run_glibc_tests}

# Increase timeouts
export TIMEOUTFACTOR=16
parent=$$
echo ====================TESTING=========================
cd build-%{nptl_target_cpu}-linuxnptl
( make %{?_smp_mflags} -k check PARALLELMFLAGS=-s 2>&1
  sleep 10s
  teepid="`ps -eo ppid,pid,command | awk '($1 == '${parent}' && $3 ~ /^tee/) { print $2 }'`"
  [ -n "$teepid" ] && kill $teepid
) | tee check.log || :
cd ..
echo ====================TESTING DETAILS=================
for i in `sed -n 's|^.*\*\*\* \[\([^]]*\.out\)\].*$|\1|p' build-*-linux*/check.log`; do
  echo =====$i=====
  cat $i || :
  echo ============
done
echo ====================TESTING END=====================
PLTCMD='/^Relocation section .*\(\.rela\?\.plt\|\.rela\.IA_64\.pltoff\)/,/^$/p'
echo ====================PLT RELOCS LD.SO================
readelf -Wr $RPM_BUILD_ROOT/%{_lib}/ld-*.so | sed -n -e "$PLTCMD"
echo ====================PLT RELOCS LIBC.SO==============
readelf -Wr $RPM_BUILD_ROOT/%{_lib}/libc-*.so | sed -n -e "$PLTCMD"
echo ====================PLT RELOCS END==================

%endif

pushd $RPM_BUILD_ROOT/usr/%{_lib}/
gcc -r -nostdlib -o libpthread.o -Wl,--whole-archive ./libpthread.a
rm libpthread.a
ar rcs libpthread.a libpthread.o
rm libpthread.o
popd

find_debuginfo_args='--strict-build-id -g'
/usr/lib/rpm/find-debuginfo.sh $find_debuginfo_args -o debuginfo.filelist
# Remove any duplicates output by a buggy find-debuginfo.sh.
sort -u debuginfo.filelist > debuginfo2.filelist
mv debuginfo2.filelist debuginfo.filelist

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

exclude_common_dirs debuginfo.filelist

mkdir -p $RPM_BUILD_ROOT/var/{db,run}/nscd
touch $RPM_BUILD_ROOT/var/{db,run}/nscd/{passwd,group,hosts,services}
touch $RPM_BUILD_ROOT/var/run/nscd/{socket,nscd.pid}

install -m 700 ../build-locale-archive $RPM_BUILD_ROOT/usr/sbin/build-locale-archive

mkdir -p $RPM_BUILD_ROOT/var/cache/ldconfig
> $RPM_BUILD_ROOT/var/cache/ldconfig/aux-cache

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%pre headers
# this used to be a link and it is causing nightmares now
if [ -L %{_prefix}/include/scsi ] ; then
  rm -f %{_prefix}/include/scsi
fi

%post utils -p /sbin/ldconfig

%postun utils -p /sbin/ldconfig

%pre -n nscd
/usr/sbin/useradd -M -o -r -d / -s /sbin/nologin \
  -c "NSCD Daemon" -u 28 nscd > /dev/null 2>&1 || :

%postun -n nscd
if [ $1 = 0 ] ; then
  /usr/sbin/userdel nscd > /dev/null 2>&1 || :
fi
if [ "$1" -ge "1" ]; then
  service nscd condrestart > /dev/null 2>&1 || :
fi


%files -f build-%{name}-%{version}/rpm.filelist
%defattr(-,root,root)
%verify(not md5 size mtime) %config(noreplace) /etc/localtime
%verify(not md5 size mtime) %config(noreplace) /etc/nsswitch.conf
%verify(not md5 size mtime) %config(noreplace) /etc/ld.so.conf
%dir /etc/ld.so.conf.d
%dir %{_prefix}/libexec/getconf
%dir %{_prefix}/%{_lib}/gconv
%dir %attr(0700,root,root) /var/cache/ldconfig
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/cache/ldconfig/aux-cache
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /etc/ld.so.cache
%license COPYING COPYING.LIB LICENSES


%ifnarch %{auxarches}
%files -f build-%{name}-%{version}/common.filelist common
%defattr(-,root,root)
%dir %{_prefix}/lib/locale
%dir %attr(755,root,root) /etc/default
%verify(not md5 size mtime) %config(noreplace) /etc/default/nss

%files -f build-%{name}-%{version}/devel.filelist devel
%defattr(-,root,root)

%files -f build-%{name}-%{version}/static.filelist static
%defattr(-,root,root)

%files -f build-%{name}-%{version}/headers.filelist headers
%defattr(-,root,root)

%files -f build-%{name}-%{version}/utils.filelist utils
%defattr(-,root,root)

%files -f build-%{name}-%{version}/nscd.filelist -n nscd
%defattr(-,root,root)
%config(noreplace) /etc/nscd.conf
%dir %attr(0755,root,root) /var/run/nscd
%dir %attr(0755,root,root) /var/db/nscd
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
