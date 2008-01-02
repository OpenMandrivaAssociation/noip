Summary:	Linux client for the no-ip.com dynamic DNS service
Name:		noip
Version:	2.1.7
Release:	%mkrel 1
License:	GPL
Group:		Networking/Other
URL:		http://www.no-ip.com
Source0:	http://www.no-ip.com/client/linux/%{name}-%{version}.tar.bz2
Source1:	%{name}-initscript
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-config-path.patch
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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
%patch0 -p0
%patch1 -p0
mv -f %{name}2.c %{name}.c

%build
perl -pi -e "s/CCFLAGS=.*/CCFLAGS=%{optflags}/" Makefile

%make 

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std 

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

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc README.FIRST README.urpmi
%attr(755,root,root) %{_sbindir}/*
%attr(744,root,root) %{_initrddir}/%{name}
%ghost %{_sysconfdir}/%{name}.conf
