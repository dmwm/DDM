var chart;
/*default legend line height*/
var legendlineheight = 16;
var chartheight = 400;
var chartwidth = 900;

var subtitle ='';

var detailChart;

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

function plotTimeChart(jsonresult,theInfo) {
   
        var $container = $('#'+theInfo.placeholder)
        .css({position: 'relative', height: 380+(legendlineheight*jsonresult["data"].length)});

	var detailcontainer = 'detailcontainer'+theInfo.placeholder	

	$('#'+detailcontainer).remove();

   	var $detailContainer = $('<div id="'+ detailcontainer + '">')
      	.css({ position: 'absolute', width: '100%' })
      	.appendTo($container);


   	createDetail(jsonresult,theInfo);

} 
           

   

   // create the detail chart
function createDetail(jsonresult,theInfo) {
      // prepare the detail chart

      // create a detail chart referenced by a global variable
      detailChart = new Highcharts.StockChart({
		    chart: {
		        renderTo: 'detailcontainer'+theInfo.placeholder,
		        type: 'line',
            		zoomType: '',
		    },
		    credits:  {
		         enabled:true,
         		 text: theInfo.credits+" " +theInfo.today,
		         position:{align:"right",x:-10,verticalAlign:"bottom",y:0},
		         style:{cursor:"pointer",color:"#909090",fontSize:"10px"}
		      },


		    rangeSelector: {
		        selected: 1
		    },

		    title: {
		        text: theInfo.htitle
		    },
	           subtitle: {
        	    text: subtitle
         	    },

	plotOptions :{
		line : {
			gapSize : 1,
			},
	},	

      xAxis: {
         type: 'datetime',
         minRange: 5*3600000, // 1 hour
      },

      yAxis: {
            lineWidth: 2,
            offset: 0,
            labels: {
                align: 'right',
                x: -3,
                y: 6
            },
            showLastLabel: true,         
	title: {
            style: {
                fontSize: '150%'
                },
            text: theInfo.ytitle
         },
         min: 0,
      },
      legend: {
	enabled : true,
        //layout: 'vertical',
        align: 'center',
        borderWidth: 1,
        verticalAlign: 'top',
        floating: false,
        y: 35,
      },
      rangeSelector:{

	buttons: [
			{
				type: 'week',
				count: 1,
				text: '1w'
			},{
				type: 'month',
				count: 1,
				text: '1m'
			}, {
				type: 'month',
				count: 3,
				text: '3m'
			}, {
				type: 'month',
				count: 6,
				text: '6m'
			}, {
				type: 'ytd',
				text: 'YTD'
			}, {
				type: 'year',
				count: 1,
				text: '1y'
			}, {
				type: 'all',
				text: 'All'
			}]
		},


	        series: jsonresult["data"],	
		}
	);

}
