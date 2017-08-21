/* globals define, ngwConfig */
define([
    "dojo/_base/lang",
    "./load-json!api/component/pyramid/route"
], function (
    lang,
    rdata
) {
    var module = {};

    var generator = function (args) {
        var sub,
            template = this[0],
            keys = this.slice(1),
            isArray = Object.prototype.toString.call(args) === '[object Array]',
            isObject = Object.prototype.toString.call(args) === '[object Object]';
        
        if (isArray) {
            // Список замен можно указать в виде массива.
            sub = args;
        } else if (!isObject) {
            // Если список замен не массив и не объект, то используем
            // в качестве списка замен массив аргументов, особенно это
            // полезно в случае одного аргумента.
            sub = arguments;
        } else {
            // Если в качестве списка замен передали объект, то 
            // используем его ключи для подстановки, но вначале
            // нужно преобразовать их в массив.
            sub = [];
            for (var k in args) { sub[keys.indexOf(k)] = args[k]; }
        }

        return ngwConfig.applicationUrl + template.replace(/\{(\w+)\}/g, function (m, a) {
            var idx = parseInt(a), value = sub[idx];

            // TODO: Неплохо бы так же добавить имя маршрута в сообщение.
            if (value === undefined) { console.error("Undefined parameter " + idx + ":" + keys[idx] + " in URL " + template + "."); }
            
            return value;
        });
    };

    // Перед сборкой объекта нужно отсортировать ключи, так чтобы
    // ключ foo был обработан раньше foo.bar, иначе ключ foo.bar
    // может оказаться недоступен в итоговом объекте.
    var rkeys = [];
    for (var k in rdata) { rkeys.push(k); }
    rkeys.sort();
    
    for (var i in rkeys) {
        var rname = rkeys[i];
        lang.setObject(rname, lang.hitch(rdata[rname], generator), module);
    }

    console.log('Route initialization completed, registered ' + rkeys.length + ' routes.');

    return module;
});
