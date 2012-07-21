<?php
    if ($_POST["url"]) {
        $ch = curl_init();
	curl_setopt_array(
		$ch,
		array(
			CURLOPT_URL => $_POST["url"]
		)	
	);
	$content=curl_exec($ch);
	if(curl_errno($ch)) 
            echo curl_error($ch);
	else 
            echo $content;
	curl_close($ch);       
    } else {
    	echo "Http Agent!";
    }
	
?>