$.datepicker.formatDate('yy-mm-dd');

function formatdate(n){
	if (parseInt(n)<10) {
		return "0"+n;
	}
	else return ""+n;
}


function setDefaultEndDate(){
	var end = new Date();
        end.setDate(end.getDate()+1);
        $("#endDate").val(end.getFullYear()+"-"+formatdate(end.getMonth()+1)+"-"+formatdate(end.getDate()));

}

function setDefautlStartDate(){
        var start = new Date();
        start.setDate(start.getDate()-7);
        $('#startDate').val(start.getFullYear()+"-"+formatdate(start.getMonth()+1)+"-"+formatdate(start.getDate()));

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
        setOptionDate();
        //$.datepicker.formatDate('yy-mm-dd');
	setDefaultEndDate();
	setDefautlStartDate();
	bindEndDate();
	//setOptionDate();
}
