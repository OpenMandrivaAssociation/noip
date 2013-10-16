Summary:	Linux client for the no-ip.com dynamic DNS service
Name:		noip
Version:	2.1.9
Release:	8
License:	GPLv2+
Group:		Networking/Other
URL:		http://www.no-ip.com
Source0:	http://www.no-ip.com/client/linux/%{name}-%{version}.tar.bz2
Source1:	%{name}-initscript
Patch0:		%{name}-2.1.9-makefile.patch
Patch1:		%{name}-2.1.9-config-path.patch
Requires(pre):	rpm-helper
Requires(post):	rpm-helper

%description
This is the No-IP.com Dynamic DNS update client page.

When configured correctly, the client will check your IP address at a
given time interval checking to see if your IP has changed. If your IP
address has changed it will notify No-IP DNS servers and update the IP
corresponding to your No-IP/No-IP+ hostname.

NOTE: You must add hostnames on the website (http://www.no-ip.com)
first before you can have the updater update them.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
mv -f %{name}2.c %{name}.c

%build
%define Werror_cflags %{nil}
%if %mdvver >= 201200
%serverbuild_hardened
%else
%serverbuild
%endif

%make PREFIX="%{_prefix}" BINDIR="%{_sbindir}" CONFDIR="%{_sysconfdir}"

%install
%makeinstall_std PREFIX=%{_prefix} CONFDIR="%{_sysconfdir}" BINDIR="%{_sbindir}"

touch %{buildroot}%{_sysconfdir}/%{name}.conf
mkdir -p %{buildroot}%{_initrddir}
install %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

cat > README.urpmi << EOF
To configure the noip deamon, run noip -C as root.
This command will set the corrects parameters in /etc/noip.conf.
Then you can start the deamon with service noip start
EOF

%post
%create_ghostfile %{_sysconfdir}/%{name}.conf root root 600
%_post_service %{name}

echo
echo To configure the noip deamon, run noip -C as root.
echo This command will set the correct parameters in /etc/noip.conf.
echo Then you can restart the deamon with "service noip restart".
echo

%preun
%_preun_service %{name}

%files
%doc README.FIRST README.urpmi
%attr(755,root,root) %{_sbindir}/*
%attr(744,root,root) %{_initrddir}/%{name}
%ghost %{_sysconfdir}/%{name}.conf


%changelog
* Sun Oct 02 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 2.1.9-5mdv2012.0
+ Revision: 702407
- use %%serverbuild_hardened flags for mdv2012

* Mon Sep 12 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 2.1.9-4
+ Revision: 699580
- enable %%serverbuild and pass ldflags

* Sat Dec 11 2010 Oden Eriksson <oeriksson@mandriva.com> 2.1.9-3mdv2011.0
+ Revision: 620505
- the mass rebuild of 2010.0 packages

* Mon Sep 14 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 2.1.9-2mdv2010.0
+ Revision: 440531
- use Werror_cflags

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Tue Nov 25 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.1.9-1mdv2009.1
+ Revision: 306800
- update to new version 2.1.9
- rewrite patch 0 and 1

* Sun Sep 14 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.1.7-4mdv2009.0
+ Revision: 284710
- rebuild

* Tue Jul 29 2008 Thierry Vignaud <tv@mandriva.org> 2.1.7-3mdv2009.0
+ Revision: 254058
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Fri Sep 14 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2.1.7-1mdv2008.1
+ Revision: 85688
- new version

* Sun Jul 08 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2.1.4-1mdv2008.0
+ Revision: 49806
- bzip source
- new version
- fix mixture of tabs and spaces


* Mon Jan 22 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2.1.3-4mdv2007.0
+ Revision: 111884
- fix config path

* Sat Jan 20 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2.1.3-3mdv2007.1
+ Revision: 111083
- bump release tag
- correct chmod bits on initscript

* Thu Jan 18 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2.1.3-2mdv2007.1
+ Revision: 110380
- fix post scriplet
- minor fixes, cleans

* Thu Jan 18 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2.1.3-1mdv2007.1
+ Revision: 110221
- Import noip

