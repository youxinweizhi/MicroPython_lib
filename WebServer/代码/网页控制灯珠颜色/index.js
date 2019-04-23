$(document).ready(function() {
    $('.colorpicker').minimalColorpicker({
        color: '#4513e9',
        onUpdateColor: function(e, color) {
            console.log(color);
            $.ajax({
                url: "/test/",
                type: "post",
                datatype: "json",
                data: JSON.stringify({"code":color}),
                success: function (callback) {
                    console.log(callback);
                }

            })
        }
    });
});

jQuery.fn.minimalColorpicker = function(options) {

    var defaults = {
        color: '#000000'
    };

    var settings = $.extend({}, defaults, options);

    return this.each(function() {
        var self = $(this);
        var hue = $('<div />').addClass('hue');
        var hueDrag = $('<div />').addClass('drag');
        var field = $('<div />').addClass('field');
        var fieldOverlay = $('<div />').addClass('fieldOverlay');
        var fieldDrag = $('<div />').addClass('drag');
        var input = $('<input />').val('#ffffff');
        var rgbList = $('<ul />');
        rgbList.append($('<li />').html('<strong>255</strong>R'));
        rgbList.append($('<li />').html('<strong>255</strong>G'));
        rgbList.append($('<li />').html('<strong>255</strong>B'));

        if(tinycolor(settings.color).isValid()) {
            self.color = tinycolor(settings.color).toHsl();
        }

        if(tinycolor(self.data('color')).isValid()) {
            self.color = tinycolor(self.data('color')).toHsl();
        }

        hue.append(hueDrag);
        self.append(hue);
        fieldOverlay.append(fieldDrag);
        field.append(fieldOverlay);
        self.append(field);
        self.append(input);
        self.append(rgbList);

        self.hue = hue.get(0);
        self.hue.drag = hueDrag.get(0);

        self.fieldBase = field.get(0);
        self.field = fieldOverlay.get(0);
        self.field.drag = fieldDrag.get(0);

        self.updateHue = function(e) {
            self.setHue(e.offsetY / hue.outerHeight() * 360);
            if(self.hue.onmousemove === null) {
                self.hue.onmousemove = function(e) {
                    if(e.target === self.hue) {
                        self.setHue(e.offsetY / hue.outerHeight() * 360);
                        e.stopPropagation();
                    }
                }
            }
            self.clearMousemove('hue');
        }

        self.updateColor = function(e) {
            self.setColorPos(e.offsetX, e.offsetY);
            if(self.field.onmousemove === null) {
                self.field.onmousemove = function(e) {
                    if(e.target === self.field) {
                        self.setColorPos(e.offsetX, e.offsetY);
                        e.stopPropagation();
                    }
                }
            }
            self.clearMousemove('field');
        }

        self.setColorPos = function(x, y) {
            self.field.drag.style.setProperty('--x', x);
            self.field.drag.style.setProperty('--y', y);
            self.color = tinycolor({
                h: self.color.h,
                s: ((x / (field.outerWidth() - 1)) * 100),
                v: ((1 - y / (field.outerHeight() - 1)) * 100)
            }).toHsl();
            self.setColor();
        }

        self.setHue = function(a) {
            self.color.h = a;
            self.setColor();
        }

        self.setColor = function(e) {
            var c = tinycolor(self.color);
            chsv = c.toHsv();
            c = c.toHslString();
            self.field.drag.style.setProperty('--x', Math.round((chsv.s) * (field.outerWidth() - 1)) + 'px');
            self.field.drag.style.setProperty('--y', Math.round((1 - chsv.v) * (field.outerHeight())) + 'px');
            self.hue.drag.style.setProperty('--y', self.color.h / 360 * hue.outerHeight() + 'px');
            self.fieldBase.style.setProperty('--backgroundHue', self.color.h);
            if(options.onUpdateColor !== undefined) {
                options.onUpdateColor(e, {
                    hex: tinycolor(self.color).toHex(),
                    rgb: tinycolor(self.color).toRgb(),
                    rgbString: tinycolor(self.color).toRgbString()
                });
            }
            self.setOutput();
        }

        self.setOutput = function(e) {
            input.val('#' + tinycolor(self.color).toHex());
            rgbList.find('li:nth-child(1) strong').text(tinycolor(self.color).toRgb().r);
            rgbList.find('li:nth-child(2) strong').text(tinycolor(self.color).toRgb().g);
            rgbList.find('li:nth-child(3) strong').text(tinycolor(self.color).toRgb().b);
        }

        self.updateOutput = function(e) {
            if(input.val().length == 7 && tinycolor(input.val()).isValid()) {
                var c = tinycolor(input.val());
                self.color = c.toHsl();
                self.setColorPos(Math.round((c.toHsv().s) * (field.outerWidth() - 1)), Math.round((1 - c.toHsv().v) * (field.outerHeight())));
                self.setColor();
                self.setOutput();
            }
        }

        self.clearMousemove = function(m) {
            if(document.onmouseup === null) {
                document.onmouseup = function(e) {
                    self[m].onmousemove = null;
                    document.onmouseup = null;
                }
            }
        }

        input.on('change keyup', self.updateOutput);
        field.on('mousedown', self.updateColor);
        hue.on('mousedown', self.updateHue);

        self.setColor();
        self.setHue(self.color.h);
        self.setOutput();

    });

}