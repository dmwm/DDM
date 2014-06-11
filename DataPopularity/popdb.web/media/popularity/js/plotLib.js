//functions that creates the on demand flot plots

function datasetplot_init(){
	alreadyFetched = {};
	data = []
	placeholder = $("#placeholder");
	options = {
		legend : {show: true, container: $("#plotLegend")},
	        lines: { show: true },
     		points: { show: true },
       		 /*xaxis: { tickDecimals: 0, tickSize: 1 }*/
		xaxis: {mode: "time" ,timeformat: "%b/%d"}
    		};
 	$("#select_popIdx").val(1);
}	

function datasetplot_getdata(url){

	var apiUrl = url+"?";
	var popIdx = $("#select_popIdx").val();	
	var timeAggr= $("#select_timeAggr").val();
		
	apiUrl = apiUrl + "aggr=" + timeAggr + "&n=" + popIdx 		

	var startDate=$("#startDate").val();
	if (startDate != '') {apiUrl=apiUrl+"&tstart="+startDate;}
	var endDate=$("#endDate").val();
	if (endDate !='') {apiUrl=apiUrl+"&tstop="+endDate; }

	/*alert(apiUrl)*/

        // then fetch the data with jQuery
        function onDataReceived(series) {
            // extract the first coordinate pair so you can see that
            // data is now an ordinary Javascript object

            // let's add it to our current data
            if (!alreadyFetched[series.label]) {
                alreadyFetched[series.label] = true;
                data.push(series);
            }
            // and plot all we got
            $.plot(placeholder, data, options);
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
    };


function datasetplot (url) {
    
	datasetplot_init();
	datasetplot_getdata(url);
      
};

/*----------------------------------------------------*/

function trendplot_init(){
	alreadyFetched = {};
	data = []
	placeholder = $("#placeholder");
	options = {
		legend : {show: true, container: $("#plotLegend")},
	        lines: { show: true },
     		points: { show: true },
       		 /*xaxis: { tickDecimals: 0, tickSize: 1 }*/
		xaxis: {mode: "time" ,timeformat: "%b/%d"}
    		};
 	$("#select_popIdx").val(1);
}	

function trendplot_getdata(url){

	var apiUrl = url+"?n=1";
	// fetch one series, adding to what we got
	//if (plotDS==1){ apiUrl="http://cms-popularity.cern.ch/popdb/PlotDS/?n=1"}
	//else{ apiUrl="http://cms-popularity.cern.ch/popdb/PlotDataTier/?n=1"}


	var popIdx = $("#select_popIdx").val() -1 ;	
	var timeAggr= $("#select_timeAggr").val();
		
	apiUrl = apiUrl + "&aggr=" + timeAggr 

	var startDate=$("#startDate").val();
	if (startDate != '') {apiUrl=apiUrl+"&tstart="+startDate;}
	var endDate=$("#endDate").val();
	if (endDate !='') {apiUrl=apiUrl+"&tstop="+endDate; }

	alert(apiUrl)

        // then fetch the data with jQuery
        function onDataReceived(series) {
            // extract the first coordinate pair so you can see that
            // data is now an ordinary Javascript object

		alert(series)
		  // hard-code color indices to prevent them from shifting as
    		// countries are turned on/off
    		var i = 0;
    		$.each(series, function(key, val) {
        		val.color = i;
        		++i;
    		});


	    // insert checkboxes 
    	var choiceContainer = $("#choices");
    	$.each(series, function(key, val) {
        choiceContainer.append('<br/><input type="checkbox" name="' + key +
                               '" checked="checked" id="id' + key + '">' +
                               '<label for="id' + key + '">'
                                + val.label + '</label>');
    });
    choiceContainer.find("input").click(plotAccordingToChoices);

   function plotAccordingToChoices() {
        	 data = [];

        choiceContainer.find("input:checked").each(function () {
            var key = $(this).attr("name");
            if (key && datasets[key])
                data.push(datasets[key]);
        });

        if (data.length > 0)
            $.plot($("#placeholder"), data, {
                yaxis: { min: 0 },
                xaxis: { tickDecimals: 0 }
            });
    }


            // let's add it to our current data
            if (!alreadyFetched[series.label]) {
                alreadyFetched[series.label] = true;
                data.push(series);
            }
            // and plot all we got
		$.plot("#placeholder", data, options);	 
	}	
        
        $.ajax({
            url: apiUrl,
            method: 'GET',
            dataType: 'json',
            success: onDataReceived,
            "statusCode": {
                        400: function() {
                        alert('BAD REQUEST\ncould not load data\nplease check input values');
                        }       
                        }
        });
    };


function trendplot (url) {
    
	trendplot_init();
	trendplot_getdata(url);
      
};

