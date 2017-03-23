<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
        <meta charset="UTF-8">
	<title>Sirtfi Dashboard</title>
	
	<!-- Bootstrap Css --!>
	<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
	<!--Boostrap Css Overrides -->
	<link rel="stylesheet" type="text/css" href="css/style.css">
	<!-- Latest compiled JavaScript -->
	<script src="https:///maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
	<!-- JQuery -->
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
	<!-- Datatables styling sheets -->
	<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.12/css/jquery.dataTables.min.css"/>
	<!-- Datatables js -->
	<script type="text/javascript" src="https://cdn.datatables.net/v/dt/jq-2.2.3/dt-1.10.12/datatables.min.js"></script>
	<script type="text/javascript" src="https://cdn.datatables.net/1.10.12/js/jquery.dataTables.min.js"></script>
        <!-- Store SP as javascript variable if recognised (must manually update this table) -->	
        <script>
	var sp = "<?php 
            if (in_array(strtoupper(htmlspecialchars($_GET['sp'])), array("CERN"))) {
                echo strtoupper($_GET['sp']);
            } else {
                echo "a Service Provider in eduGAIN";
            }
        ?>";
        </script>

</head>

<body >
	
<!-- Nav bar -->
<div class="row">
	<div class="col-md-12">
		<nav class="navbar navbar-default" style="border-color:#FFC277;background-color:#FFC277">
			<div class="container-fluid">
				<div class="navbar-header">
					<a class="navbar-brand" href="http://sirtfi.cern.ch/index.php">Sirtfi Dashboard</a>
				</div>
				<ul class="nav navbar-nav navbar-right">
					<li><a href="/sirtfi-metadata.xml" data-toggle="modal">Metadata</a></li>
				</ul>
			</div>
		</nav>
	</div>
</div>
<div class="container">
<div class="row">
	<div class="col-md-1"> </div>
	<div class="col-md-8">
		<h2>The Security Incident Response Trust Framework for Federated Identity</h2>
		<?php if (isset($_GET['sp'])) {
 		   echo "<p>You need Sirtfi to access ";
		   echo strtoupper(htmlspecialchars($_GET['sp'],ENT_QUOTES, 'UTF-8'));
		   echo "! Look for your home organisation below and click to email them a request.</p>";
		}else{
		   echo "<p>Do you need Sirtfi to access a service? Look for your home organisation below and click to email them a request.</p>";
		} ?>
                <p>Want more information? Visit the <a href="https://refeds.org/sirtfi">Sirtfi Homepage</a>.</p>
	</div>
	<div class="col-md-1">
		<img src="/sirtfi-logo.png" class="img-rounded" alt="Sirtfi Logo"  width="152" height="118">
	</div>
	<div class="col-md-1"> </div>
</div>
<hr>
<div class="row">
	<div class="col-md-1"> </div>
	<div class="col-md-10">
		<table id="example" class="display" width="100%"></table>
	</div>
	<div class="col-md-1"> </div>
</div>
<div class="row">
        <div class="col-md-1"> </div>
        <div class="col-md-10" style="color:#FFC277">
        <b>
	<?php
            include 'table.txt.php';
	?>  
        </b>   
        </div>
        <div class="col-md-1"> </div>
</div>
</div>

<script>
var dataSet = [
	<?php $idps = file_get_contents('table.txt'); echo $idps  ?>
];

$(document).ready(function() {
	$('#example').DataTable( {
		data: dataSet,
		columns: [
			{ title: "Name" },
			{ title: "Sirtfi?" },
			{ title: "Contact" },
		],
                columnDefs: [
                        { "targets": [ 1 ],
                          "createdCell": function (td, cellData, rowData, row, col) {
                                  if ( cellData == "True" ) {
                                    $(td).css('color', 'green')
                                  } else {
                                    $(td).css('color', 'red')
                                  }
                          } 
                        },
                        { "targets": [ 2 ],
                          "visible": false 
                        },
                ],
	} );

	var table = $('#example').DataTable();
        $('#example tbody').on('click', 'tr', function () {
            var data = table.row( this ).data();
            var msg = "";
            
            if ( data[1] == "False" ){
            	msg = "Hello,%0A%0A I am having trouble accessing "+sp+","+
                   " because my Identity Provider, '"+data[0]+
		   "', is not compliant with the Sirtfi Framework."+
        	   "%0A%0A You can find more details at https://wiki.refeds.org/display/SIRTFI/Guide+for+Federation+Participants."+
                   " %0A%0A Please could you help me?";
            } else {
            	msg = "Hello,%0A%0A I am having trouble accessing "+sp+","+
                   " from my Identity Provider, '"+data[0]+"'."+
                   " %0A%0A Please could you help me?";
            }
		msg += "%0A%0A-----------------------------" +
			"%0A%0A This message was sent using sirtfi.cern.ch"
	    window.open('mailto:'+data[2]+'?subject=Attribute%20Release%20Problem&body='+msg);

        } );
} );

</script>

</body>

</html>
