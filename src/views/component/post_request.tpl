<html>
    <head>
        <script src="/files/third/jquery3_1/jquery-3.1.0.js" type="text/javascript"></script>
        <script src="/files/third/jquery_base64_js/jquery.base64.js"></script>
        
        <script type="text/javascript">
            $(document).ready(function(){
                debugger;
                var data = "{{post_data}}";
                var data_str = $('<div/>').html(data).text();
                var data_json = eval('(' + data_str + ')');
                
                for(var p in data_json){
                    var key = p;
                    var value = data_json[p];
                    var item_post_input = $('<input type="text" name="' + key + '" value="' + value + '"/>');
                    $("#post_form").append(item_post_input);
                }  
              
                $("#post_form_submit").click();
            });
        </script>
        
    <title>Post Request</title>
    </head>
    <body>
        <form id="post_form" action="{{url}}" method="post">
            <input id="post_form_submit" type="submit" value="Submit" hidden="true"/>
        </form>
    </body>
</html>
