Summary:	Linux client for the no-ip.com dynamic DNS service
Name:		noip
Version:	2.1.9
Release:	8
License:	GPLv2+
Group:		Networking/Other
URL:		http://www.no-ip.com
Source0:	http://www.no-ip.com/client/linux/%{name}-%{version}.tar.bz2
Source1:	%{name}.service
Source2:	%{name}.sysusers
BuildRequires:	systemd-macros

%description
This is the No-IP.com Dynamic DNS update client page.

When configured correctly, the client will check your IP address at a
given time interval checking to see if your IP has changed. If your IP
address has changed it will notify No-IP DNS servers and update the IP
corresponding to your No-IP/No-IP+ hostname.

NOTE: You must add hostnames on the website (http://www.no-ip.com)
first before you can have the updater update them.

%prep
%autosetup -p1

%build
%define Werror_cflags %{nil}
%serverbuild_hardened
sed -i 's|@OPTFLAGS@|%{optflags}|g;s|@SBINDIR@|%{buildroot}%{_sbindir}|g;s|@SYSCONFDIR@|%{buildroot}%{_sysconfdir}|g' Makefile

%make_build

%install
%make_install

# Make dummy config file
mkdir -p %{buildroot}/%{_sysconfdir}
touch %{buildroot}/%{_sysconfdir}/no-ip2.conf

install -Dm644  %{SOURCE1} %{buildroot}%{_unitdir}/noip.service
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.conf

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%doc COPYING README.FIRST
%{_sbindir}/noip2
%{_sysusersdir}/%{name}.conf
%attr(600,noip,noip) %config(noreplace) %{_sysconfdir}/no-ip2.conf
%{_unitdir}/noip.service
