
case $(tty) in
(/dev/tty[0-9]|/dev/tty[0-9][0-9])

	if [ -f /etc/sysconfig/console ]
	then
		. /etc/sysconfig/console
	
		if [ "$CONSOLEMAP" != "" ]
		then
			# Switch the G0 charset map from the default ISO-8859-1
			# to the user-defined map (loaded with consolefonts)
			echo -n -e '\033(K' > /proc/$$/fd/0
		fi
		
	fi
        if dmesg|grep 'Console: mono' >/dev/null 2>&1
	then
	        TERM=linux-m
	        export TERM
	fi
	;;
esac
