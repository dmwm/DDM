$.datepicker.formatDate('yy-mm-dd');
function setDefaultEndDate(){
	var end = new Date();
        end.setDate(end.getDate()+1);
        $("#endDate").val(end.getFullYear()+"-"+(end.getMonth()+1)+"-"+end.getDate());

}

function setDefautlStartDate(){
        var start = new Date();
        start.setDate(start.getDate()-7);
        $('#startDate').val(start.getFullYear()+"-"+(start.getMonth()+1)+"-"+start.getDate());

}

function bindEndDate(){
		$("#startDate").bind("change",'', function(){
				 var startDate=$("#startDate").val(); 
				 if(startDate) { 
				 	$("#endDate").datepicker("option","minDate", startDate ); 
				 	}
				 }
				);
}

function setOptionDate(){
		$('.inputDate').datepicker(
		{
		    dateFormat: 'yy-mm-dd' ,
		    showWeek: true,
		    firstDay: 1,
		    maxDate:+1,
		    changeMonth: true,
		    changeYear: true	

		}	
		);
	}


function setDates(){
	setDefaultEndDate();
	setDefautlStartDate();
	bindEndDate();
	setOptionDate();
}