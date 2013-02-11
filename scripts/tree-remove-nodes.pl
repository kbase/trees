#!/usr/bin/env perl
use strict;
use warnings;
use Getopt::Long;
use Data::Dumper;

use Bio::KBase::Tree::Client;
use Bio::KBase::Tree::Util qw(get_tree_client);


my $DESCRIPTION =
"
NAME
      tree-remove-nodes -- remove nodes by label in a tree and simplify the tree

SYNOPSIS
      tree-remove-nodes [OPTIONS] [NEWICK_TREE]

DESCRIPTION
     Given a tree in newick format, remove the nodes with the given names indicated
     in the list, and simplify the tree.  Simplifying a tree involves removing unnamed
     internal nodes that have only one child, and removing unnamed leaf nodes.  During
     the removal process, edge lengths (if they exist) are conserved so that the summed
     end to end distance between any two nodes left in the tree will remain the same.
     If the tree is not provided as an argument and no input file is specified,
     the tree is read in from standard-in.
      
      -r, --removal-list
                        specify the file name of the list of nodes to remove; this file should
                        be a one column file where each line contains the name of the node to
                        remove; if multiple nodes have a identical labels, they are all
                        removed
                        
      -i, --input
                        specify an input file to read the tree from
                        
      -h, --help
                        diplay this help message, ignore all arguments
                        
                        
EXAMPLES
      Replace node names based on the file mapping.txt
      > cat removal_list.txt
      mr_tree
      > tree-remove-nodes -r removal_list.txt '(l1,mr_tree,l3,l4)root;'
      (l1,l3,l4)root;

AUTHORS
      Michael Sneddon (mwsneddon\@lbl.gov)
      Matt Henderson (mhenderson\@lbl.gov)

";


my $help = '';
my $treeString='';
my $inputFile = '';
my $removalFile = '';

# parse arguments and output file
my $stdinString = "";
my $opt = GetOptions("help" => \$help,
                     "input=s" => \$inputFile,
                     "removal-list=s" => \$removalFile
                     );
if($help) {
     print $DESCRIPTION;
     exit 0;
}
if(!$removalFile) {
     print "FAILURE - no removal list specified.  Run with -h for usage.\n";
     exit 1;
}


my $n_args = $#ARGV + 1;
# if we have specified an input file, then read the file
if($inputFile) {
     my $inputFileHandle;
     open($inputFileHandle, "<", $inputFile);
     if(!$inputFileHandle) {
          print "FAILURE - cannot open '$inputFile' \n$!\n";
          exit 1;
     }
     eval {
          while (my $line = <$inputFileHandle>) {
               chomp($line);
               $treeString = $treeString.$line;
          }
          close $inputFileHandle;
     };
}

# if we have a single argument, then accept it as the treeString
elsif($n_args==1) {
     $treeString = $ARGV[0];
     chomp($treeString);
}

# if we have no arguments, then read the tree from standard-in
elsif($n_args == 0) {
     while(my $line = <STDIN>) {
          chomp($line);
          $treeString = $treeString.$line;
     }
}

# otherwise we have some bad number of commandline args
else {
    print "Bad options / Invalid number of arguments.  Run with --help for usage.\n";
    exit 1;
}

#create client
my $treeClient;
eval{ $treeClient = get_tree_client(); };
my $client_error = $@;
if ($client_error) {
     print Dumper($client_error);
     print "FAILURE - unable to create tree service client.  Is you tree URL correct? see tree-url.\n";
     exit 1;
}

# make sure we got something out of all of that
if ($treeString ne '') {
     
     my $removalList = [];
     my $inputFileHandle;
     open($inputFileHandle, "<", $removalFile);
     if(!$inputFileHandle) {
          print "FAILURE - cannot open removal list file '$removalFile' \n$!\n";
          exit 1;
     }
     eval {
          my $line_number =0;
          while (my $line = <$inputFileHandle>) {
               $line_number++;
               chomp($line);
               if($line eq '') { next; }
               push @$removalList, $line;
          }
          close $inputFileHandle;
     };
     my $new_tree;
     eval {
          $new_tree = $treeClient->remove_node_names_and_simplify($treeString, $removalList);
     };

     $client_error = $@;
     if ($client_error) {
          print Dumper($client_error);
          print "FAILURE - error calling Tree service.\n";
          exit 1;
     }

     print $new_tree."\n";
     exit 0;
     
} else {
     print "FAILURE - no tree specified.  Run with --help for usage.\n";
     exit 1;
}

exit 0;

