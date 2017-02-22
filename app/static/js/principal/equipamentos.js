/*
################################################################################
## SIE - UFC 
################################################################################
## Javascript Página de Equipamentos - Blueprint Principal
################################################################################
*/


// Mapa de Equipamentos

var mapa_equip = L.map('map').setView([-3.745376, -38.575800], 14)

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, \
							 <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, \
				  		 Imagery © <a href="http://mapbox.com">Mapbox</a>',
	maxZoom: 18,
	id: 'mapbox.streets',
	accessToken: 'pk.eyJ1IjoibHVjYXNzbSIsImEiOiJjaW05cDlmMXYwMDFidzhtM3JzN291dzZqIn0.WC0WGjp2FzN0VNOZ3JHjnQ'

}).addTo(mapa_equip);

var layers = {

};

L.control.layers(null, layers).addTo(mapa_equip);