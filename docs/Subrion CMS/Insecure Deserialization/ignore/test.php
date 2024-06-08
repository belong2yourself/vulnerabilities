<?php

$re = '/__st\".*\svalue\=\"(\w*)\"/m';
$str = '<input type="hidden" name="__st" value="E67yMwCcQvwydseYwRU5hI4lHD9mcghPUT1p80Ug">';

preg_match_all($re, $str, $matches, PREG_SET_ORDER, 0);

// Print the entire match result
var_dump($matches);
?>