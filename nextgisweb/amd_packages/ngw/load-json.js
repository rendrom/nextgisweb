define([
    "dojo/request/xhr"
], function (
    xhr
) {
    return {
        load: function (id, require, load) {
            xhr.get(ngwConfig.applicationUrl + '/' + id, {
                handleAs: 'json'
            }).then(
                function (data) {
                    load(data);
                },
                function (error) {
                    load();
                }
            )
        }
    }
});