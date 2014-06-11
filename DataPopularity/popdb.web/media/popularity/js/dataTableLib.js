function fnGetSelected( oTableLocal )
{
    var aReturn = new Array();
    var aTrs = oTableLocal.fnGetNodes();
     
    for ( var i=0 ; i<aTrs.length ; i++ )
    {
        if ( $(aTrs[i]).hasClass('row_selected') )
        {
            aReturn.push( aTrs[i] );
        }
    }
    return aReturn;
}


function setColFilter(oTable) {
        var asInitVals = new Array();
	$("tfoot input").keyup( function () {
		/* Filter on the column (the index) of this element */
		oTable.fnFilter( this.value, $("tfoot input").index(this) );
	} );
	
	
	/*
	 * Support functions to provide a little bit of 'user friendlyness' to the textboxes in 
	 * the footer
	 */
	/*
        $("thead input").each( function (i) {
                asInitVals[i] = this.value;
        } );

        $("thead input").focus( function () {
                if ( this.className == "search_init" )
                {
                        this.className = "";
                        this.value = "";
                }
        } );

        $("thead input").blur( function (i) {
                if ( this.value == "" )
                {
                        this.className = "search_init";
                        this.value = asInitVals[$("thead input").index(this)];
                }
        } );
	*/



	$("tfoot input").each( function (i) {
		asInitVals[i] = this.value;
	} );
	
	$("tfoot input").focus( function () {
		if ( this.className == "search_init" )
		{
			this.className = "";
			this.value = "";
		}
	} );
	
	$("tfoot input").blur( function (i) {
		if ( this.value == "" )
		{
			this.className = "search_init";
			this.value = asInitVals[$("tfoot input").index(this)];
		}
	} );
}


//function to extract the total sum of the columns of a  table

function sumColumn( item, nRow, aaData, iStart, iEnd, aiDisplay ) {
			/*
			 * Calculate the total market share for all browsers in this table (ie inc. outside
			 * the pagination)
			 */

			var iTotalMarket = 0;
			for ( var i=0 ; i<aaData.length ; i++ )
			{
				iTotalMarket += aaData[i][item]*1.;
			}
			
			/* Calculate the market share for browsers on this page */
			var iPageMarket = 0;
			for ( var i=iStart ; i<iEnd ; i++ )
			{
				iPageMarket += aaData[ aiDisplay[i] ][item]*1.;
			}
	
			return parseInt(iPageMarket*100)/100 + '<br>' + parseInt(iTotalMarket*100)/100	
			}

function fnFooterCallBack( nRow, aaData, iStart, iEnd, aiDisplay ) {
	/*console.dir(this.fnSettings().aoColumns);*/

	var columns=this.fnSettings().aoColumns;
	var aCol=-1;
	var col_text;
	for (var icol in columns){
		        aCol+=1;
			if(aCol!=0){
		 		var item = columns[icol].mDataProp
				col_text = sumColumn(item,nRow, aaData, iStart, iEnd, aiDisplay);
			}else{
			col_text = 'Shown Sum <br> Total Sum'
			}	
				/* Modify the footer row to match what we want */
		var nCells = nRow.getElementsByTagName('th');
		nCells[aCol].innerHTML = col_text
	}
}


function getServerData( sSource, aoData, fnCallback ) {
  $.getJSON( sSource, aoData, function (json) {
    if (json.sError != undefined)
    {
      alert(json.sError);
    }
    fnCallback(json)
  });
}

//functions to create dataset table
function DataSetTable(url) {
                var apiUrl = url;
                var table = createDataSetTable(apiUrl, '#DataSetTable', [ [0, 'asc'] ]);
		return table;
         };


function createDataSetTable(apiUrl,id,theSorting) {

        var oTable = $(id).dataTable( {
                         "iDisplayLength": 10,
                         "aLengthMenu": [5, 10, 25],
                         "bDestroy": true,
                         "bProcessing": true,
                         "sAjaxSource": apiUrl,
                         "sAjaxDataProp":"DATA",
                         "aaSorting": theSorting,
                         "aoColumns": [
                                 { "mDataProp": "COLLNAME" }
                         ],
                         //"fnFooterCallback": fnFooterCallBack,
                         "fnServerData": function ( sSource, aoData, fnCallback ) {
                                $.ajax( {
                                "dataType": 'json',
                                "type": "GET",
                                "url": sSource,
                                "data": aoData,
                                "success": fnCallback,
                                "statusCode": {
                                        400: function(xhr,err) {
                                                alert("BAD REQUEST: \n"+xhr.responseText);
                                                //alert('BAD REQUEST\ncould not load data\nplease check input values');
                                        },
                                        500: function() {
                                                alert('INTERNAL SERVER ERROR\ncould not load data');                                                                            }
                                        }
                                } );
                         }
                 } );
        setColFilter(oTable);
	return oTable;
}




//common functions that creates the data table

function aDataStatInTimeWindow(apiUrl,id,theSorting) {

		var startDate=$("#startDate").val();
		if (startDate != '') {apiUrl=apiUrl+"&tstart="+startDate;}
		var endDate=$("#endDate").val();
		if (endDate !='') {apiUrl=apiUrl+"&tstop="+endDate; }

        var oTable = $(id).dataTable( {
			 "iDisplayLength": 10,
			 "aLengthMenu": [[10, 25, 50, -1],[10, 25, 50, "All"]],                 
			 "bDestroy": true,
             		 "bProcessing": true,
             		 "sAjaxSource": apiUrl,
			 "sAjaxDataProp":"DATA",
			 "aaSorting": theSorting,
             		 "aoColumns": [ 
                                 { "mDataProp": "COLLNAME" },
                                 { "mDataProp": "NACC" },
                                 { "mDataProp": "RNACC" },
                                 { "mDataProp": "TOTCPU" },
                                 { "mDataProp": "RTOTCPU" },
                                 { "mDataProp": "NUSERS" },
                                 { "mDataProp": "RNUSERS" }
                         ],
   			 "fnFooterCallback": fnFooterCallBack,
			 "fnServerData": function ( sSource, aoData, fnCallback ) {
                                $.ajax( {
                                "dataType": 'json',
                                "type": "GET",
                                "url": sSource,
                                "data": aoData,
                                "success": fnCallback,
                                "statusCode": {
                                        400: function(xhr,err) {
                                                alert("BAD REQUEST: \n"+xhr.responseText);
                                                //alert('BAD REQUEST\ncould not load data\nplease check input values');
                                        },
                                        500: function() {
                                                alert('INTERNAL SERVER ERROR\ncould not load data');                                        					}
                                	}
				} );
			 }	
                 } );
        setColFilter(oTable);
        //update "getjson" button url on the table page 
        setJSONurl(apiUrl);
         
         
}

//functions that creates the dataTier table	
function DataTierStatInTimeWindow(url) {
		var apiUrl = url+"?";
                var siteName = $("#select_siteName").val();
                if (siteName != "all") {apiUrl = apiUrl+"&sitename="+siteName}
		aDataStatInTimeWindow(apiUrl, '#DataTierStatInTimeWindow', [ [0, 'asc'] ]);
         };


//functions that creates the dataSet tabe	
function DataSetStatInTimeWindow(url) {

		var apiUrl = url+"?";
                var siteName = $("#select_siteName").val();
                if (siteName != "all") {apiUrl = apiUrl+"&sitename="+siteName}

		aDataStatInTimeWindow(apiUrl,'#DataSetStatInTimeWindow',[ [4,'desc'] ]);
         };

//functions that creates the dataSet table	
function DataSetNameStatInTimeWindow(url) {

		var apiUrl=url+"?"
                var siteName = $("#select_siteName").val();
                if (siteName != "all") {apiUrl = apiUrl+"&sitename="+siteName}
		aDataStatInTimeWindow(apiUrl,'#DataSetNameStatInTimeWindow',[ [4,'desc'] ]);
         };


function dump(arr,level) {
	var dumped_text = "";
	if(!level) level = 0;
	
	//The padding given at the beginning of the line.
	var level_padding = "";
	for(var j=0;j<level+1;j++) level_padding += "    ";
	
	if(typeof(arr) == 'object') { //Array/Hashes/Objects 
		for(var item in arr) {
			var value = arr[item];
			
			if(typeof(value) == 'object') { //If it is an array,
				dumped_text += level_padding + "'" + item + "' ...\n";
				dumped_text += dump(value,level+1);
			} else {
				dumped_text += level_padding + "'" + item + "' => \"" + value + "\"\n";
			}
		}
	} else { //Stings/Chars/Numbers etc.
		dumped_text = "===>"+arr+"<===("+typeof(arr)+")";
	}
	return dumped_text;
}

//functions that creates the userTable	
function userStatTable(url){
		var dataTier= $("#select_dataTier").val();
		var apiUrl=url+"?collname="+dataTier
		var startDate=$("#startDate").val();
		if (startDate != '') {apiUrl=apiUrl+"&tstart="+startDate;}
		var endDate=$("#endDate").val();
		if (endDate !='') {apiUrl=apiUrl+"&tstop="+endDate; }
		var oTable = $('#userStat').dataTable( {
			 "iDisplayLength": 10,
			 "aLengthMenu": [[10, 25, 50, -1],[10, 25, 50, "All"]],                 
			 "bDestroy": true,
             		 "bProcessing": true,
             		 "sAjaxSource": apiUrl ,
			 "sAjaxDataProp":"DATA",
             		 "aoColumns": [ 
                                 { "mDataProp": "USERNAME" },
                                 { "mDataProp": "NACC" },
                                 { "mDataProp": "RNACC" },
                                 { "mDataProp": "TOTCPU" },
                                 { "mDataProp": "RTOTCPU" },
                                 { "mDataProp": "NSITES" },
                                 { "mDataProp": "RNSITES" }
                         	],
   			 "fnFooterCallback": fnFooterCallBack,
			 "fnServerData": function ( sSource, aoData, fnCallback ) {
            		 	$.ajax( {
                	 	"dataType": 'json', 
                		"type": "GET", 
                		"url": sSource, 
                		"data": aoData, 
                		"success": fnCallback,
				"statusCode": {
					400: function(xhr,err) {
                                                alert("BAD REQUEST: \n"+xhr.responseText);
						//alert('BAD REQUEST\ncould not load data\nplease check input values');
                                        },
                                        500: function() {
                                                alert('INTERNAL SERVER ERROR\ncould not load data');                                        }
            			}} );
        		 } 	
                 } );
        setColFilter(oTable);
        //update "getjson" button url on the table page 
        setJSONurl(apiUrl);
}


//functions that creates the corrupted files table	
function corruptedFilesTable(apiUrl,info) {
        var oTable = $("#"+info.placeholder).dataTable( {
			 "iDisplayLength": info.iDisplayLength,
			 "aLengthMenu": [[10, 25, 50, -1],[10, 25, 50, "All"]],                 
			 "bDestroy": true,
             		 "bProcessing": true,
             		 "sAjaxSource": apiUrl,
			 "sAjaxDataProp":"DATA",
			 "aaSorting": info.sorting,
             		 "aoColumns": info.aoColumns, 
			 "fnServerData": function ( sSource, aoData, fnCallback ) {
                                $.ajax( {
                                "dataType": 'json',
                                "type": "GET",
                                "url": sSource,
                                "data": aoData,
                                "success": fnCallback,
                                "statusCode": {
                                        400: function(xhr,err) {
                                                alert("BAD REQUEST: \n"+xhr.responseText);
                                        },
					500: function() {
                                                alert('INTERNAL SERVER ERROR\ncould not load data');
                                        }
                                }} );
                 }} );
        setColFilter(oTable);
        //update "getjson" button url on the table page 
        setJSONurl(apiUrl);


	//Added this function to allow at click of a raw the redirection to the JSON information of the specific site
	$('#'+info.placeholder+' tbody tr').live('dblclick', function () {
								 var cells = this.cells;
								 window.location.href = 'getCorruptedFiles/?sitename='+cells[0].textContent;
								 })         

}

