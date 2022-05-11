(function ($) {
    "use strict";
      
    /*--
    Skillbar Instance
  -----------------------------------*/
  
  var deferJs = {
    i: function (e) {
        deferJs.d();
        deferJs.methods();
    },

    d: function (e) {
        this._window = $(window),
            this._document = $(document),
            this._body = $('body'),
            this._html = $('html')

    },

    methods: function (e) {
        deferJs.radialProgress();
    },

    radialProgress: function () {
        $('.radial-progress').waypoint(function () {
            $('.radial-progress').easyPieChart({
                lineWidth: 10,
                scaleLength: 0,
                rotate: 0,
                trackColor: false,
                lineCap: 'round',
                size: 123
            });
        }, {
            triggerOnce: true,
            offset: 'bottom-in-view'
        });
    }
  }
  deferJs.i();


})(jQuery);