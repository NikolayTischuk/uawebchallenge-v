function is_valid_url(url) {
     return url.match(/^https?:\/\/[a-z0-9-\.]+\.[a-z]{2,4}\/?([^\s<>\#%"\,\{\}\\|\\\^\[\]`]+)?$/);
}

var Page = function(link) {
    var self = this;
    self.link = ko.observable(link);
}

var app = {};
app.sending = function(link, params, type) {
    app.result.loading(true);
    app.result.unused.removeAll();
    
    var xhrAjax = $.ajax({'url':link, 'data':params, 'type':'POST'});
    xhrAjax.done(function(xhr) {
        app.result.loading(false);
        if(xhr.result == true) {
            if(!xhr.unused) {
                 return false;
            }
            
            $.each(xhr.unused, function(i, params) {
                var result = new Result(params);
                app.result.unused.push(result);
            });
        }
    });
};

var Result = function(data) {
    var self = this;
    self.website = ko.observable(data.uri);
    self.unused = ko.observable(data.unused);
}

app.result = {
    'unused'  : ko.observableArray([]),
    'loading' : ko.observable(false),
}

app.pages = {
    'url'  : ko.observable(''),
    'links': ko.observableArray([]),
    'list' : ko.observable(false),
    // add new link
    'push' : function(element) {
        var link = app.pages.url();
        if(!link || !is_valid_url(link)) {
            return false;
        }

        var page = new Page(link);
        app.pages.links.push(page);
        app.pages.list(true);

        app.pages.url('');
    },
    'remove':function(page) {
        if(!app.pages.links.length) {
            app.pages.list(false);
        }
        
        app.pages.links.remove(page);
    },
    'sending': function(element) {
        var form = $(element);
        var links = app.pages.links();
        if(links.length) {
            var pages = [];
            var length = links.length;
            for(var i = 0; i<length; i++) {
                var page = links[i];
                pages.push(page.link());
            }
            
            var serialize = form.serializeArray();
            serialize.push({name:'links', value:pages});
            var params = {};
            $.each(serialize, function(i, item) {
                params[item.name] = item.value;
            })
            
            app.sending(form.attr('action'), params, form.attr('method'));
        }

        return false;
    }
};
app.website = {
    'url'    : ko.observable(''),
    'depth'  : ko.observable(),
    'sending': function(element) {
        var form = $(element);
        var control = form.find('#url').parents('.control-group:first');
        control.removeClass('error');

        if(!app.website.url()) {
            control.addClass('error');
            return false;
        }

        app.sending(form.attr('action'), form.serialize(), form.attr('method'));
        return false;
    }
};

$(document).ready(function() {
    ko.applyBindings(app);
});