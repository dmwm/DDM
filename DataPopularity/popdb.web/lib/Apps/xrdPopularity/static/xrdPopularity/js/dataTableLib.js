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



function axrdMonitoringDataTable(url,id,theSorting) {

        var oTable = $(id).dataTable( {
			 "iDisplayLength": 10,
			 "aLengthMenu": [[10, 25, 50, -1],[10, 25, 50, "All"]],                 
			 "bDestroy": true,
             		 "bProcessing": true,
             		 "sAjaxSource": url,
			 "sAjaxDataProp":"DATA",
			 "aaSorting": theSorting,
             		 "aoColumns": [ 
                                 { "mDataProp": "XTIME" },
                                 { "mDataProp": "YVALUE" },
                                 { "mDataProp": "RATE" }
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
function xrdMonitoringDataTable(url) {	
		//var apiUrl = buildUrl(url);
		axrdMonitoringDataTable(url, '#xrdMonitoringDataTable', [ [0, 'desc'] ]);
}	



//common functions that creates the data table

function DataStatInTimeWindow(apiUrl,info) {
        var oTable = $("#"+info.placeholder).dataTable( {
			 "iDisplayLength": info.iDisplayLength,
			 "aLengthMenu": [[10, 25, 50, -1],[10, 25, 50, "All"]],                 
			 "bDestroy": true,
             		 "bProcessing": true,
             		 "sAjaxSource": apiUrl,
			 "sAjaxDataProp":"DATA",
			 "aaSorting": info.sorting,
             		 "aoColumns": info.aoColumns, 
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

