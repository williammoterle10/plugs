(function($){
    QueryString = function(options){
        this.urlParams = {};
        this.load();
    }
    QueryString.prototype = {
        load: function(param){
            this.urlParams = {}
            var e,k,v,
                a = /\+/g,  // Regex for replacing addition symbol with a space
                r = /([^&=]+)=?([^&]*)/g,
                d = function (s) { return decodeURIComponent(s.replace(a, " ")); }
            if(!param){
                param = window.location.search;
            }
            if (param.charAt(0) == '?'){
                param = param.substring(1);
            }
            while (e = r.exec(param)){
                k = d(e[1]);
                v = d(e[2]);
                this.set(k, v);
            }
            return this;
        },
        toString:function(options){
            var settings = {
                'hash' : false,
                'traditional' : true
            };
            if ( options ) { 
              $.extend( settings, options );
            }
            var old = jQuery.ajaxSettings.traditional;
            jQuery.ajaxSettings.traditional = settings.traditional;
            var result = '?' + $.param(this.urlParams);
            jQuery.ajaxSettings.traditional = old;
            if (settings.hash)
                result = result + window.location.hash;
            return result;
        },
        set:function(k, v, replace){
            replace = replace || false;
            if (replace)
                this.urlParams[k] = v;
            else{
                if (k in this.urlParams){
                    if ($.type(this.urlParams[k]) === 'array'){
                        this.urlParams[k].push(v);
                    }
                    else{
                        if (this.urlParams[k] == '')
                            this.urlParams[k] = v;
                        else
                            this.urlParams[k] = [this.urlParams[k], v];
                    }
                }
                else
                    this.urlParams[k] = v;
            }
            return this;
        },
        get:function(k){
            return this.urlParams[k];
        },
        remove:function(k){
            if (k in this.urlParams){
                delete this.urlParams[k];
            }
            return this;
        }
    }
    $.query_string = new QueryString();
})(jQuery);

(function($){
    $(function(){
        jQuery('<iframe src="" style="display:none" id="ajaxiframedownload"></iframe>')
        .appendTo('body');
    });
    $.download = function(url){
    	//url and data options required
    	if(url){ 
    		//send request
            var el = $('#ajaxiframedownload');
            el.attr('src', url);
    	};
    };
})(jQuery);