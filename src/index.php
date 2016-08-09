<?php 
phpinfo();
$a='123';echo $a;

function test(&$c, $d) {
	$a = 234;
	$b = 345;
	$c .= '456';
	echo $d;
}

test($a, $a);

class A {
	private $data;

	public function A_F($a) {
		$this->data = $a;
		echo $a;
	}
}

$newObj = new A();
$newObj->A_F($a);

$newObj1 = new A();
$newObj1->A_F($a);

?>
