//General Alert
function genalert(alertvalue)
{
var agree=confirm(alertvalue);
if (agree)
	return true ;
else
	return false ;
}

function addimage(iid,furl) {
	document.getElementById('images').value += iid + ',';
	document.getElementById('rimages').innerHTML += ('<div class="preview" id="' + iid + '"><a href="#" onclick="return removeimage("' + iid + '");"><img src="' + furl + '=s80-c" width="80" height="80" style="display: visible;" /></a></div>')
	return false;
}

function removeimage(iid) {
	var curimg = document.getElementById('images').value;
	newimg = curimg.replace(iid + ',','');
	document.getElementById('images').value = newimg;
	document.getElementById(iid).style.display = 'none';
	return false;
}