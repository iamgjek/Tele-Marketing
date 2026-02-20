function openYH(){
    $.blockUI({
        message: "<img src='/static/images/Spinner-5.gif' style='width:50%' >", 
        //borderWidth:'0px' 和透明背景
        css: { borderWidth: '0px', backgroundColor: 'transparent' },
    });
}

function closeYH(){
    $.unblockUI();
}