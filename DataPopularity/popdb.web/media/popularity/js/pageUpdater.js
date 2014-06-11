function setJSONurl(url){

    var js = "window.open('"+url+"');";
    // create a function from the "js" string
    var newclick = new Function(js);

    // clears onclick then sets click using jQuery
    $("#getjeson").attr('onClick', '').unbind('click').click(newclick);
    $("#jsonurl").html(url);
    $("#jsonurl").attr("href", url)

}
