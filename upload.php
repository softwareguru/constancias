<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>Importar constancias para generar</title>
<style type="text/css">
body {
    background: #E3F4FC;
    color: #2b2b2b;
    font-family: Helvetica, Arial, sans-serif;
}
a {
	color:#898989;
	font-size:14px;
	font-weight:bold;
	text-decoration:none;
}
a:hover {
	color:#CC0033;
}

h1 {
    text-align: center;
}
#container {
	background: #CCC;
}
#form 			{padding: 10px;}
#form input     {margin-bottom: 20px;}
</style>
</head>
<body>
<h1>Importar lista para generar constancias</h1>

<p>Formato: template_id, nombre de participante, email, evento[/sede]</p>

Ej:
<pre>
 7	Fernando Hernández 	fernando@sg.com.mx 	sgvirtual
 7	Pedro Galván Kondo	pedrogk@gmail.com 	sgvirtual7/uabc
</pre>

<div id="container">
  <div id="form">

<?php
require_once('constants.php');
$db = new PDO("mysql:host=".DBHOST.";dbname=".DBNAME, DBUSER, DBPASS, array(PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES utf8"));

if (isset($_POST['submit'])) {
  if (is_uploaded_file($_FILES['filename']['tmp_name'])) {
    echo "<h2>" . "Archivo ". $_FILES['filename']['name'] ." subido exitosamente." . "</h2>";
    $handle = fopen($_FILES['filename']['tmp_name'], "r");

    $import = "INSERT into constancias_generar (template_id, nombre_participante, email, tag) VALUES \n";
    while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
      if(is_numeric($data[0])) {
        $import .= "( $data[0],'$data[1]','$data[2]','$data[3]'),\n";
      } // if
    } // while
    $import = chop($import, ",\n");
//    print "<pre>$import</pre>"; // Si quieres debuggear el query string.
    $db->exec($import);
    print "<p>Insert exitoso</p>";
    fclose($handle);
  } // if
} else {
    print "<form enctype='multipart/form-data' action='upload.php' method='post'>";
    print "<p>Nombre del archivo a importar <br />";
    print "<span style='font-size: 0.9em; font-style: italic;'>(usar archivo csv, separado por comas)</span>:</p>";
    print "<input size='50' type='file' name='filename'><br />\n";
    print "<input type='submit' name='submit' value='Upload'></form>";
}
?>

  </div>
</div>
</body>
</html>

