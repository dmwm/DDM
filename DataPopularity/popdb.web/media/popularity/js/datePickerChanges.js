$.datepicker.formatDate('yy-mm-dd');
/*
$(document).ready(
        function(){
		var today = new Date();
		today.setDate(today.getDate()-1);
                $("#endDate").val(today.getFullYear()+"-"+(today.getMonth()+1)+"-"+today.getDate());
                var start = new Date();
                today.setDate(today.getDate()-7);
                $('#startDate').val(today.getFullYear()+"-"+(today.getMonth()+1)+"-"+today.getDate());
	}
);
*/
function setDefaultEndDate(){
	var end = new Date();
        end.setDate(end.getDate()-1);
        $("#endDate").val(end.getFullYear()+"-"+(end.getMonth()+1)+"-"+end.getDate());

}

function setDefautlStartDate(){
        var start = new Date();
        start.setDate(start.getDate()-8);
        $('#startDate').val(start.getFullYear()+"-"+(start.getMonth()+1)+"-"+start.getDate());

}

$(document).ready(
	function(){
		$("#startDate").bind("change",'', function(){
				 var startDate=$("#startDate").val(); 
				 if(startDate) { 
				 	$("#endDate").datepicker("option","minDate", startDate ); 
				 }
				 });
		$('.inputDate').datepicker(
		
		{
		    dateFormat: 'yy-mm-dd' ,
		    showWeek: true,
		    firstDay: 1,
		    maxDate:"yesterday"	

		}	
		);
	}


);
