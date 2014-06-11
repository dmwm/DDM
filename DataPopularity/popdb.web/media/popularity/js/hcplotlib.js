var chart;
/*default legend line height*/
var legendlineheight = 16;
var chartheight = 400;
var chartwidth = 900;


function buildUrl(url){

	var apiUrl = url+"?";
        var popIdx = $("#select_popIdx").val();
        var timeAggr = $("#select_timeAggr").val();
        var siteName = $("#select_siteName").val();

        apiUrl = apiUrl + "aggr=" + timeAggr + "&n=" + popIdx
        if (siteName != "all"){apiUrl = apiUrl+"&sitename=" + siteName }
        var startDate=$("#startDate").val();
        if (startDate != '') {apiUrl=apiUrl+"&tstart="+startDate;}
        var endDate=$("#endDate").val();
        if (endDate !='') {apiUrl=apiUrl+"&tstop="+endDate; }

        var metric = $("#select_metric").val();
        if (metric == "tot_cpu_time") {apiUrl = apiUrl+ "&orderby=totcpu"}
        else if (metric == "n_access" ) {apiUrl = apiUrl+ "&orderby=naccess"}
        else if (metric == "n_users_per_day") {apiUrl = apiUrl+ "&orderby=nusers"}
        yaxisname = metric;

        return apiUrl;

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




function requestData(url) {
        var apiUrl = url+"?";
        var popIdx = $("#select_popIdx").val();
        var timeAggr = $("#select_timeAggr").val();
        var siteName = $("#select_siteName").val();

        apiUrl = apiUrl + "aggr=" + timeAggr + "&n=" + popIdx + "&orderby="+ metric 
        if (siteName != "all"){apiUrl = apiUrl+"&sitename=" + siteName }
        var startDate=$("#startDate").val();
        if (startDate != '') {apiUrl=apiUrl+"&tstart="+startDate;}
        var endDate=$("#endDate").val();
        if (endDate !='') {apiUrl=apiUrl+"&tstop="+endDate; }

        var metric = $("#select_metric").val();
        if (metric == "tot_cpu_time") {apiUrl = apiUrl+ "&orderby=totcpu"}
        else if (metric == "n_access" ) {apiUrl = apiUrl+ "&orderby=naccess"}
        else if (metric == "n_users_per_day") {apiUrl = apiUrl+ "&orderby=nusers"}
        yaxisname = metric;

        function onDataReceived(series){
		plotTimeChart(series);
        }

        $.ajax({
            url: apiUrl,
            method: 'GET',
            dataType: 'json',
            success: onDataReceived,
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
        // Modify the link for the "getJSON" button on the plot page
        setJSONurl(apiUrl);
}


var masterChart,
    detailChart;
var items = [];
var title = "Time Evolution",
    subtitle,
    credits = "CMS Popularity Service",
    yaxisname = "";
var metric_labels = {};
metric_labels["tot_cpu_time"] = "CPU time [h]";
metric_labels["n_access"] = "number of access";
metric_labels["n_users_per_day"] = "users per day";

function hctimeplot(url, info) {

        title = info.datatype+" Time Evolution";
        credits = "CMS Popularity Service "+info.today;

        requestData(url);

};

function hctimeplot2(info){

	//apiUrl = buildUrl(url);
        //jdata = getData();
        plotTimeChart({"data": []}); 

}

function additemtotimeplot(name, url){
        if (items.indexOf(name) != -1){
                //alert("item already added to chart");
                return;
        }
	apiUrl = buildUrl(url);
        apiUrl = apiUrl + "&name=" + name;
	var serie = getData(apiUrl);
	jsondata = jQuery.parseJSON(serie["responseText"]);
        if (items.length == 0){
		console.log(jsondata["data"]);
		plotTimeChart(jsondata);
	}else{
		toadd = jsondata["data"];
		newserie = { "data": toadd["data"],
			     "name": toadd["name"]
			   }
		console.log(toadd[0]);
		masterChart.addSeries(toadd[0]);
		//series = masterChart.series;
		//series.push(toadd[0]);
		//jsondata["data"] = series;
		//console.log(jsondata);
		//plotTimeChart(jsondata);

        $('#placeholder').css({position: 'relative', height: 380+(legendlineheight*masterChart.series.length)});

        $('#master-container').css({ position: 'absolute', top: 300+(legendlineheight*masterChart.series.length), width: '100%' })

        	masterChart.redraw();
        	createDetail(masterChart, jsondata);

	}
	items.push(name);

}

function updateplot(url){

	apiUrl = buildUrl(url);
	var series = [];
	var jsondata;
	for (i = 0; i<items.length; i++){
		var serie = getData(apiUrl+ "&name=" +items[i]);
                jsondata = jQuery.parseJSON(serie["responseText"]);
		//jsonserie = jsondata["data"];
		console.log(jsondata["data"][0]);
		series.push(jsondata["data"][0]);
	}
	jsondata["data"] = series;
	plotTimeChart(jsondata);
}

function cleartimeplot(){
	items = [];	
        
	masterChart.destroy();
        detailChart.destroy();
}
   
function plotTimeChart(jsonresult) {
   
        var $container = $('#placeholder')
        .css({position: 'relative', height: 380+(legendlineheight*jsonresult["data"].length)});

	$('#detail-container').remove();
	$('#master-container').remove();

   	var $detailContainer = $('<div id="detail-container">')
      	.css({ position: 'absolute', width: '100%' })
      	.appendTo($container);

   	var $masterContainer = $('<div id="master-container">')
      	.css({ position: 'absolute', top: 300+(legendlineheight*jsonresult["data"].length), width: '100%' })
      	.appendTo($container);

   	jsonseries = [];
   	for (s=0; s < jsonresult["data"].length; s++){
        jsonseries.push(jsonresult["data"][s]);
   	}
   	// create master and in its callback, create the detail chart
   	createMaster(jsonresult);

} 
   // create the master chart
function createMaster(jsonresult) {
      masterChart = new Highcharts.Chart({
         chart: {
            renderTo: 'master-container',
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
               selection: function(event) {
                  var extremesObject = event.xAxis[0],
                     min = extremesObject.min-(extremesObject.min%(3600000*24)),
                     max = extremesObject.max-(extremesObject.max%(3600000*24)),
                     xAxis = this.xAxis[0];
                  
                  // reverse engineer the last part of the data
                  for(s=0; s<this.series.length; s++){
                  detailData = [];
                  // add a zero valued point at the beginning to draw the series even with no data in the interval
                  if(this.series[s].data[0].x > min){
                     if(this.series[s].data[0].x < max){
                        detailData.push({
                           x: this.series[s].data[0].x,
                           y: 0
                        });
                     }
                     detailData.push({
                           x: min,
                           y: 0
                        });
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
                  
		  detailChart.series[s].setData(detailData);
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
         text: credits,
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

         createDetail(masterChart, jsonresult)
      });

   

}
   
   // create the detail chart
function createDetail(masterChart, jsonresult) {
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
      }
      
      // create a detail chart referenced by a global variable
      detailChart = new Highcharts.Chart({
         chart: {
            plotBorderWidth: 0,
            marginBottom: 120,
            renderTo: 'detail-container',
            height: chartheight+(16*(detailData.length)),
            marginLeft: 70,
            marginRight: 20,
            zoomType: 'y',

            defaultSeriesType: 'line',
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
            text: title
         },
         subtitle: {
            text: 'Select an area by dragging across the lower chart'
         },

/*
         xAxis: {
            type: 'datetime'
         },
*/
      xAxis: {
         type: 'datetime',
         maxZoom: 3600000, // 1 hour
         /*dateTimeLabelFormats: {
            month: '%e. %b',
            year: '%b'
         }*/
      },
/*
         yAxis: {
            title: null,
            maxZoom: 0.1
         },
*/
      yAxis: {
         title: {
            style: {
                fontSize: '150%'
                },
            text: metric_labels[yaxisname]
         },
         min: 0
      },

      tooltip: {
         formatter: function() {
             return '<b>'+  Highcharts.dateFormat('%B %e %Y', this.x) +'</b><br/>'+this.series.name +'<br/>'+ this.y+' '+ metric_labels[yaxisname];
         }
      },

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
      detailChart.addSeries(
      {
      name: detailData[s].name,
      data: []
      }
      );
      detailChart.series[s].setData(detailData[s].data, false);
      //if (s > 0){
      //detailChart.series[s].hide();
      //}
   }
   detailChart.redraw();
}
