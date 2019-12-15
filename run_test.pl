
use strict;
use warnings;

my $testcase = 100;

foreach (my $i = 0; $i < $testcase ; $i++) {
  system('python main.py test/test-randlen-'.$i.'.txt')
}
