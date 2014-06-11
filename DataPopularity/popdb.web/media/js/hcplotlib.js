var chart;
/*default legend line height*/
var legendlineheight = 16;
var chartheight = 400;
var chartwidth = 900;
var charts = {};

var subtitle ='Select an area by dragging across the lower chart';


function requestData(apiUrl,theInfo) {
      
        function onDataReceived(series){
		plotTimeChart(series,theInfo);
        }
	
	//alert(apiUrl)

        $.ajax({
            url: apiUrl,
            method: 'GET',
            dataType: 'json',
            success: onDataReceived,
            "statusCode": {
                        400: function(xhr,err) {
                        alert('BAD REQUEST: \n'+xhr.responseText);
                        $('#'+theInfo.placeholder)
                        .html('<p class="errors">BAD REQUEST<br/>'+xhr.responseText);
                        },
                        500: function() {
                        alert('INTERNAL SERVER ERROR\ncould not load data\n');
                        $('#'+theInfo.placeholder)
                        .html('<p class="errors">INTERNAL SERVER ERROR<br/>could not load data<br/>');
                        }
                        }
        });
        // Modify the link for the "getJSON" button on the plot page
        setJSONurl(apiUrl);
}


function getData(apiUrl){

            var result = $.ajax({
            url: apiUrl,
            method: 'GET',
            dataType: 'json',
            async: false,
            success: function(data){
                     return data;
                           },
            "statusCode": {
                        400: function(xhr,err) {
                        alert('BAD REQUEST: \n'+xhr.responseText);
                        $('#placeholder')
                        .html('<p class="errors">BAD REQUEST<br/>'+xhr.responseText);
                        },
                        500: function() {
                        alert('INTERNAL SERVER ERROR\ncould not load data\n');
                        $('#placeholder')
                        .html('<p class="errors">INTERNAL SERVER ERROR<br/>could not load data<br/>');
                        }
                        }
        });
        return result;
}

function plotTimeChart(jsonresult,theInfo) {
   
        var $container = $('#'+theInfo.placeholder)
        .css({position: 'relative', height: 380+(legendlineheight*jsonresult["data"].length)});

	var detailcontainer = 'detailcontainer'+theInfo.placeholder	
	var mastercontainer = 'mastercontainer'+theInfo.placeholder	

	$('#'+detailcontainer).remove();
	$('#'+mastercontainer).remove();

   	var $detailContainer = $('<div id="'+ detailcontainer + '">')
      	.css({ position: 'absolute', width: '100%' })
      	.appendTo($container);

   	var $masterContainer = $('<div id="'+ mastercontainer + '">')
      	.css({ position: 'absolute', top: 300+(legendlineheight*jsonresult["data"].length), width: '100%' })
      	.appendTo($container);

   	jsonseries = [];
   	for (s=0; s < jsonresult["data"].length; s++){
        jsonseries.push(jsonresult["data"][s]);
   	}
   	// create master and in its callback, create the detail chart


	var masterChart;

	return createMaster(jsonresult,theInfo, masterChart);
}


function additemtotimeplot(name, url, theInfo){
        /*
        if (items.indexOf(name) != -1){
                //alert("item already added to chart");
                return;
        }
        */

        //apiUrl = buildUrl(url);
        apiUrl = url + "&name=" + name;
        //var serie = getData(apiUrl);
        //jsondata = jQuery.parseJSON(serie["responseText"]);
        if (charts[theInfo.placeholder] == null ){
		var serie = getData(apiUrl);
        	jsondata = jQuery.parseJSON(serie["responseText"]);

                //console.log(jsondata["data"]);
		var masterChart = plotTimeChart(jsondata, theInfo);
		//console.log(masterChart);
                charts[""+theInfo.placeholder] = masterChart;
		//console.log(charts);
        }else{
		masterChart = charts[theInfo.placeholder];
		if ($.inArray(name, masterChart.series.map(function(element) {return element.name;})) != -1)
		{
			return;
		}
                var serie = getData(apiUrl);
        	jsondata = jQuery.parseJSON(serie["responseText"]);

                toadd = jsondata["data"];
                newserie = { "data": toadd["data"],
                             "name": toadd["name"]
                           }
                //console.log(toadd[0]);
                masterChart.addSeries(toadd[0]);
                //series = masterChart.series;
                //series.push(toadd[0]);
                //jsondata["data"] = series;
                //console.log(jsondata);
                //plotTimeChart(jsondata);

        var detailcontainer = 'detailcontainer'+theInfo.placeholder
        var mastercontainer = 'mastercontainer'+theInfo.placeholder

        var $container = $('#'+theInfo.placeholder)
        .css({position: 'relative', height: 380+(legendlineheight*masterChart.series.length)});

        var $masterContainer = $('<div id="'+ mastercontainer + '">')
	.css({ position: 'absolute', top: 300+(legendlineheight*masterChart.series.length), width: '100%' });

                masterChart.redraw();
                createDetail(masterChart, jsondata, theInfo);

        }

}


function updateplot(url, theInfo){
        //apiUrl = buildUrl(url);
        var series = [];
        var jsondata;
        var items = [];
	masterChart = charts[theInfo.placeholder];
	items = masterChart.series.map(function(element) {return element.name;})
        for (i = 0; i<items.length; i++){
                var serie = getData(url+ "&name=" +items[i]);
                jsondata = jQuery.parseJSON(serie["responseText"]);
                //jsonserie = jsondata["data"];
                //console.log(jsondata["data"][0]);
                series.push(jsondata["data"][0]);
        }
        jsondata["data"] = series;
        plotTimeChart(jsondata, theInfo);
}

function cleartimeplot(theInfo){
        masterChart = charts[theInfo.placeholder];
	//console.log(charts);
	masterChart.detailChart.destroy();;
        masterChart.destroy();
	delete charts[theInfo.placeholder];
}

 
           

   // create the master chart
function createMaster(jsonresult,theInfo, masterChart) {
      masterChart = new Highcharts.Chart({
         chart: {
            renderTo: 'mastercontainer'+theInfo.placeholder,
            reflow: true,
            height: 80,
            borderWidth: 0,
            backgroundColor: null,
            marginLeft: 70,
            marginRight: 20,
            zoomType: 'x', 
	   events: {
               
               // listen to the selection event on the master chart to update the 
               // extremes of the detail chart
               selection: function(event){
                  var extremesObject = event.xAxis[0],
                     min = extremesObject.min-(extremesObject.min%(3600000*24)),
                     max = extremesObject.max-(extremesObject.max%(3600000*24)),
                     xAxis = this.xAxis[0];
                  
                  // reverse engineer the last part of the data
                  for(s=0; s<this.series.length; s++){
                  detailData = [];
                  // add a zero valued point at the beginning to draw the series even with no data in the interval
                  if(this.series[s].data[0].x > min){
                     detailData.push({
                           x: min,
                           y: 0
                        });

                     if(this.series[s].data[0].x < max){
                        detailData.push({
                           x: this.series[s].data[0].x,
                           y: 0
                        });
                     }
                  }
                  // add points in the interval to the detailed chart serie
                  jQuery.each(this.series[s].data, function(i, point) {
                     if (point.x >= min && point.x <= max) {
                        detailData.push({
                           x: point.x,
                           y: point.y
                        });
                     }
                  });
                  // add a zero valued point at the end to draw the series even with no data in the interval
                  if(this.series[s].data[(this.series[s].data.length-1)].x < max){
                     if(this.series[s].data[(this.series[s].data.length-1)].x > min){
                        detailData.push({
                           x: this.series[s].data[(this.series[s].data.length-1)].x,
                           y: 0
                        });
                     }
                     detailData.push({
                           x: max,
                           y: 0
                        });
                  }
                  //console.log(detailData)
                  
		  this.detailChart.series[s].setData(detailData);
		  }
                  

                  // move the plot bands to reflect the new detail span
                  xAxis.removePlotBand('mask-before');
                  xAxis.addPlotBand({
                     id: 'mask-before',
                     from: min,
                     to: max,
                     color: Highcharts.theme.maskColor || 'rgba(255, 255, 102, 1.0)'
                  });


                  return false;
               }


		}
         },
         title: {
            text: null
         },
         xAxis: {
            type: 'datetime',
/*
            showLastTickLabel: true,
*/
            maxZoom: 3600000, // 1 hour
            plotBands: [{
               id: 'mask-before',
               from: Date.UTC(jsonresult["tstart"].split("-")[0], (jsonresult["tstart"].split("-")[1])-1, jsonresult["tstart"].split("-")[2]),
               to: Date.UTC(jsonresult["tstop"].split("-")[0], (jsonresult["tstop"].split("-")[1])-1, jsonresult["tstop"].split("-")[2]),
               color: Highcharts.theme.maskColor || 'rgba(255, 255, 102, 1.0)'
            }],
            title: {
               text: null
            }
         },
         yAxis: {
            gridLineWidth: 0,
            labels: {
               enabled: false
            },
            title: {
               text: null
            },
            min: 0.6,
            showFirstLabel: false
         },
         tooltip: {
            formatter: function() {
               return false;
            }
         },
         legend: {
            enabled: false
         },

      credits:  {
         enabled:true,
         text: theInfo.credits+" " +theInfo.today,
         position:{align:"right",x:-10,verticalAlign:"bottom",y:0},
         style:{cursor:"pointer",color:"#909090",fontSize:"10px"}
      },

         plotOptions: {
            series: {
               fillColor: {
                  linearGradient: [0, 0, 0, 70],
                  stops: [
                     [0, highchartsOptions.colors[0]],
                     [1, 'rgba(0,0,0,0)']
                  ]
               },
               lineWidth: 1,
               marker: {
                  enabled: false
               },
               shadow: false,
               states: {
                  hover: {
                     lineWidth: 1                  
                  }
               },
               enableMouseTracking: false
            }
         },
      

	series: jsonresult["data"],
  
         exporting: {
            enabled: false
         }
      
      }, function(masterChart) {

         createDetail(masterChart, jsonresult,theInfo)
      });

      return masterChart;
}
   

   // create the detail chart
function createDetail(masterChart, jsonresult,theInfo) {
      // prepare the detail chart
      var detailData = [],
         detailStart = Date.UTC(jsonresult["tstart"].split("-")[0], (jsonresult["tstart"].split("-")[1])-1, jsonresult["tstart"].split("-")[2]),
         detailStop = Date.UTC(jsonresult["tstop"].split("-")[0], (jsonresult["tstop"].split("-")[1])-1, jsonresult["tstop"].split("-")[2]);
      
      for (s=0; s<masterChart.series.length; s++){
      detailserie = {};
      detailserie.data = [];
      detailserie.name = masterChart.series[s].name;   
      jQuery.each(masterChart.series[s].data, function(i, point) {
         if (point.x >= detailStart && point.x <= detailStop) {
            detailserie.data.push(
            {
            x: point.x,
            y: point.y
            }
            );
         }
      });
      detailData.push(detailserie);
      //console.log(detailData)
      }
      
      // create a detail chart referenced by a global variable
      masterChart.detailChart = new Highcharts.Chart({
         chart: {
            plotBorderWidth: 0,
            marginBottom: 120,
            renderTo: 'detailcontainer'+theInfo.placeholder,
            height: chartheight+(16*(detailData.length)),
            marginLeft: 70,
            marginRight: 20,
            zoomType: 'y',
            type: 'line',
/*
            height: chartheight,
            width: chartwidth,
*/
            style: {
               position: 'absolute'
            }
         },
         credits: {
            enabled: false
         },
         title: {
            text: theInfo.htitle
         },
         subtitle: {
            text: subtitle
         },

      xAxis: {
         type: 'datetime',
         maxZoom: 3600000, // 1 hour
      },

      yAxis: {
         title: {
            style: {
                fontSize: '150%'
                },
            text: theInfo.ytitle
         },
         min: 0
      },

      tooltip: {
         formatter: function() {
             return '<b>'+  Highcharts.dateFormat('%b %e %Y %H:%M', this.x) +'</b><br/>'+this.series.name +' : ' + this.y;
         }
      },

/*
      legend: {
        //layout: 'vertical',
        align: 'center',
        borderWidth: 1,
        verticalAlign: 'top',
        floating: false,
        y: 35,
      },
*/

      legend: {
        layout: 'vertical',
        align: 'center',
        borderWidth: 0,
        verticalAlign: 'top',
        floating: false,
        y: 35,
        labelFormatter: function() {
            return (this.index+1) +' - '+ this.name;
        },
      },


         plotOptions: {
            series: {
               marker: {
                  enabled: false,
                  states: {
                     hover: {
                        enabled: true,
                        radius: 3
                     }
                  }
               }
            }
         },
         
         exporting: {
            enabled: true
         }
      
      });
   for (s=0; s<detailData.length; s++){
      masterChart.detailChart.addSeries(
      {
      name: detailData[s].name,
      data: []
      }
      );
      masterChart.detailChart.series[s].setData(detailData[s].data,false);
      /*
      if (s > 0){
      detailChart.series[s].hide();
      }
       */
   }
   masterChart.detailChart.redraw();
}
