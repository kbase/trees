#  Simple module that returns the host and port to use to test the service.  Could be extended to
#  read a config file if more config options are required in the future.
#
#  created Oct 2012 by msneddon

package TreeTestConfig;

use strict;
use warnings;
require Exporter;
our @ISA = qw(Exporter);
our @EXPORT_OK = qw(getHost getPort);


# CHANGE THE HOST AND PORT CONFIGURATION HERE
my $host = "http://localhost";
my $port = "7047";


sub getHost  { return $host; }
sub getPort  { return $port; }


1;
