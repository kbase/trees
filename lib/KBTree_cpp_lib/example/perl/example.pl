#!/usr/bin/perl

use lib "../../lib/perl_interface";
use KBTreeUtil;

print "Testing KBTreeUtil Interface\n";

my $TreeString = "((A:1[as],C:1)D:1,[hellp]B[adf]:1)E;";
$t = new KBTreeUtil::KBTree($TreeString);
my $nodeCount = $t->getNodeCount();
print $t->getNodeCount()."\n";
$t->printTree();

print $t->toNewick(4)."\n";

print $t->getAllLeafNames()."\n";

# get all the names of the leaves
my $leaf_names = $t->getAllLeafNames();
my @values = split(';', $leaf_names);
foreach my $val (@values) {
    print "$val\n";
}

$t->removeNodesByNameAndSimplify("D");
$nodeCount = $t->getNodeCount();
print $t->getNodeCount()."\n";
$t->printTree();

print $t->toNewick(4)."\n";


print "\ndone.\n";

