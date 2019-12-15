
use strict;
use warnings;

my $testcase = 100;

foreach (my $i = 0; $i < $testcase ; $i++) {
  system('python _generator.py > test/test-randlen-'.$i.'.txt')
}
