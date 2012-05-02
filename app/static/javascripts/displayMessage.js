function displayMessage(str)
{
	// Using pure JavaScript to create and style a div element

	var d = document.createElement('div');

	with(d.style)
	{
		// Applying styles:

		position='fixed';
		width = '350px';
		height = '20px';
		top = '50%';
		left = '50%';
		margin = '-30px 0 0 -195px';
		backgroundColor = '#f7f7f7';
		border = '1px solid #ccc';
		color = '#777';
		padding = '20px';
		fontSize = '18px';
		fontFamily = '"Myriad Pro",Arial,Helvetica,sans-serif';
		textAlign = 'center';
		zIndex = 100000;

		textShadow = '1px 1px 0 white';

		MozBorderRadius = "12px";
		webkitBorderRadius = "12px";
		borderRadius = "12px";

		MozBoxShadow = '0 0 6px #ccc';
		webkitBoxShadow = '0 0 6px #ccc';
		boxShadow = '0 0 6px #ccc';
	}

	d.setAttribute('onclick','document.body.removeChild(this)');

    // Adding the message passed to the function as text:
	d.appendChild(document.createTextNode(str));

    // Appending the div to document
	document.body.appendChild(d);

    // The message will auto-hide in 3 seconds:

	setTimeout(function(){
		try{
			document.body.removeChild(d);
		}	catch(error){}
	},3000);
}